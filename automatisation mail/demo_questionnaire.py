"""
Démonstration du questionnaire de configuration avec données d'exemple
"""

from business_questionnaire import BusinessQuestionnaire
import json

def demo_configuration_conciergerie():
    """Démonstration pour une entreprise de conciergerie"""
    print("="*60)
    print(" DEMO QUESTIONNAIRE - ENTREPRISE DE CONCIERGERIE")
    print("="*60)

    questionnaire = BusinessQuestionnaire()
    config = questionnaire.get_default_config()

    # Simulation des réponses pour une conciergerie
    print("\n1. INFORMATIONS ENTREPRISE")
    print("Nom de l'entreprise: Hotel Paradise")
    print("Secteur: 1. Conciergerie/Services")
    print("Taille: 2. PME (10-249 employés)")
    print("Volume emails/jour: 300")

    config["company_info"]["name"] = "Hotel Paradise"
    config["company_info"]["industry"] = "conciergerie"
    config["company_info"]["size"] = "pme"
    config["company_info"]["email_volume"] = "300"

    # Configuration automatique pour conciergerie
    print("\n2. CONFIGURATION PRIORITES (Auto-détection secteur)")
    config = questionnaire.configure_conciergerie_priorities(config)

    # Règles spéciales
    print("\n3. REGLES SPECIALES")
    print("Clients VIP: @syndic-principal.fr, @proprietaire-vip.com")
    print("Expéditeurs bloqués: @spam.com, @marketing-agressif.fr")

    config["special_rules"]["vip_clients"] = ["@syndic-principal.fr", "@proprietaire-vip.com"]
    config["special_rules"]["blocked_senders"] = ["@spam.com", "@marketing-agressif.fr"]

    # Horaires
    print("\n4. HORAIRES DE TRAVAIL")
    print("Début: 07:00")
    print("Fin: 20:00")

    config["business_hours"]["start"] = "07:00"
    config["business_hours"]["end"] = "20:00"

    # Sauvegarde
    questionnaire.save_config(config)

    print("\n" + "="*60)
    print(" CONFIGURATION TERMINEE !")
    print("="*60)

    return config

def demo_configuration_ecommerce():
    """Démonstration pour un e-commerce"""
    print("\n" + "="*60)
    print(" DEMO QUESTIONNAIRE - E-COMMERCE")
    print("="*60)

    questionnaire = BusinessQuestionnaire()
    config = questionnaire.get_default_config()

    # Simulation des réponses pour e-commerce
    print("\n1. INFORMATIONS ENTREPRISE")
    print("Nom de l'entreprise: TechStore Online")
    print("Secteur: 2. E-commerce")
    print("Taille: 2. PME (10-249 employés)")
    print("Volume emails/jour: 800")

    config["company_info"]["name"] = "TechStore Online"
    config["company_info"]["industry"] = "ecommerce"
    config["company_info"]["size"] = "pme"
    config["company_info"]["email_volume"] = "800"

    # Configuration automatique pour e-commerce
    print("\n2. CONFIGURATION PRIORITES (Auto-détection secteur)")
    config = questionnaire.configure_ecommerce_priorities(config)

    # Règles spéciales
    print("\n3. REGLES SPECIALES")
    print("Clients VIP: @entreprise-corporate.fr, @gros-client.com")
    print("Expéditeurs bloqués: @concurrent.com, @phishing.org")

    config["special_rules"]["vip_clients"] = ["@entreprise-corporate.fr", "@gros-client.com"]
    config["special_rules"]["blocked_senders"] = ["@concurrent.com", "@phishing.org"]

    # Horaires
    print("\n4. HORAIRES DE TRAVAIL")
    print("Début: 08:00")
    print("Fin: 19:00")

    config["business_hours"]["start"] = "08:00"
    config["business_hours"]["end"] = "19:00"

    # Sauvegarde avec nom différent
    config_file = "ecommerce_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"\nConfiguration E-commerce sauvée: {config_file}")

    return config

def compare_configurations():
    """Comparer les deux configurations créées"""
    print("\n" + "="*60)
    print(" COMPARAISON DES CONFIGURATIONS")
    print("="*60)

    # Charger les configurations
    try:
        with open('business_config.json', 'r', encoding='utf-8') as f:
            config_conciergerie = json.load(f)
    except:
        print("Configuration conciergerie non trouvée")
        return

    try:
        with open('ecommerce_config.json', 'r', encoding='utf-8') as f:
            config_ecommerce = json.load(f)
    except:
        print("Configuration e-commerce non trouvée")
        return

    print(f"\nCONCIERGERIE ({config_conciergerie['company_info']['name']}):")
    print(f"  Volume: {config_conciergerie['company_info']['email_volume']} emails/jour")
    print(f"  Horaires: {config_conciergerie['business_hours']['start']} - {config_conciergerie['business_hours']['end']}")

    urgent_keywords_c = config_conciergerie['priority_rules']['urgent']['keywords'][:5]
    print(f"  Mots-clés urgents: {', '.join(urgent_keywords_c)}...")
    print(f"  Total mots-clés urgents: {len(config_conciergerie['priority_rules']['urgent']['keywords'])}")

    print(f"\nE-COMMERCE ({config_ecommerce['company_info']['name']}):")
    print(f"  Volume: {config_ecommerce['company_info']['email_volume']} emails/jour")
    print(f"  Horaires: {config_ecommerce['business_hours']['start']} - {config_ecommerce['business_hours']['end']}")

    urgent_keywords_e = config_ecommerce['priority_rules']['urgent']['keywords'][:5]
    print(f"  Mots-clés urgents: {', '.join(urgent_keywords_e)}...")
    print(f"  Total mots-clés urgents: {len(config_ecommerce['priority_rules']['urgent']['keywords'])}")

    # Différences clés
    print(f"\nDIFFERENCES CLES:")
    print(f"  Conciergerie priorise: pannes, urgences techniques, réclamations")
    print(f"  E-commerce priorise: fraudes, chargebacks, problèmes paiement")

def test_configurations():
    """Tester les deux configurations avec des emails d'exemple"""
    print("\n" + "="*60)
    print(" TEST DES CONFIGURATIONS")
    print("="*60)

    from adaptive_classifier import AdaptiveEmailClassifier

    # Emails de test
    test_emails = [
        ("urgent@client.com", "URGENT - Panne ascenseur", "L'ascenseur est en panne depuis 2h"),
        ("fraud@bank.com", "Transaction suspecte", "Alerte fraude détectée sur votre compte"),
        ("client@hotel.fr", "Réservation weekend", "Je souhaite réserver pour ce weekend"),
        ("customer@shop.com", "Commande non reçue", "Ma commande n'est toujours pas arrivée"),
        ("newsletter@promo.com", "Offres spéciales", "Découvrez nos promotions du mois")
    ]

    print("\nTEST CONFIGURATION CONCIERGERIE:")
    try:
        classifier_c = AdaptiveEmailClassifier("business_config.json")
        for sender, subject, body in test_emails:
            priority_num, priority_label = classifier_c.classify_email_priority(subject, sender, body)
            print(f"  '{subject}' → {priority_label}")
        classifier_c.close()
    except Exception as e:
        print(f"  Erreur: {e}")

    print("\nTEST CONFIGURATION E-COMMERCE:")
    try:
        classifier_e = AdaptiveEmailClassifier("ecommerce_config.json")
        for sender, subject, body in test_emails:
            priority_num, priority_label = classifier_e.classify_email_priority(subject, sender, body)
            print(f"  '{subject}' → {priority_label}")
        classifier_e.close()
    except Exception as e:
        print(f"  Erreur: {e}")

def show_questionnaire_process():
    """Montrer le processus complet du questionnaire"""
    print("DEMONSTRATION COMPLETE DU QUESTIONNAIRE DE CONFIGURATION")
    print("=" * 70)

    print("""
ETAPES DU QUESTIONNAIRE INTERACTIF:

1. INFORMATIONS ENTREPRISE (1 min)
   - Nom de l'entreprise
   - Secteur d'activité (8 choix prédéfinis)
   - Taille (TPE/PME/Grande entreprise)
   - Volume d'emails quotidien

2. CONFIGURATION AUTOMATIQUE DES PRIORITES (2 min)
   - Détection automatique selon le secteur
   - Mots-clés spécialisés pré-configurés
   - Possibilité d'ajout de mots-clés personnalisés
   - Règles de priorité optimisées

3. REGLES SPECIALES (1 min)
   - Clients VIP (domaines ou emails)
   - Expéditeurs à bloquer
   - Escalades automatiques

4. HORAIRES DE TRAVAIL (1 min)
   - Heures de début/fin
   - Gestion hors horaires
   - Priorité weekend

5. VALIDATION ET TEST
   - Résumé de la configuration
   - Test avec emails d'exemple
   - Sauvegarde automatique

TOTAL: 5-10 minutes pour une configuration complète !
""")

if __name__ == "__main__":
    show_questionnaire_process()

    # Démonstrations
    config_conciergerie = demo_configuration_conciergerie()
    config_ecommerce = demo_configuration_ecommerce()

    # Comparaison
    compare_configurations()

    # Tests
    test_configurations()

    print("\n" + "="*60)
    print(" DEMONSTRATION TERMINEE")
    print("="*60)
    print("Configurations sauvées:")
    print("  - business_config.json (Conciergerie)")
    print("  - ecommerce_config.json (E-commerce)")
    print("\nPour utiliser l'interface graphique:")
    print("  python setup_wizard.py")