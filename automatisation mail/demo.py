"""
Script de démonstration pour tester la classification sans emails réels
"""

from email_classifier import EmailClassifier
import sqlite3
from datetime import datetime

def create_demo_data():
    """Créer des données de démonstration"""
    classifier = EmailClassifier()

    # Emails de test pour démonstration
    demo_emails = [
        {
            'sender': 'client.urgent@hotel.com',
            'subject': 'URGENT - Panne ascenseur étage 5',
            'body': 'Bonjour, l\'ascenseur de l\'étage 5 est en panne depuis ce matin. Nos clients sont bloqués.',
            'date': '2025-01-15 09:30:00'
        },
        {
            'sender': 'nouveau.client@gmail.com',
            'subject': 'Demande de réservation chambre',
            'body': 'Bonjour, je souhaiterais réserver une chambre pour le weekend du 25-26 janvier.',
            'date': '2025-01-15 10:15:00'
        },
        {
            'sender': 'newsletter@hotels.com',
            'subject': 'Newsletter - Offres spéciales janvier',
            'body': 'Découvrez nos offres spéciales pour le mois de janvier. Promotions exclusives.',
            'date': '2025-01-15 08:00:00'
        },
        {
            'sender': 'maintenance@building.com',
            'subject': 'Confirmation intervention plomberie',
            'body': 'Nous confirmons notre intervention de demain à 14h pour la réparation.',
            'date': '2025-01-15 11:00:00'
        },
        {
            'sender': 'client.vip@company.fr',
            'subject': 'Réclamation - Service de ménage insuffisant',
            'body': 'Je suis très déçu du service de ménage. La chambre n\'était pas propre à mon arrivée.',
            'date': '2025-01-15 16:45:00'
        }
    ]

    # Traiter chaque email de démonstration
    for email_data in demo_emails:
        priority_num, priority_label = classifier.classify_email_priority(
            email_data['subject'],
            email_data['sender'],
            email_data['body']
        )

        # Sauvegarder en base
        cursor = classifier.conn.cursor()
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

    classifier.conn.commit()
    classifier.close()
    return len(demo_emails)

def show_results():
    """Afficher les résultats du tri"""
    conn = sqlite3.connect('emails_trie.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM emails ORDER BY priority DESC, processed_date DESC')
    emails = cursor.fetchall()

    print("\n" + "="*80)
    print(" RESULTATS DU TRI AUTOMATIQUE DES EMAILS")
    print("="*80)

    priority_colors = {
        'URGENT': '[URGENT]',
        'HAUTE': '[HAUTE]',
        'MOYENNE': '[MOYENNE]',
        'BASSE': '[BASSE]'
    }

    for email in emails:
        id_email, sender, subject, content, priority_num, priority_label, date_received, processed_date = email

        icon = priority_colors.get(priority_label, '[AUTRE]')
        print(f"\n{icon} De: {sender}")
        print(f"   Sujet: {subject}")
        print(f"   Contenu: {content[:100]}...")
        print(f"   Traite le: {processed_date}")

    # Statistiques
    print("\n" + "-"*50)
    print(" STATISTIQUES")
    print("-"*50)

    stats = {}
    for email in emails:
        priority = email[5]
        stats[priority] = stats.get(priority, 0) + 1

    for priority, count in sorted(stats.items(), key=lambda x: ['URGENT', 'HAUTE', 'MOYENNE', 'BASSE'].index(x[0])):
        icon = priority_colors.get(priority, '[AUTRE]')
        print(f"{icon}: {count} emails")

    conn.close()

if __name__ == "__main__":
    print("DEMONSTRATION - SYSTEME DE TRI D'EMAILS CONCIERGERIE")
    print("\nCreation de donnees de test...")

    count = create_demo_data()
    print(f"OK - {count} emails de demonstration traites")

    show_results()

    print(f"\nInterface graphique disponible:")
    print(f"   python interface.py")

    print(f"\nBase de donnees creee: emails_trie.db")
    print(f"Classification automatique operationnelle!")