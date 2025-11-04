"""
Affichage de toutes les questions du questionnaire
"""

def afficher_questionnaire_complet():
    """Affiche toutes les questions du questionnaire"""

    print("="*80)
    print("           QUESTIONNAIRE COMPLET - TRI D'EMAILS INTELLIGENT")
    print("="*80)
    print("Durée: 5-10 minutes | Personnalisation complète selon votre secteur")
    print()

    print("🔹 OBJECTIF:")
    print("   Configurer le système pour qu'il trie automatiquement vos emails")
    print("   selon les priorités RÉELLES de votre entreprise")
    print()

    # ÉTAPE 1
    print("━" * 60)
    print("📋 ÉTAPE 1/4: INFORMATIONS ENTREPRISE (1-2 minutes)")
    print("━" * 60)
    print()

    print("❓ QUESTION 1: Quel est le nom de votre entreprise ?")
    print("   💡 Exemples: 'Hotel Paradise', 'Cabinet Dr Martin', 'TechShop Online'")
    print("   📝 Réponse attendue: [Votre nom d'entreprise]")
    print()

    print("❓ QUESTION 2: Dans quel secteur d'activité travaillez-vous ?")
    print("   🏨 1. Conciergerie/Services aux particuliers")
    print("   🛒 2. E-commerce/Vente en ligne")
    print("   🏥 3. Santé/Médical")
    print("   💰 4. Finance/Banque/Assurance")
    print("   🏠 5. Immobilier")
    print("   💻 6. Tech/Informatique")
    print("   🎓 7. Éducation/Formation")
    print("   📊 8. Autre")
    print("   📝 Réponse attendue: [Numéro de 1 à 8]")
    print()

    print("❓ QUESTION 3: Quelle est la taille de votre entreprise ?")
    print("   👥 1. TPE (1-9 employés)")
    print("   🏢 2. PME (10-249 employés)")
    print("   🏬 3. Grande entreprise (250+ employés)")
    print("   📝 Réponse attendue: [1, 2 ou 3]")
    print()

    print("❓ QUESTION 4: Combien d'emails recevez-vous par jour ?")
    print("   💡 Exemples: 50, 200, 500, 1000...")
    print("   📝 Réponse attendue: [Nombre approximatif]")
    print()

    # ÉTAPE 2
    print("━" * 60)
    print("⚙️ ÉTAPE 2/4: CONFIGURATION AUTOMATIQUE (2-3 minutes)")
    print("━" * 60)
    print()

    print("🤖 Le système détecte automatiquement les mots-clés selon votre secteur:")
    print()

    print("🏨 SI CONCIERGERIE:")
    print("   🔴 URGENT: panne, urgence, fuite, ascenseur, réclamation, incident...")
    print("   🟡 HAUTE: réservation, nouveau client, maintenance, livraison...")
    print("   🔵 MOYENNE: confirmation, question, facture, planning...")
    print("   ⚪ BASSE: newsletter, promo, marketing, spam...")
    print()

    print("🛒 SI E-COMMERCE:")
    print("   🔴 URGENT: fraude, chargeback, réclamation grave, retour urgent...")
    print("   🟡 HAUTE: nouvelle commande, paiement, livraison, stock...")
    print("   🔵 MOYENNE: question produit, SAV, suivi commande...")
    print("   ⚪ BASSE: newsletter, catalogue, promotion...")
    print()

    print("🏥 SI SANTÉ:")
    print("   🔴 URGENT: urgence médicale, patient critique, ambulance...")
    print("   🟡 HAUTE: rdv, prescription, résultats, analyses...")
    print("   🔵 MOYENNE: rappel, confirmation, planning...")
    print("   ⚪ BASSE: formation, congrès, newsletter...")
    print()

    print("❓ QUESTION 5: Voulez-vous ajouter des mots-clés spécifiques ?")
    print("   💡 Exemple conciergerie: 'syndic', 'locataire', 'copropriété'")
    print("   💡 Exemple e-commerce: 'marketplace', 'amazon', 'leboncoin'")
    print("   💡 Exemple médical: 'ordonnance', 'mutuelle', 'urgence'")
    print("   📝 Réponse: [o/n] puis [mots-clés séparés par virgules]")
    print()

    # ÉTAPE 3
    print("━" * 60)
    print("⭐ ÉTAPE 3/4: RÈGLES SPÉCIALES (1-2 minutes)")
    print("━" * 60)
    print()

    print("❓ QUESTION 6: Avez-vous des clients VIP toujours prioritaires ?")
    print("   💡 Exemples:")
    print("      - @client-important.com (tout le domaine)")
    print("      - pdg@entreprise.fr (email spécifique)")
    print("      - @syndic-principal.fr (pour conciergerie)")
    print("      - @gros-client.com (pour e-commerce)")
    print("   📝 Réponse: [emails/domaines séparés par virgules ou vide]")
    print()

    print("❓ QUESTION 7: Y a-t-il des expéditeurs à bloquer/ignorer ?")
    print("   💡 Exemples:")
    print("      - @spam.com")
    print("      - @concurrent.fr")
    print("      - @marketing-agressif.com")
    print("   📝 Réponse: [emails/domaines séparés par virgules ou vide]")
    print()

    # ÉTAPE 4
    print("━" * 60)
    print("🕐 ÉTAPE 4/4: HORAIRES DE TRAVAIL (1 minute)")
    print("━" * 60)
    print()

    print("❓ QUESTION 8: À quelle heure commence votre journée ?")
    print("   💡 Exemples: 08:00, 09:00, 07:30...")
    print("   📝 Réponse: [HH:MM]")
    print()

    print("❓ QUESTION 9: À quelle heure finit votre journée ?")
    print("   💡 Exemples: 17:00, 18:00, 19:30...")
    print("   📝 Réponse: [HH:MM]")
    print()

    print("❓ QUESTION 10: Comment traiter les emails hors horaires ?")
    print("   1. Priorité normale (selon le contenu)")
    print("   2. Priorité réduite (sauf vraies urgences)")
    print("   📝 Réponse: [1 ou 2]")
    print()

    # RÉSULTAT
    print("━" * 60)
    print("✅ RÉSULTAT: CONFIGURATION PERSONNALISÉE")
    print("━" * 60)
    print()

    print("📊 Le système génère automatiquement:")
    print("   • Fichier de configuration business_config.json")
    print("   • Règles de tri adaptées à votre métier")
    print("   • Mots-clés spécialisés (20-50 par niveau)")
    print("   • Clients VIP reconnus automatiquement")
    print("   • Horaires de travail pris en compte")
    print()

    print("🧪 Test immédiat avec emails d'exemple")
    print("📈 Précision attendue: 70-90% dès l'installation")
    print()

    # EXEMPLES CONCRETS
    print("━" * 60)
    print("💡 EXEMPLES CONCRETS DE CLASSIFICATION")
    print("━" * 60)
    print()

    print("📧 Email: 'URGENT - Panne ascenseur étage 5'")
    print("   🏨 Conciergerie → 🔴 URGENT")
    print("   🛒 E-commerce → 🔵 MOYENNE")
    print("   🏥 Médical → 🔵 MOYENNE")
    print()

    print("📧 Email: 'Transaction suspecte détectée'")
    print("   🏨 Conciergerie → 🔵 MOYENNE")
    print("   🛒 E-commerce → 🔴 URGENT")
    print("   💰 Finance → 🔴 URGENT")
    print()

    print("📧 Email: 'Patient en détresse respiratoire'")
    print("   🏨 Conciergerie → 🔵 MOYENNE")
    print("   🛒 E-commerce → 🔵 MOYENNE")
    print("   🏥 Médical → 🔴 URGENT")
    print()

    print("📧 Email: 'Newsletter - Offres du mois'")
    print("   🏨 Tous secteurs → ⚪ BASSE")
    print()

    print("=" * 80)
    print("                    PRÊT À CONFIGURER ?")
    print("=" * 80)
    print()
    print("🚀 Pour démarrer la configuration:")
    print("   1. Interface graphique: python setup_wizard.py")
    print("   2. Version console: python questionnaire_interactif.py")
    print("   3. Configuration rapide: Choisir un profil prédéfini")
    print()
    print("⏱️ Durée totale: 5-10 minutes pour une solution sur-mesure")
    print("🎯 Résultat: Système de tri parfaitement adapté à votre entreprise")

def exemples_reponses_secteurs():
    """Exemples de réponses pour différents secteurs"""
    print("\n" + "="*60)
    print("📝 EXEMPLES DE RÉPONSES PAR SECTEUR")
    print("="*60)

    exemples = {
        "Conciergerie Hotel 4*": {
            "nom": "Hotel Paradise",
            "secteur": "1 (Conciergerie)",
            "taille": "2 (PME)",
            "volume": "300",
            "mots_urgent": "syndic, locataire, dégât, copropriété",
            "vip": "@syndic-principal.fr, @proprietaire-vip.com",
            "bloque": "@spam.com, @concurrent-hotel.fr",
            "debut": "07:00",
            "fin": "20:00",
            "hh": "2 (priorité réduite)"
        },
        "Boutique E-commerce": {
            "nom": "TechShop Online",
            "secteur": "2 (E-commerce)",
            "taille": "2 (PME)",
            "volume": "800",
            "mots_urgent": "marketplace, amazon, leboncoin, rupture",
            "vip": "@entreprise-corporate.fr, @gros-client.com",
            "bloque": "@concurrent.com, @phishing.org",
            "debut": "08:00",
            "fin": "19:00",
            "hh": "1 (priorité normale)"
        },
        "Cabinet Médical": {
            "nom": "Cabinet Dr Martin",
            "secteur": "3 (Santé)",
            "taille": "1 (TPE)",
            "volume": "80",
            "mots_urgent": "ordonnance, mutuelle, urgence, ambulance",
            "vip": "@hopital-partenaire.fr, @medecin-referent.fr",
            "bloque": "@pharma-marketing.com, @formation-spam.org",
            "debut": "08:30",
            "fin": "18:30",
            "hh": "2 (priorité réduite)"
        }
    }

    for entreprise, reponses in exemples.items():
        print(f"\n📋 EXEMPLE: {entreprise}")
        print("-" * 40)
        for cle, valeur in reponses.items():
            print(f"   {cle}: {valeur}")

if __name__ == "__main__":
    afficher_questionnaire_complet()
    exemples_reponses_secteurs()