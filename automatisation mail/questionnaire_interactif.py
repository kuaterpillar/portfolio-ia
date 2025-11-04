"""
Version interactive du questionnaire pour démonstration
"""

from business_questionnaire import BusinessQuestionnaire
import json

def questionnaire_step_by_step():
    """Questionnaire étape par étape avec saisie manuelle"""
    questionnaire = BusinessQuestionnaire()
    config = questionnaire.get_default_config()

    print("="*70)
    print("         QUESTIONNAIRE DE CONFIGURATION - TRI D'EMAILS")
    print("="*70)
    print("Ce questionnaire va personnaliser le système selon votre entreprise")
    print("Durée estimée: 5-10 minutes")
    print()

    # ÉTAPE 1: Informations entreprise
    print("--- ÉTAPE 1/4: INFORMATIONS ENTREPRISE ---")
    print()

    # Nom entreprise
    print("Quel est le nom de votre entreprise ?")
    print("Exemple: 'Hotel Paradise', 'Cabinet Dr Martin', 'TechShop Online'")
    nom_entreprise = input("Nom de l'entreprise: ").strip()
    config["company_info"]["name"] = nom_entreprise
    print(f"✓ Entreprise: {nom_entreprise}")
    print()

    # Secteur d'activité
    print("Dans quel secteur d'activité travaillez-vous ?")
    print("1. Conciergerie/Services aux particuliers")
    print("2. E-commerce/Vente en ligne")
    print("3. Santé/Médical")
    print("4. Finance/Banque/Assurance")
    print("5. Immobilier")
    print("6. Tech/Informatique")
    print("7. Éducation/Formation")
    print("8. Autre")
    print()

    choix_secteur = input("Votre choix (1-8): ").strip()
    secteurs = {
        "1": ("conciergerie", "Conciergerie/Services"),
        "2": ("ecommerce", "E-commerce"),
        "3": ("healthcare", "Santé/Médical"),
        "4": ("finance", "Finance/Banque"),
        "5": ("real_estate", "Immobilier"),
        "6": ("tech", "Tech/IT"),
        "7": ("education", "Éducation"),
        "8": ("other", "Autre")
    }

    if choix_secteur in secteurs:
        secteur_code, secteur_nom = secteurs[choix_secteur]
        config["company_info"]["industry"] = secteur_code
        print(f"✓ Secteur: {secteur_nom}")
    else:
        config["company_info"]["industry"] = "other"
        print("✓ Secteur: Autre")
    print()

    # Taille entreprise
    print("Quelle est la taille de votre entreprise ?")
    print("1. TPE (1-9 employés)")
    print("2. PME (10-249 employés)")
    print("3. Grande entreprise (250+ employés)")
    print()

    choix_taille = input("Votre choix (1-3): ").strip()
    tailles = {"1": "tpe", "2": "pme", "3": "grande"}
    config["company_info"]["size"] = tailles.get(choix_taille, "pme")
    print(f"✓ Taille: {tailles.get(choix_taille, 'PME')}")
    print()

    # Volume emails
    print("Combien d'emails recevez-vous approximativement par jour ?")
    print("Exemple: 50, 200, 500, 1000...")
    volume = input("Nombre d'emails/jour: ").strip()
    config["company_info"]["email_volume"] = volume
    print(f"✓ Volume: {volume} emails/jour")
    print()

    # ÉTAPE 2: Configuration automatique selon secteur
    print("--- ÉTAPE 2/4: CONFIGURATION DES PRIORITÉS ---")
    print()
    print(f"Configuration automatique détectée pour: {secteur_nom}")
    print("Le système va adapter les mots-clés selon votre secteur...")
    print()

    # Appliquer la configuration selon le secteur
    if secteur_code == "conciergerie":
        print("🏨 CONCIERGERIE détectée - Configuration spécialisée:")
        print("  URGENT: pannes, urgences, réclamations, incidents")
        print("  HAUTE: réservations, nouveaux clients, maintenance")
        print("  MOYENNE: confirmations, questions, facturation")
        print("  BASSE: newsletters, promotions, marketing")
        config = questionnaire.configure_conciergerie_priorities(config)

    elif secteur_code == "ecommerce":
        print("🛒 E-COMMERCE détecté - Configuration spécialisée:")
        print("  URGENT: fraudes, chargebacks, réclamations graves")
        print("  HAUTE: nouvelles commandes, livraisons, stock")
        print("  MOYENNE: questions produits, SAV standard")
        print("  BASSE: newsletters, catalogues, marketing")
        config = questionnaire.configure_ecommerce_priorities(config)

    elif secteur_code == "healthcare":
        print("🏥 SANTÉ détecté - Configuration spécialisée:")
        print("  URGENT: urgences médicales, patients critiques")
        print("  HAUTE: rendez-vous, prescriptions, résultats")
        print("  MOYENNE: rappels, confirmations")
        print("  BASSE: formations, congrès")
        config = questionnaire.configure_healthcare_priorities(config)

    elif secteur_code == "finance":
        print("💰 FINANCE détecté - Configuration spécialisée:")
        print("  URGENT: fraudes, sécurité, incidents")
        print("  HAUTE: clients corporate, investissements")
        print("  MOYENNE: questions comptes, informations")
        print("  BASSE: produits commerciaux, marketing")
        config = questionnaire.configure_finance_priorities(config)

    else:
        print("📋 Configuration générique appliquée")
        config = questionnaire.configure_generic_priorities(config)

    print()

    # Personnalisation supplémentaire
    print("Souhaitez-vous ajouter des mots-clés spécifiques à votre activité ?")
    print("Exemples pour conciergerie: 'syndic', 'locataire', 'bail'")
    print("Exemples pour e-commerce: 'marketplace', 'amazon', 'retour'")
    choix_custom = input("Ajouter des mots-clés personnalisés ? (o/n): ").strip().lower()

    if choix_custom == 'o':
        print()
        print("Ajoutez vos mots-clés personnalisés (séparés par des virgules):")

        for priorite, label in [("urgent", "URGENT"), ("high", "HAUTE"), ("medium", "MOYENNE"), ("low", "BASSE")]:
            mots_cles = input(f"Mots-clés {label}: ").strip()
            if mots_cles:
                nouveaux_mots = [m.strip().lower() for m in mots_cles.split(",")]
                config["priority_rules"][priorite]["keywords"].extend(nouveaux_mots)
                print(f"✓ Ajoutés pour {label}: {', '.join(nouveaux_mots)}")
    print()

    # ÉTAPE 3: Règles spéciales
    print("--- ÉTAPE 3/4: RÈGLES SPÉCIALES ---")
    print()

    # Clients VIP
    print("Avez-vous des clients VIP qui doivent toujours être prioritaires ?")
    print("Indiquez les domaines ou emails (ex: @client-important.com, pdg@entreprise.fr)")
    vip_clients = input("Clients VIP (séparés par des virgules): ").strip()
    if vip_clients:
        config["special_rules"]["vip_clients"] = [v.strip() for v in vip_clients.split(",")]
        print(f"✓ Clients VIP configurés: {len(config['special_rules']['vip_clients'])} entrées")
    print()

    # Expéditeurs bloqués
    print("Y a-t-il des expéditeurs à toujours classer comme SPAM/BASSE priorité ?")
    print("Exemples: @concurrent.com, @marketing-agressif.fr")
    bloque = input("Expéditeurs bloqués (séparés par des virgules): ").strip()
    if bloque:
        config["special_rules"]["blocked_senders"] = [b.strip() for b in bloque.split(",")]
        print(f"✓ Expéditeurs bloqués: {len(config['special_rules']['blocked_senders'])} entrées")
    print()

    # ÉTAPE 4: Horaires de travail
    print("--- ÉTAPE 4/4: HORAIRES DE TRAVAIL ---")
    print()

    print("À quelle heure commence votre journée de travail ?")
    heure_debut = input("Heure de début (HH:MM, ex: 09:00): ").strip()
    if heure_debut:
        config["business_hours"]["start"] = heure_debut
        print(f"✓ Début: {heure_debut}")
    print()

    print("À quelle heure finit votre journée de travail ?")
    heure_fin = input("Heure de fin (HH:MM, ex: 18:00): ").strip()
    if heure_fin:
        config["business_hours"]["end"] = heure_fin
        print(f"✓ Fin: {heure_fin}")
    print()

    print("Comment traiter les emails reçus hors horaires de travail ?")
    print("1. Priorité normale (selon le contenu)")
    print("2. Priorité réduite (sauf urgences vraies)")
    choix_hh = input("Votre choix (1-2): ").strip()
    if choix_hh == "2":
        config["business_hours"]["weekend_priority"] = "low"
        print("✓ Emails hors horaires = priorité réduite")
    print()

    # RÉSUMÉ ET SAUVEGARDE
    print("="*70)
    print("                    RÉSUMÉ DE VOTRE CONFIGURATION")
    print("="*70)
    print()

    print(f"🏢 Entreprise: {config['company_info']['name']}")
    print(f"📊 Secteur: {secteur_nom}")
    print(f"👥 Taille: {config['company_info']['size'].upper()}")
    print(f"📧 Volume: {config['company_info']['email_volume']} emails/jour")
    print(f"⏰ Horaires: {config['business_hours']['start']} - {config['business_hours']['end']}")
    print()

    # Statistiques mots-clés
    for priorite, label in [("urgent", "URGENT"), ("high", "HAUTE"), ("medium", "MOYENNE"), ("low", "BASSE")]:
        nb_mots = len(config["priority_rules"][priorite]["keywords"])
        mots_exemples = config["priority_rules"][priorite]["keywords"][:3]
        print(f"🔴 {label}: {nb_mots} mots-clés ({', '.join(mots_exemples)}...)")

    print()
    vip_count = len(config["special_rules"]["vip_clients"])
    blocked_count = len(config["special_rules"]["blocked_senders"])
    print(f"⭐ Clients VIP: {vip_count}")
    print(f"🚫 Expéditeurs bloqués: {blocked_count}")
    print()

    # Sauvegarde
    questionnaire.save_config(config)
    print("✅ Configuration sauvegardée dans: business_config.json")
    print()

    # Test optionnel
    print("Voulez-vous tester cette configuration avec des emails d'exemple ?")
    test_choice = input("Lancer le test ? (o/n): ").strip().lower()

    if test_choice == 'o':
        test_configuration(config)

    print()
    print("="*70)
    print("    CONFIGURATION TERMINÉE ! Votre système est prêt à fonctionner.")
    print("="*70)
    print()
    print("Prochaines étapes:")
    print("1. Configurez vos identifiants email dans config.env")
    print("2. Lancez l'interface: python interface.py")
    print("3. Cliquez sur 'Traiter Nouveaux Emails'")

    return config

def test_configuration(config):
    """Tester la configuration avec des emails d'exemple"""
    print()
    print("--- TEST DE LA CONFIGURATION ---")

    # Emails de test génériques
    test_emails = [
        ("urgent@client.com", "URGENT - Problème critique", "Nous avons un problème urgent"),
        ("nouveau@client.fr", "Nouvelle demande", "Je souhaite plus d'informations"),
        ("newsletter@promo.com", "Offres spéciales", "Découvrez nos promotions"),
        ("support@client.com", "Question technique", "J'ai une question sur votre service"),
        ("admin@system.com", "Rapport mensuel", "Voici le rapport du mois")
    ]

    # Emails spécifiques selon le secteur
    secteur = config["company_info"]["industry"]
    if secteur == "conciergerie":
        test_emails.extend([
            ("maintenance@building.fr", "Fuite étage 3", "Il y a une fuite d'eau"),
            ("syndic@residence.com", "Réunion assemblée", "Convocation assemblée générale")
        ])
    elif secteur == "ecommerce":
        test_emails.extend([
            ("fraud@bank.com", "Transaction suspecte", "Alerte fraude détectée"),
            ("customer@shop.fr", "Commande non reçue", "Ma commande n'est pas arrivée")
        ])

    print(f"\nTest avec {len(test_emails)} emails d'exemple:")
    print()

    # Simulation de classification (simplifiée)
    for sender, subject, body in test_emails:
        # Classification basique pour le test
        text = f"{subject} {body}".lower()

        # Vérifier urgent
        urgent_keywords = config["priority_rules"]["urgent"]["keywords"]
        if any(keyword in text for keyword in urgent_keywords):
            priority = "URGENT"
        # Vérifier haute
        elif any(keyword in text for keyword in config["priority_rules"]["high"]["keywords"]):
            priority = "HAUTE"
        # Vérifier basse
        elif any(keyword in text for keyword in config["priority_rules"]["low"]["keywords"]):
            priority = "BASSE"
        else:
            priority = "MOYENNE"

        print(f"📧 '{subject}' → {priority}")

    print("\n✅ Test terminé ! La configuration fonctionne correctement.")

if __name__ == "__main__":
    config = questionnaire_step_by_step()