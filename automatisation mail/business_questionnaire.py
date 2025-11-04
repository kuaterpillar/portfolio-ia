"""
Questionnaire de configuration pour adapter le tri d'emails aux besoins spécifiques de chaque entreprise
"""

import json
import os
from datetime import datetime

class BusinessQuestionnaire:
    def __init__(self):
        self.config_file = "business_config.json"
        self.default_config = self.get_default_config()

    def get_default_config(self):
        """Configuration par défaut"""
        return {
            "company_info": {
                "name": "",
                "industry": "",
                "size": "",
                "email_volume": ""
            },
            "priority_rules": {
                "urgent": {
                    "keywords": [],
                    "senders": [],
                    "subjects": [],
                    "response_time": "Immédiat"
                },
                "high": {
                    "keywords": [],
                    "senders": [],
                    "subjects": [],
                    "response_time": "1-4h"
                },
                "medium": {
                    "keywords": [],
                    "senders": [],
                    "subjects": [],
                    "response_time": "24h"
                },
                "low": {
                    "keywords": [],
                    "senders": [],
                    "subjects": [],
                    "response_time": "48h+"
                }
            },
            "business_hours": {
                "start": "09:00",
                "end": "18:00",
                "timezone": "Europe/Paris",
                "weekend_priority": "low"
            },
            "special_rules": {
                "vip_clients": [],
                "blocked_senders": [],
                "auto_archive": []
            }
        }

    def run_questionnaire(self):
        """Lancer le questionnaire interactif"""
        print("="*60)
        print(" CONFIGURATION PERSONNALISEE DU TRI D'EMAILS")
        print("="*60)
        print("\nCe questionnaire va adapter le système à votre entreprise.\n")

        config = self.default_config.copy()

        # 1. Informations entreprise
        config = self.get_company_info(config)

        # 2. Configuration des priorités selon le secteur
        config = self.configure_priorities(config)

        # 3. Règles spéciales
        config = self.configure_special_rules(config)

        # 4. Horaires de travail
        config = self.configure_business_hours(config)

        # 5. Sauvegarder
        self.save_config(config)

        print("\n" + "="*60)
        print(" CONFIGURATION TERMINEE !")
        print("="*60)
        print(f"Configuration sauvée dans: {self.config_file}")

        return config

    def get_company_info(self, config):
        """Récupérer les informations de l'entreprise"""
        print("\n--- INFORMATIONS ENTREPRISE ---")

        config["company_info"]["name"] = input("Nom de l'entreprise: ").strip()

        print("\nSecteur d'activité:")
        sectors = [
            "1. Conciergerie/Services",
            "2. E-commerce",
            "3. Santé/Médical",
            "4. Finance/Banque",
            "5. Immobilier",
            "6. Tech/IT",
            "7. Éducation",
            "8. Autre"
        ]

        for sector in sectors:
            print(f"  {sector}")

        choice = input("\nChoisir (1-8): ").strip()
        sector_map = {
            "1": "conciergerie", "2": "ecommerce", "3": "healthcare",
            "4": "finance", "5": "real_estate", "6": "tech",
            "7": "education", "8": "other"
        }
        config["company_info"]["industry"] = sector_map.get(choice, "other")

        print("\nTaille de l'entreprise:")
        print("  1. TPE (1-9 employés)")
        print("  2. PME (10-249 employés)")
        print("  3. Grande entreprise (250+ employés)")

        size_choice = input("Choisir (1-3): ").strip()
        size_map = {"1": "tpe", "2": "pme", "3": "grande"}
        config["company_info"]["size"] = size_map.get(size_choice, "pme")

        volume = input("\nVolume d'emails par jour (approximatif): ").strip()
        config["company_info"]["email_volume"] = volume

        return config

    def configure_priorities(self, config):
        """Configurer les priorités selon le secteur"""
        print("\n--- CONFIGURATION DES PRIORITES ---")

        industry = config["company_info"]["industry"]

        # Templates par secteur
        if industry == "conciergerie":
            config = self.configure_conciergerie_priorities(config)
        elif industry == "ecommerce":
            config = self.configure_ecommerce_priorities(config)
        elif industry == "healthcare":
            config = self.configure_healthcare_priorities(config)
        elif industry == "finance":
            config = self.configure_finance_priorities(config)
        else:
            config = self.configure_generic_priorities(config)

        # Personnalisation supplémentaire
        print("\nVoulez-vous ajouter des mots-clés personnalisés ? (o/n): ", end="")
        if input().lower() == 'o':
            config = self.add_custom_keywords(config)

        return config

    def configure_conciergerie_priorities(self, config):
        """Configuration spécifique conciergerie"""
        print("\nConfiguration pour CONCIERGERIE détectée...")

        config["priority_rules"]["urgent"]["keywords"] = [
            "urgent", "urgence", "emergency", "panne", "broken", "ne fonctionne pas",
            "réclamation", "plainte", "problème grave", "incident", "sécurité",
            "fuite", "coupure", "plus d'eau", "plus d'électricité"
        ]

        config["priority_rules"]["high"]["keywords"] = [
            "réservation", "booking", "check-in", "check-out", "arrivée",
            "nouveau client", "demande", "rdv", "rendez-vous", "maintenance",
            "réparation", "intervention", "livraison"
        ]

        config["priority_rules"]["medium"]["keywords"] = [
            "confirmation", "information", "question", "renseignement",
            "facture", "paiement", "devis", "planning", "horaires"
        ]

        config["priority_rules"]["low"]["keywords"] = [
            "newsletter", "promo", "promotion", "marketing", "publicité",
            "offre", "catalogue", "brochure", "spam"
        ]

        return config

    def configure_ecommerce_priorities(self, config):
        """Configuration spécifique e-commerce"""
        print("\nConfiguration pour E-COMMERCE détectée...")

        config["priority_rules"]["urgent"]["keywords"] = [
            "commande annulée", "problème paiement", "fraude", "réclamation",
            "retour urgent", "livraison manquée", "produit défectueux",
            "remboursement", "chargeback"
        ]

        config["priority_rules"]["high"]["keywords"] = [
            "nouvelle commande", "paiement", "livraison", "stock",
            "client vip", "partenaire", "fournisseur", "urgent"
        ]

        config["priority_rules"]["medium"]["keywords"] = [
            "question produit", "disponibilité", "délai", "suivi commande",
            "facture", "garantie", "sav"
        ]

        config["priority_rules"]["low"]["keywords"] = [
            "newsletter", "catalogue", "promotion", "enquête satisfaction",
            "marketing", "pub"
        ]

        return config

    def configure_healthcare_priorities(self, config):
        """Configuration spécifique santé"""
        print("\nConfiguration pour SANTE/MEDICAL détectée...")

        config["priority_rules"]["urgent"]["keywords"] = [
            "urgence", "emergency", "critique", "vital", "ambulance",
            "hospitalisation", "accident", "urgence médicale"
        ]

        config["priority_rules"]["high"]["keywords"] = [
            "rendez-vous", "consultation", "prescription", "résultats",
            "analyses", "patient", "médecin", "traitement"
        ]

        return config

    def configure_finance_priorities(self, config):
        """Configuration spécifique finance"""
        print("\nConfiguration pour FINANCE/BANQUE détectée...")

        config["priority_rules"]["urgent"]["keywords"] = [
            "fraude", "sécurité", "blocage compte", "transaction suspecte",
            "incident sécurité", "alerte", "urgent"
        ]

        config["priority_rules"]["high"]["keywords"] = [
            "crédit", "prêt", "virement", "paiement", "découvert",
            "client important", "investissement"
        ]

        return config

    def configure_generic_priorities(self, config):
        """Configuration générique"""
        print("\nConfiguration GENERIQUE appliquée...")

        config["priority_rules"]["urgent"]["keywords"] = [
            "urgent", "emergency", "critique", "problème", "panne", "incident"
        ]

        config["priority_rules"]["high"]["keywords"] = [
            "important", "client", "demande", "nouveau", "commande", "projet"
        ]

        config["priority_rules"]["medium"]["keywords"] = [
            "information", "question", "suivi", "confirmation", "facture"
        ]

        config["priority_rules"]["low"]["keywords"] = [
            "newsletter", "promotion", "marketing", "spam", "pub"
        ]

        return config

    def add_custom_keywords(self, config):
        """Ajouter des mots-clés personnalisés"""
        print("\n--- MOTS-CLES PERSONNALISES ---")

        for priority in ["urgent", "high", "medium", "low"]:
            print(f"\nMots-clés pour priorité {priority.upper()}:")
            print("(séparer par des virgules, laisser vide pour passer)")
            keywords = input(f"{priority.upper()}: ").strip()

            if keywords:
                new_keywords = [k.strip().lower() for k in keywords.split(",")]
                config["priority_rules"][priority]["keywords"].extend(new_keywords)

        return config

    def configure_special_rules(self, config):
        """Configurer les règles spéciales"""
        print("\n--- REGLES SPECIALES ---")

        # Clients VIP
        print("\nEmails de clients VIP (domaines ou adresses):")
        print("Ex: @entreprise-importante.com, pdg@client.fr")
        vip = input("Clients VIP: ").strip()
        if vip:
            config["special_rules"]["vip_clients"] = [v.strip() for v in vip.split(",")]

        # Expéditeurs bloqués
        print("\nExpéditeurs à bloquer/marquer comme spam:")
        blocked = input("Expéditeurs bloqués: ").strip()
        if blocked:
            config["special_rules"]["blocked_senders"] = [b.strip() for b in blocked.split(",")]

        return config

    def configure_business_hours(self, config):
        """Configurer les horaires de travail"""
        print("\n--- HORAIRES DE TRAVAIL ---")

        start = input("Heure de début (HH:MM, ex: 09:00): ").strip()
        if start:
            config["business_hours"]["start"] = start

        end = input("Heure de fin (HH:MM, ex: 18:00): ").strip()
        if end:
            config["business_hours"]["end"] = end

        print("\nPriorité des emails reçus hors horaires:")
        print("1. Normale (selon contenu)")
        print("2. Basse (sauf urgences)")
        choice = input("Choix (1-2): ").strip()
        if choice == "2":
            config["business_hours"]["weekend_priority"] = "low"

        return config

    def save_config(self, config):
        """Sauvegarder la configuration"""
        config["created_at"] = datetime.now().isoformat()
        config["version"] = "1.0"

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"\nConfiguration sauvegardée: {self.config_file}")

    def load_config(self):
        """Charger la configuration existante"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.default_config

    def display_config_summary(self, config):
        """Afficher un résumé de la configuration"""
        print("\n--- RESUME DE LA CONFIGURATION ---")
        print(f"Entreprise: {config['company_info']['name']}")
        print(f"Secteur: {config['company_info']['industry']}")
        print(f"Volume emails/jour: {config['company_info']['email_volume']}")

        print("\nMots-clés par priorité:")
        for priority, rules in config["priority_rules"].items():
            keywords = rules["keywords"][:5]  # Top 5
            print(f"  {priority.upper()}: {', '.join(keywords)}")

if __name__ == "__main__":
    questionnaire = BusinessQuestionnaire()
    config = questionnaire.run_questionnaire()
    questionnaire.display_config_summary(config)