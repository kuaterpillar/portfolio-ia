import imaplib
import email
from email.header import decode_header
import sqlite3
import re
from datetime import datetime
import os

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class EmailClassifier:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key and OPENAI_AVAILABLE:
            openai.api_key = self.openai_api_key
        self.setup_database()

    def setup_database(self):
        """Créer la base de données pour stocker les emails triés"""
        self.conn = sqlite3.connect('emails_trie.db')
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                subject TEXT,
                content TEXT,
                priority INTEGER,
                priority_label TEXT,
                date_received TEXT,
                processed_date TEXT
            )
        ''')
        self.conn.commit()

    def connect_to_email(self, email_address, password, imap_server='imap.gmail.com'):
        """Se connecter au serveur email IMAP"""
        try:
            self.mail = imaplib.IMAP4_SSL(imap_server)
            self.mail.login(email_address, password)
            self.mail.select('inbox')
            return True
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return False

    def get_emails(self, count=10):
        """Récupérer les emails récents"""
        try:
            status, messages = self.mail.search(None, 'ALL')
            email_ids = messages[0].split()[-count:]
            emails = []

            for email_id in email_ids:
                status, msg_data = self.mail.fetch(email_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])

                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()

                sender = msg.get("From")

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                emails.append({
                    'sender': sender,
                    'subject': subject,
                    'body': body[:500],  # Limiter à 500 caractères
                    'date': msg.get("Date")
                })

            return emails
        except Exception as e:
            print(f"Erreur lors de la récupération des emails: {e}")
            return []

    def classify_email_priority(self, subject, sender, body):
        """Classifier l'email par ordre d'importance"""
        # Mots-clés pour classification rapide
        urgent_keywords = ['urgent', 'emergency', 'problème', 'panne', 'réclamation', 'plainte', 'incident']
        high_keywords = ['réservation', 'booking', 'demande', 'nouveau client', 'rdv', 'rendez-vous']
        low_keywords = ['newsletter', 'promo', 'marketing', 'publicité', 'unsubscribe']

        text = f"{subject} {body}".lower()

        # Classification par mots-clés
        if any(keyword in text for keyword in urgent_keywords):
            return 4, "URGENT"
        elif any(keyword in text for keyword in high_keywords):
            return 3, "HAUTE"
        elif any(keyword in text for keyword in low_keywords):
            return 1, "BASSE"
        else:
            # Classification IA si clé OpenAI disponible
            if self.openai_api_key and OPENAI_AVAILABLE:
                return self.classify_with_ai(subject, sender, body)
            else:
                return 2, "MOYENNE"

    def classify_with_ai(self, subject, sender, body):
        """Classification avancée avec OpenAI"""
        try:
            prompt = f"""
            Analysez cet email reçu par une entreprise de conciergerie et classez sa priorité:

            Expéditeur: {sender}
            Sujet: {subject}
            Contenu: {body[:300]}

            Critères de priorité:
            4-URGENT: Urgences, pannes, réclamations graves, problèmes techniques
            3-HAUTE: Nouvelles demandes clients, réservations, rendez-vous
            2-MOYENNE: Confirmations, demandes d'information, suivi
            1-BASSE: Newsletters, spam, promotions

            Répondez uniquement avec le format: "4,URGENT" ou "3,HAUTE" ou "2,MOYENNE" ou "1,BASSE"
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10
            )

            result = response.choices[0].message.content.strip()
            priority_num, priority_label = result.split(',')
            return int(priority_num), priority_label

        except Exception as e:
            print(f"Erreur classification IA: {e}")
            return 2, "MOYENNE"

    def process_emails(self, email_address, password):
        """Traiter et classer tous les emails"""
        if not self.connect_to_email(email_address, password):
            return False

        emails = self.get_emails(50)  # Traiter les 50 derniers emails

        for email_data in emails:
            priority_num, priority_label = self.classify_email_priority(
                email_data['subject'],
                email_data['sender'],
                email_data['body']
            )

            # Sauvegarder en base
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO emails (sender, subject, content, priority, priority_label, date_received, processed_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                email_data['sender'],
                email_data['subject'],
                email_data['body'],
                priority_num,
                priority_label,
                email_data['date'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))

        self.conn.commit()
        self.mail.logout()
        return True

    def get_sorted_emails(self):
        """Récupérer les emails triés par priorité"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM emails ORDER BY priority DESC, processed_date DESC')
        return cursor.fetchall()

    def close(self):
        """Fermer la connexion à la base"""
        self.conn.close()

if __name__ == "__main__":
    classifier = EmailClassifier()

    # Configuration (à remplacer par vos vraies données)
    EMAIL = "votre@email.com"
    PASSWORD = "votre_mot_de_passe"

    print("Démarrage du tri des emails...")
    if classifier.process_emails(EMAIL, PASSWORD):
        print("Emails traités avec succès!")

        # Afficher les résultats
        sorted_emails = classifier.get_sorted_emails()
        for email_row in sorted_emails[:10]:  # Top 10
            print(f"\n[{email_row[5]}] De: {email_row[1]}")
            print(f"Sujet: {email_row[2]}")
            print(f"Priorité: {email_row[5]}")

    classifier.close()