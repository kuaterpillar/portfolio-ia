"""
Classificateur adaptatif qui utilise la configuration business pour trier les emails
"""

import json
import os
import re
from datetime import datetime, time
import sqlite3
from email_classifier import EmailClassifier

class AdaptiveEmailClassifier(EmailClassifier):
    def __init__(self, config_file="business_config.json"):
        super().__init__()
        self.config_file = config_file
        self.business_config = self.load_business_config()

    def load_business_config(self):
        """Charger la configuration business"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"Configuration non trouvée: {self.config_file}")
            print("Utilisation de la configuration par défaut")
            return self.get_default_business_config()

    def get_default_business_config(self):
        """Configuration par défaut si aucune configuration n'existe"""
        return {
            "company_info": {"industry": "generic"},
            "priority_rules": {
                "urgent": {"keywords": ["urgent", "emergency"], "senders": [], "subjects": []},
                "high": {"keywords": ["important", "client"], "senders": [], "subjects": []},
                "medium": {"keywords": ["information", "question"], "senders": [], "subjects": []},
                "low": {"keywords": ["newsletter", "promo"], "senders": [], "subjects": []}
            },
            "business_hours": {"start": "09:00", "end": "18:00"},
            "special_rules": {"vip_clients": [], "blocked_senders": []}
        }

    def classify_email_priority(self, subject, sender, body):
        """Classification adaptative basée sur la configuration business"""

        # Vérifier les expéditeurs bloqués
        if self.is_blocked_sender(sender):
            return 0, "BLOQUE"

        # Vérifier les clients VIP
        if self.is_vip_client(sender):
            base_priority, label = self.classify_with_business_rules(subject, sender, body)
            # Augmenter la priorité pour les VIP
            return min(4, base_priority + 1), f"VIP-{label}"

        # Classification normale avec règles business
        return self.classify_with_business_rules(subject, sender, body)

    def classify_with_business_rules(self, subject, sender, body):
        """Classification utilisant les règles de l'entreprise"""
        text = f"{subject} {body}".lower()
        sender_lower = sender.lower()

        # Vérifier chaque niveau de priorité selon la config
        priorities = [
            (4, "URGENT", "urgent"),
            (3, "HAUTE", "high"),
            (2, "MOYENNE", "medium"),
            (1, "BASSE", "low")
        ]

        for priority_num, priority_label, config_key in priorities:
            rules = self.business_config["priority_rules"][config_key]

            # Vérifier mots-clés
            if self.check_keywords(text, rules["keywords"]):
                return priority_num, priority_label

            # Vérifier expéditeurs spécifiques
            if self.check_senders(sender_lower, rules.get("senders", [])):
                return priority_num, priority_label

            # Vérifier sujets spécifiques
            if self.check_subjects(subject.lower(), rules.get("subjects", [])):
                return priority_num, priority_label

        # Ajustement selon les horaires de travail
        return self.adjust_for_business_hours(2, "MOYENNE")

    def check_keywords(self, text, keywords):
        """Vérifier si le texte contient des mots-clés"""
        return any(keyword.lower() in text for keyword in keywords)

    def check_senders(self, sender, sender_patterns):
        """Vérifier si l'expéditeur correspond aux patterns"""
        for pattern in sender_patterns:
            if pattern.lower() in sender or sender.endswith(pattern.lower()):
                return True
        return False

    def check_subjects(self, subject, subject_patterns):
        """Vérifier si le sujet correspond aux patterns"""
        for pattern in subject_patterns:
            if pattern.lower() in subject:
                return True
        return False

    def is_vip_client(self, sender):
        """Vérifier si l'expéditeur est un client VIP"""
        vip_clients = self.business_config["special_rules"].get("vip_clients", [])
        sender_lower = sender.lower()

        for vip in vip_clients:
            vip_lower = vip.lower()
            if "@" in vip_lower:
                # Domaine ou email complet
                if vip_lower in sender_lower:
                    return True
            else:
                # Mot-clé dans l'email
                if vip_lower in sender_lower:
                    return True
        return False

    def is_blocked_sender(self, sender):
        """Vérifier si l'expéditeur est bloqué"""
        blocked = self.business_config["special_rules"].get("blocked_senders", [])
        sender_lower = sender.lower()

        for blocked_pattern in blocked:
            if blocked_pattern.lower() in sender_lower:
                return True
        return False

    def adjust_for_business_hours(self, priority_num, priority_label):
        """Ajuster la priorité selon les horaires de travail"""
        try:
            now = datetime.now().time()
            business_hours = self.business_config["business_hours"]

            start_time = time.fromisoformat(business_hours["start"])
            end_time = time.fromisoformat(business_hours["end"])

            # Si hors horaires de travail
            if not (start_time <= now <= end_time):
                weekend_priority = business_hours.get("weekend_priority", "normal")
                if weekend_priority == "low" and priority_num > 1:
                    # Réduire la priorité sauf pour les urgences
                    if priority_num < 4:  # Pas urgent
                        return max(1, priority_num - 1), f"HH-{priority_label}"

            return priority_num, priority_label

        except Exception:
            # En cas d'erreur, retourner la priorité normale
            return priority_num, priority_label

    def get_classification_stats(self):
        """Obtenir les statistiques de classification"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT priority_label, COUNT(*) as count
            FROM emails
            GROUP BY priority_label
            ORDER BY priority DESC
        ''')

        stats = {}
        total = 0
        for row in cursor.fetchall():
            priority, count = row
            stats[priority] = count
            total += count

        # Calculer les pourcentages
        percentages = {}
        for priority, count in stats.items():
            percentages[priority] = round((count / total * 100), 1) if total > 0 else 0

        return stats, percentages, total

    def analyze_classification_accuracy(self):
        """Analyser la précision de la classification"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT sender, subject, content, priority_label FROM emails ORDER BY processed_date DESC LIMIT 50')

        recent_emails = cursor.fetchall()

        print("\n--- ANALYSE DE CLASSIFICATION ---")
        print(f"Derniers {len(recent_emails)} emails classifiés:")

        priority_distribution = {}
        for email in recent_emails:
            priority = email[3]
            priority_distribution[priority] = priority_distribution.get(priority, 0) + 1

        for priority, count in sorted(priority_distribution.items()):
            percentage = round((count / len(recent_emails)) * 100, 1)
            print(f"  {priority}: {count} emails ({percentage}%)")

    def export_business_rules(self):
        """Exporter les règles business actuelles"""
        export_data = {
            "config_summary": {
                "company": self.business_config["company_info"]["name"],
                "industry": self.business_config["company_info"]["industry"],
                "created_at": self.business_config.get("created_at", ""),
            },
            "priority_rules": self.business_config["priority_rules"],
            "special_rules": self.business_config["special_rules"],
            "business_hours": self.business_config["business_hours"]
        }

        filename = f"business_rules_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"\nRègles exportées vers: {filename}")
        return filename

    def update_rules_from_feedback(self, email_id, correct_priority):
        """Mettre à jour les règles basées sur le feedback utilisateur"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT subject, sender, content FROM emails WHERE id = ?', (email_id,))

        email_data = cursor.fetchone()
        if not email_data:
            return False

        subject, sender, content = email_data

        # Analyser pourquoi la classification était incorrecte
        # et suggérer des améliorations

        print(f"\nEmail mal classifié:")
        print(f"Sujet: {subject}")
        print(f"De: {sender}")
        print(f"Priorité correcte: {correct_priority}")

        # TODO: Implémenter l'apprentissage automatique des règles

        return True

def create_industry_template(industry):
    """Créer un template de configuration pour une industrie"""
    templates = {
        "conciergerie": {
            "urgent": ["urgent", "panne", "broken", "réclamation", "urgence", "emergency", "incident"],
            "high": ["réservation", "booking", "nouveau client", "demande", "rdv", "maintenance"],
            "medium": ["confirmation", "information", "question", "facture", "planning"],
            "low": ["newsletter", "promo", "marketing", "publicité"]
        },
        "ecommerce": {
            "urgent": ["fraude", "chargeback", "réclamation", "retour urgent", "problème paiement"],
            "high": ["nouvelle commande", "paiement", "livraison", "stock", "client vip"],
            "medium": ["question produit", "suivi commande", "disponibilité", "sav"],
            "low": ["newsletter", "catalogue", "promotion", "marketing"]
        },
        "healthcare": {
            "urgent": ["urgence", "emergency", "critique", "vital", "ambulance"],
            "high": ["rdv", "consultation", "prescription", "résultats", "patient"],
            "medium": ["rappel", "information", "planning", "confirmation"],
            "low": ["newsletter", "formation", "congrès"]
        }
    }

    return templates.get(industry, templates["conciergerie"])

if __name__ == "__main__":
    # Tester le classificateur adaptatif
    classifier = AdaptiveEmailClassifier()

    print("Configuration chargée:")
    print(f"Entreprise: {classifier.business_config['company_info'].get('name', 'Non définie')}")
    print(f"Secteur: {classifier.business_config['company_info'].get('industry', 'generic')}")

    # Test de classification
    test_emails = [
        ("client.urgent@hotel.com", "URGENT - Panne ascenseur", "L'ascenseur est en panne"),
        ("newsletter@promo.com", "Offres spéciales", "Découvrez nos promotions"),
        ("vip@important-client.fr", "Question rapide", "J'ai une question")
    ]

    print("\n--- TESTS DE CLASSIFICATION ---")
    for sender, subject, body in test_emails:
        priority_num, priority_label = classifier.classify_email_priority(subject, sender, body)
        print(f"Email: {subject}")
        print(f"De: {sender}")
        print(f"Priorité: {priority_label} ({priority_num})")
        print("-" * 50)