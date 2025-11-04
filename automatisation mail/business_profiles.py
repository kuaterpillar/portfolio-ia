"""
Profils d'entreprise prédéfinis pour différents secteurs d'activité
Permet un déploiement rapide avec des configurations optimisées
"""

import json
import os
from datetime import datetime

class BusinessProfiles:
    def __init__(self):
        self.profiles = self.get_predefined_profiles()

    def get_predefined_profiles(self):
        """Profils prédéfinis par secteur d'activité"""
        return {
            "conciergerie": {
                "name": "Conciergerie / Services",
                "description": "Services de conciergerie, gestion immobilière, services aux particuliers",
                "config": {
                    "company_info": {
                        "industry": "conciergerie",
                        "typical_volume": "100-500 emails/jour",
                        "response_time_critical": "15 minutes"
                    },
                    "priority_rules": {
                        "urgent": {
                            "keywords": [
                                "urgent", "urgence", "emergency", "panne", "broken", "ne fonctionne pas",
                                "réclamation", "plainte", "problème grave", "incident", "sécurité",
                                "fuite", "coupure", "plus d'eau", "plus d'électricité", "ascenseur",
                                "chauffage", "climatisation", "serrure", "clé", "cambriolage",
                                "accident", "blessé", "ambulance", "pompiers", "police"
                            ],
                            "senders": ["@maintenance.com", "@security.", "@emergency."],
                            "subjects": ["URGENT", "EMERGENCY", "PANNE", "INCIDENT"],
                            "response_time": "15 minutes",
                            "escalation": "Responsable technique + Direction"
                        },
                        "high": {
                            "keywords": [
                                "réservation", "booking", "check-in", "check-out", "arrivée",
                                "nouveau client", "demande", "rdv", "rendez-vous", "maintenance",
                                "réparation", "intervention", "livraison", "colis", "courrier",
                                "nettoyage", "ménage", "client vip", "propriétaire"
                            ],
                            "senders": ["@booking.", "@reservation.", "@client-vip."],
                            "subjects": ["RESERVATION", "RDV", "NOUVEAU CLIENT"],
                            "response_time": "2 heures",
                            "escalation": "Responsable clientèle"
                        },
                        "medium": {
                            "keywords": [
                                "confirmation", "information", "question", "renseignement",
                                "facture", "paiement", "devis", "planning", "horaires",
                                "disponibilité", "tarif", "prix", "service", "prestation"
                            ],
                            "response_time": "24 heures",
                            "escalation": "Standard"
                        },
                        "low": {
                            "keywords": [
                                "newsletter", "promo", "promotion", "marketing", "publicité",
                                "offre", "catalogue", "brochure", "spam", "unsubscribe",
                                "formation", "congrès", "événement"
                            ],
                            "response_time": "48 heures ou plus",
                            "auto_action": "Archivage automatique possible"
                        }
                    },
                    "special_rules": {
                        "vip_clients": ["@syndic.", "@proprietaire-principal.", "@gestion-patrimoine."],
                        "always_urgent": ["pompiers", "police", "samu", "@emergency.", "@urgence."],
                        "business_hours_override": ["panne", "urgence", "sécurité"],
                        "auto_escalate": ["réclamation grave", "incident sécurité"]
                    },
                    "business_hours": {
                        "start": "07:00",
                        "end": "20:00",
                        "weekend_service": True,
                        "emergency_24_7": True
                    }
                }
            },

            "ecommerce": {
                "name": "E-commerce",
                "description": "Boutiques en ligne, vente à distance, marketplaces",
                "config": {
                    "company_info": {
                        "industry": "ecommerce",
                        "typical_volume": "200-1000 emails/jour",
                        "response_time_critical": "1 heure"
                    },
                    "priority_rules": {
                        "urgent": {
                            "keywords": [
                                "fraude", "fraud", "chargeback", "dispute", "réclamation grave",
                                "retour urgent", "problème paiement", "carte bloquée", "commande annulée",
                                "livraison manquée", "produit défectueux", "remboursement urgent",
                                "client mécontent", "avis négatif", "menace juridique"
                            ],
                            "senders": ["@bank.", "@payment.", "@fraud.", "noreply@paypal"],
                            "subjects": ["FRAUDE", "CHARGEBACK", "URGENT", "RÉCLAMATION"],
                            "response_time": "1 heure",
                            "escalation": "Service client + Direction"
                        },
                        "high": {
                            "keywords": [
                                "nouvelle commande", "paiement", "livraison", "expédition", "stock",
                                "client vip", "partenaire", "fournisseur", "marketplace",
                                "commande importante", "client professionnel", "b2b"
                            ],
                            "senders": ["@stripe.", "@paypal.", "@ups.", "@dhl.", "@amazon."],
                            "subjects": ["COMMANDE", "PAIEMENT", "LIVRAISON"],
                            "response_time": "4 heures",
                            "escalation": "Service commercial"
                        },
                        "medium": {
                            "keywords": [
                                "question produit", "disponibilité", "délai", "suivi commande",
                                "facture", "garantie", "sav", "retour", "échange",
                                "guide utilisation", "compatibilité"
                            ],
                            "response_time": "24 heures",
                            "escalation": "SAV standard"
                        },
                        "low": {
                            "keywords": [
                                "newsletter", "catalogue", "promotion", "code promo",
                                "enquête satisfaction", "marketing", "pub", "partenariat",
                                "affiliation", "test produit"
                            ],
                            "response_time": "48-72 heures",
                            "auto_action": "Traitement automatique"
                        }
                    },
                    "special_rules": {
                        "vip_clients": ["@entreprise.", "@corporate.", "@b2b."],
                        "fraud_keywords": ["fraude", "suspicious", "chargeback"],
                        "auto_process": ["confirmation commande", "expédition"],
                        "inventory_alerts": ["stock", "rupture", "approvisionnement"]
                    }
                }
            },

            "healthcare": {
                "name": "Santé / Médical",
                "description": "Cabinets médicaux, cliniques, laboratoires",
                "config": {
                    "company_info": {
                        "industry": "healthcare",
                        "typical_volume": "50-200 emails/jour",
                        "response_time_critical": "30 minutes",
                        "confidentiality": "RGPD + Secret médical"
                    },
                    "priority_rules": {
                        "urgent": {
                            "keywords": [
                                "urgence", "emergency", "critique", "vital", "life-threatening",
                                "ambulance", "samu", "hospitalisation", "accident", "chute",
                                "malaise", "douleur intense", "saignement", "fracture",
                                "urgence médicale", "patient critique"
                            ],
                            "response_time": "Immédiat",
                            "escalation": "Médecin de garde"
                        },
                        "high": {
                            "keywords": [
                                "rendez-vous", "consultation", "prescription", "ordonnance",
                                "résultats", "analyses", "examens", "patient", "médecin",
                                "traitement", "médicament", "suivi médical", "pathologie"
                            ],
                            "response_time": "2 heures",
                            "escalation": "Secrétariat médical"
                        },
                        "medium": {
                            "keywords": [
                                "rappel", "information", "planning", "confirmation",
                                "mutuelle", "sécurité sociale", "facturation",
                                "certificat", "arrêt travail"
                            ],
                            "response_time": "24 heures"
                        },
                        "low": {
                            "keywords": [
                                "newsletter médicale", "formation", "congrès",
                                "information générale", "prévention", "campagne santé"
                            ],
                            "response_time": "72 heures"
                        }
                    },
                    "special_rules": {
                        "medical_confidentiality": True,
                        "emergency_contacts": ["samu", "pompiers", "police"],
                        "patient_priority": ["@patient-vip.", "pathologie lourde"],
                        "legal_compliance": ["RGPD", "Secret médical", "Ordre des médecins"]
                    }
                }
            },

            "finance": {
                "name": "Finance / Banque",
                "description": "Banques, assurances, services financiers",
                "config": {
                    "company_info": {
                        "industry": "finance",
                        "typical_volume": "300-800 emails/jour",
                        "response_time_critical": "30 minutes",
                        "security_level": "Maximum"
                    },
                    "priority_rules": {
                        "urgent": {
                            "keywords": [
                                "fraude", "fraud", "sécurité", "security", "blocage compte",
                                "transaction suspecte", "incident sécurité", "piratage",
                                "phishing", "alerte", "urgent", "breach", "cyberattaque",
                                "compliance", "audit urgent", "régulateur"
                            ],
                            "response_time": "15 minutes",
                            "escalation": "Sécurité + Compliance"
                        },
                        "high": {
                            "keywords": [
                                "crédit", "prêt", "virement", "paiement", "découvert",
                                "client important", "investissement", "patrimoine",
                                "private banking", "entreprise", "professionnel"
                            ],
                            "response_time": "2 heures",
                            "escalation": "Conseiller client"
                        },
                        "medium": {
                            "keywords": [
                                "information compte", "solde", "relevé", "carte bancaire",
                                "assurance", "épargne", "placement", "conseil"
                            ],
                            "response_time": "24 heures"
                        },
                        "low": {
                            "keywords": [
                                "newsletter", "produit commercial", "promotion",
                                "enquête satisfaction", "marketing", "événement"
                            ],
                            "response_time": "48 heures"
                        }
                    },
                    "special_rules": {
                        "security_alerts": ["fraude", "suspicious", "blocked"],
                        "vip_clients": ["private banking", "@corporate.", "@enterprise."],
                        "regulatory_compliance": ["AMF", "ACPR", "BCE"],
                        "encryption_required": True
                    }
                }
            },

            "real_estate": {
                "name": "Immobilier",
                "description": "Agences immobilières, promoteurs, syndics",
                "config": {
                    "priority_rules": {
                        "urgent": {
                            "keywords": [
                                "sinistre", "dégât des eaux", "incendie", "cambriolage",
                                "urgence technique", "ascenseur en panne", "chauffage",
                                "fuite", "coupure", "sécurité"
                            ]
                        },
                        "high": {
                            "keywords": [
                                "vente", "achat", "signature", "compromis", "visite",
                                "client acheteur", "mandat", "estimation", "négociation"
                            ]
                        }
                    }
                }
            },

            "tech": {
                "name": "Tech / IT",
                "description": "Entreprises technologiques, services IT",
                "config": {
                    "priority_rules": {
                        "urgent": {
                            "keywords": [
                                "production down", "server crash", "security breach",
                                "outage", "critical bug", "data loss", "hack",
                                "system failure", "urgent fix needed"
                            ]
                        },
                        "high": {
                            "keywords": [
                                "bug report", "feature request", "client complaint",
                                "deployment", "release", "integration", "api issue"
                            ]
                        }
                    }
                }
            }
        }

    def get_profile(self, profile_name):
        """Récupérer un profil spécifique"""
        return self.profiles.get(profile_name, {})

    def list_profiles(self):
        """Lister tous les profils disponibles"""
        profiles_list = []
        for key, profile in self.profiles.items():
            profiles_list.append({
                "key": key,
                "name": profile["name"],
                "description": profile["description"]
            })
        return profiles_list

    def create_config_from_profile(self, profile_name, company_name="", customizations=None):
        """Créer une configuration complète à partir d'un profil"""
        profile = self.get_profile(profile_name)
        if not profile:
            raise ValueError(f"Profil '{profile_name}' non trouvé")

        # Configuration de base
        config = {
            "company_info": {
                "name": company_name,
                "industry": profile_name,
                "profile_used": profile["name"],
                "size": "",
                "email_volume": profile["config"]["company_info"].get("typical_volume", "")
            },
            "priority_rules": profile["config"]["priority_rules"],
            "business_hours": profile["config"].get("business_hours", {
                "start": "09:00",
                "end": "18:00",
                "timezone": "Europe/Paris"
            }),
            "special_rules": profile["config"].get("special_rules", {}),
            "created_at": datetime.now().isoformat(),
            "version": "1.0",
            "profile_source": profile_name
        }

        # Appliquer les personnalisations
        if customizations:
            config = self.apply_customizations(config, customizations)

        return config

    def apply_customizations(self, config, customizations):
        """Appliquer des personnalisations à une configuration"""
        for key, value in customizations.items():
            if key in config:
                if isinstance(config[key], dict) and isinstance(value, dict):
                    config[key].update(value)
                else:
                    config[key] = value
        return config

    def save_profile_config(self, profile_name, company_name, filename=None, customizations=None):
        """Sauvegarder une configuration basée sur un profil"""
        config = self.create_config_from_profile(profile_name, company_name, customizations)

        if not filename:
            filename = f"config_{profile_name}_{company_name.lower().replace(' ', '_')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        return filename, config

    def export_all_profiles(self, output_dir="profiles_export"):
        """Exporter tous les profils pour documentation"""
        import os
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        exported_files = []

        for profile_key, profile_data in self.profiles.items():
            filename = os.path.join(output_dir, f"profile_{profile_key}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            exported_files.append(filename)

        return exported_files

    def compare_profiles(self, profile1, profile2):
        """Comparer deux profils"""
        p1 = self.get_profile(profile1)
        p2 = self.get_profile(profile2)

        if not p1 or not p2:
            return {"error": "Un ou plusieurs profils non trouvés"}

        comparison = {
            "profiles": {
                "profile1": {"name": profile1, "title": p1["name"]},
                "profile2": {"name": profile2, "title": p2["name"]}
            },
            "differences": {
                "urgent_keywords": {
                    "profile1": p1["config"]["priority_rules"]["urgent"]["keywords"][:10],
                    "profile2": p2["config"]["priority_rules"]["urgent"]["keywords"][:10]
                },
                "response_times": {
                    "profile1": p1["config"]["priority_rules"]["urgent"].get("response_time", "Non défini"),
                    "profile2": p2["config"]["priority_rules"]["urgent"].get("response_time", "Non défini")
                }
            }
        }

        return comparison

def demo_profiles():
    """Démonstration des profils d'entreprise"""
    profiles = BusinessProfiles()

    print("="*60)
    print(" PROFILS D'ENTREPRISE DISPONIBLES")
    print("="*60)

    for profile_info in profiles.list_profiles():
        print(f"\n{profile_info['key'].upper()}: {profile_info['name']}")
        print(f"  Description: {profile_info['description']}")

        profile = profiles.get_profile(profile_info['key'])
        if profile:
            urgent_keywords = profile["config"]["priority_rules"]["urgent"]["keywords"][:5]
            print(f"  Mots-clés urgents: {', '.join(urgent_keywords)}...")

    # Test de création de configuration
    print("\n" + "="*60)
    print(" TEST - CREATION CONFIGURATION CONCIERGERIE")
    print("="*60)

    config = profiles.create_config_from_profile("conciergerie", "Hotel Paradise")
    print(f"Configuration créée pour: {config['company_info']['name']}")
    print(f"Secteur: {config['company_info']['industry']}")
    print(f"Nombre de mots-clés urgents: {len(config['priority_rules']['urgent']['keywords'])}")

if __name__ == "__main__":
    demo_profiles()