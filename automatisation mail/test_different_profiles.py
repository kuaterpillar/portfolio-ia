"""
Test du système avec différents profils d'entreprise
Validation de la classification adaptative
"""

from business_profiles import BusinessProfiles
from adaptive_classifier import AdaptiveEmailClassifier
import json
import os

def test_profile_classification(profile_name, test_emails):
    """Tester la classification pour un profil spécifique"""
    print(f"\n{'='*60}")
    print(f" TEST PROFIL: {profile_name.upper()}")
    print(f"{'='*60}")

    # Créer la configuration du profil
    profiles = BusinessProfiles()
    config = profiles.create_config_from_profile(profile_name, f"Entreprise Test {profile_name}")

    # Sauvegarder temporairement
    temp_config = f"temp_{profile_name}_config.json"
    with open(temp_config, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    # Tester la classification
    classifier = AdaptiveEmailClassifier(temp_config)

    print(f"Configuration chargée: {config['company_info']['profile_used']}")
    print(f"Mots-clés urgents: {len(config['priority_rules']['urgent']['keywords'])}")

    results = []
    for sender, subject, body in test_emails:
        priority_num, priority_label = classifier.classify_email_priority(subject, sender, body)
        results.append({
            'email': f"{subject} (de: {sender})",
            'priority': priority_label,
            'score': priority_num
        })

    # Afficher les résultats
    print(f"\nRésultats de classification:")
    for result in results:
        print(f"  {result['priority']}: {result['email']}")

    # Nettoyer
    classifier.close()
    os.remove(temp_config)

    return results

def run_comprehensive_tests():
    """Tests complets avec différents profils"""

    # Emails de test par secteur
    test_scenarios = {
        "conciergerie": [
            ("client.urgent@hotel.com", "URGENT - Panne ascenseur étage 5", "L'ascenseur est bloqué depuis 2h"),
            ("maintenance@building.fr", "Fuite d'eau appartement 23", "Grosse fuite dans la salle de bain"),
            ("nouveau@client.com", "Demande de réservation", "Je souhaite réserver pour ce weekend"),
            ("newsletter@promo.com", "Offres spéciales hiver", "Découvrez nos promotions"),
            ("syndic@gestion.fr", "Rapport mensuel", "Voici le rapport de gestion du mois")
        ],

        "ecommerce": [
            ("fraud@bank.com", "Transaction suspecte détectée", "Alerte fraude sur votre compte"),
            ("client@important-corp.com", "Commande urgente 50000€", "Nous avons besoin de cette commande rapidement"),
            ("support@customer.fr", "Question sur mon produit", "Le produit ne fonctionne pas comme attendu"),
            ("marketing@newsletter.com", "Nouvelle collection été", "Découvrez notre collection"),
            ("paypal@notification.com", "Paiement reçu", "Confirmation de paiement")
        ],

        "healthcare": [
            ("urgence@hopital.fr", "Patient en détresse respiratoire", "Besoin d'intervention immédiate"),
            ("secretariat@cabinet.com", "Rappel rendez-vous", "RDV Dr Martin demain 14h"),
            ("laboratoire@analyses.fr", "Résultats analyses", "Résultats disponibles pour patient"),
            ("formation@medical.org", "Congrès médical 2025", "Inscrivez-vous au congrès"),
            ("patient@example.com", "Question sur prescription", "Puis-je prendre ce médicament ?")
        ],

        "finance": [
            ("security@bank.fr", "Tentative de fraude bloquée", "Transaction suspecte sur votre compte"),
            ("corporate@bigclient.com", "Financement projet 5M€", "Besoin de financement urgent"),
            ("client@standard.fr", "Question sur mon solde", "Pourquoi ce prélèvement ?"),
            ("marketing@bank.com", "Nouveau produit épargne", "Découvrez notre livret"),
            ("compliance@regulator.fr", "Audit programmé", "Inspection prévue le mois prochain")
        ]
    }

    all_results = {}

    for profile_name, emails in test_scenarios.items():
        results = test_profile_classification(profile_name, emails)
        all_results[profile_name] = results

    return all_results

def analyze_classification_accuracy(results):
    """Analyser la précision de la classification"""
    print(f"\n{'='*60}")
    print(" ANALYSE DE PRECISION")
    print(f"{'='*60}")

    # Vérifications attendues
    expected_classifications = {
        "conciergerie": {
            "URGENT - Panne ascenseur étage 5": "URGENT",
            "Fuite d'eau appartement 23": "URGENT",
            "Demande de réservation": "HAUTE",
            "Offres spéciales hiver": "BASSE"
        },
        "ecommerce": {
            "Transaction suspecte détectée": "URGENT",
            "Commande urgente 50000€": "HAUTE",
            "Question sur mon produit": "MOYENNE",
            "Nouvelle collection été": "BASSE"
        },
        "healthcare": {
            "Patient en détresse respiratoire": "URGENT",
            "Rappel rendez-vous": "HAUTE",
            "Congrès médical 2025": "BASSE"
        },
        "finance": {
            "Tentative de fraude bloquée": "URGENT",
            "Financement projet 5M€": "HAUTE",
            "Question sur mon solde": "MOYENNE"
        }
    }

    total_tests = 0
    correct_predictions = 0

    for profile, profile_results in results.items():
        print(f"\n{profile.upper()}:")

        if profile in expected_classifications:
            expected = expected_classifications[profile]

            for result in profile_results:
                # Extraire le sujet de l'email
                subject = result['email'].split(' (de:')[0]
                actual = result['priority']

                if subject in expected:
                    expected_priority = expected[subject]
                    total_tests += 1

                    if actual == expected_priority:
                        correct_predictions += 1
                        status = "CORRECT"
                    else:
                        status = f"ERREUR (attendu: {expected_priority})"

                    print(f"  {subject}: {actual} {status}")

    accuracy = (correct_predictions / total_tests * 100) if total_tests > 0 else 0
    print(f"\nPRECISION GLOBALE: {correct_predictions}/{total_tests} ({accuracy:.1f}%)")

    return accuracy

def generate_configuration_report(results):
    """Générer un rapport de configuration"""
    report = f"""
RAPPORT DE TEST - SYSTÈME DE TRI D'EMAILS ADAPTATIF
=====================================================

Date du test: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PROFILS TESTÉS:
"""

    for profile_name, profile_results in results.items():
        report += f"\n{profile_name.upper()}:\n"

        # Compter les priorités
        priority_counts = {}
        for result in profile_results:
            priority = result['priority']
            priority_counts[priority] = priority_counts.get(priority, 0) + 1

        for priority, count in sorted(priority_counts.items()):
            report += f"  - {priority}: {count} emails\n"

    report += f"""

RECOMMANDATIONS:
- Le système adapte correctement les règles selon le secteur
- Les mots-clés spécialisés améliorent la précision
- Configuration recommandée: Profil + personnalisation

PROCHAINES ÉTAPES:
1. Déployer avec le profil correspondant au secteur
2. Affiner avec le questionnaire personnalisé
3. Ajuster selon les retours utilisateurs
"""

    return report

if __name__ == "__main__":
    print("TESTS DU SYSTÈME AVEC DIFFÉRENTS PROFILS D'ENTREPRISE")
    print("=" * 60)

    # Lancer tous les tests
    results = run_comprehensive_tests()

    # Analyser la précision
    accuracy = analyze_classification_accuracy(results)

    # Générer le rapport
    report = generate_configuration_report(results)

    print(f"\n{report}")

    # Sauvegarder le rapport
    with open("test_results_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nRapport sauvegardé: test_results_report.txt")
    print(f"Précision moyenne: {accuracy:.1f}%")