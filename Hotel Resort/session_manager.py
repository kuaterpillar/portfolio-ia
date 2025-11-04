"""
Session Manager - Initialize and manage project memory
Run this script to:
- View current session state
- Initialize a new session with current project context
- Export session reports
- Archive old sessions
"""

import sys
import os
from src.core.session_memory import SessionMemory


def initialize_project_session():
    """Initialize session with current project state"""
    memory = SessionMemory()

    print("🔄 Initialisation de la mémoire de session...\n")

    # Record project decisions
    memory.add_decision(
        decision="Créer un agent IA auto-apprenant pour le concierge d'hôtel",
        reason="Permettre au bot de s'améliorer automatiquement au fil du temps en analysant les patterns de conversations réussies",
        impact="Le bot devient de plus en plus performant et personnalisé sans intervention manuelle"
    )

    memory.add_decision(
        decision="Utiliser WhatsApp comme canal de communication principal",
        reason="WhatsApp est le canal de messagerie le plus utilisé, familier pour les clients, et supporte les webhooks via Twilio",
        impact="Accessibilité maximale pour les clients, intégration facile avec l'API Twilio"
    )

    memory.add_decision(
        decision="Stocker les données dans SQLite local",
        reason="Projet en développement, SQLite suffit pour prototypage et permet une migration facile vers PostgreSQL plus tard",
        impact="Déploiement simple, pas de dépendance externe, migration facile"
    )

    memory.add_decision(
        decision="Séparer les recommandations dans un moteur dédié",
        reason="Les recommandations nécessitent une logique spécifique (météo, budget, proximité) qui polluerait l'agent IA principal",
        impact="Code plus modulaire, recommandations plus précises, facilité de maintenance"
    )

    # Record implemented features
    memory.add_feature_implemented(
        feature_name="Agent IA auto-apprenant",
        description="Agent conversationnel avec mémoire persistante, apprentissage des patterns, tracking de performance, et personnalisation par client",
        files_involved=[
            "src/core/ai_agent.py",
            "data/agent_memory.db"
        ]
    )

    memory.add_feature_implemented(
        feature_name="Système de réservation",
        description="Gestion complète des réservations avec vérification de disponibilité, création/confirmation/annulation, et historique client",
        files_involved=[
            "src/core/booking_system.py",
            "data/bookings.db"
        ]
    )

    memory.add_feature_implemented(
        feature_name="Moteur de recommandations contextuelles",
        description="Recommandations de restaurants, activités et services basées sur budget, météo, préférences client, et proximité",
        files_involved=[
            "src/core/recommendation_engine.py"
        ]
    )

    memory.add_feature_implemented(
        feature_name="Intégration WhatsApp via Twilio",
        description="Handler complet pour WhatsApp avec webhooks, envoi de messages, templates, et messages d'accueil/sondages automatisés",
        files_involved=[
            "src/integrations/whatsapp_handler.py"
        ]
    )

    memory.add_feature_implemented(
        feature_name="Orchestrateur principal",
        description="Application principale qui coordonne AI, recommandations, réservations et WhatsApp avec détection d'intentions",
        files_involved=[
            "main.py"
        ]
    )

    memory.add_feature_implemented(
        feature_name="Système de mémoire de session",
        description="Sauvegarde automatique du contexte de projet, conversations, décisions et TODOs entre les sessions",
        files_involved=[
            "src/core/session_memory.py",
            "session_manager.py"
        ]
    )

    # Record files modified
    files_created = [
        ("main.py", "Point d'entrée principal avec orchestration"),
        ("src/core/ai_agent.py", "Agent IA avec apprentissage et mémoire client"),
        ("src/core/booking_system.py", "Système de réservation complet"),
        ("src/core/recommendation_engine.py", "Moteur de recommandations contextuelles"),
        ("src/integrations/whatsapp_handler.py", "Intégration WhatsApp/Twilio"),
        ("src/core/session_memory.py", "Système de mémoire de session"),
        ("requirements.txt", "Dépendances Python"),
        (".env.example", "Template de configuration"),
        ("README.md", "Documentation complète du projet"),
        ("test_bot.py", "Tests automatisés"),
        ("session_manager.py", "Gestionnaire de mémoire de session")
    ]

    for file_path, description in files_created:
        memory.add_file_modified(file_path, description)

    # Add current TODOs
    memory.add_todo(
        "Implémenter l'extraction automatique de dates dans les messages de réservation",
        status="pending",
        priority="high"
    )

    memory.add_todo(
        "Ajouter plus de restaurants et activités dans la base de données",
        status="pending",
        priority="medium"
    )

    memory.add_todo(
        "Créer un dashboard web pour visualiser les métriques de performance",
        status="pending",
        priority="medium"
    )

    memory.add_todo(
        "Implémenter la logique de pattern reinforcement dans learn_from_feedback",
        status="pending",
        priority="high"
    )

    memory.add_todo(
        "Ajouter support pour les messages vocaux WhatsApp",
        status="pending",
        priority="low"
    )

    memory.add_todo(
        "Créer des tests unitaires pour chaque module",
        status="pending",
        priority="medium"
    )

    # Add configurations
    memory.set_configuration("openai_model", "gpt-4o")
    memory.set_configuration("whatsapp_provider", "Twilio")
    memory.set_configuration("database", "SQLite")
    memory.set_configuration("default_language", "français")

    # Add notes
    memory.add_note(
        "L'agent utilise GPT-4o pour des réponses de qualité maximale. Peut être changé vers gpt-4o-mini pour réduire les coûts.",
        category="configuration"
    )

    memory.add_note(
        "La base de données de recommandations est actuellement statique. Prévoir une interface admin pour la gérer dynamiquement.",
        category="amélioration"
    )

    memory.add_note(
        "Le système de learning est en place mais la logique de pattern reinforcement reste à implémenter complètement.",
        category="développement"
    )

    memory.add_note(
        "Pour la production, penser à configurer ngrok ou un serveur avec HTTPS pour les webhooks Twilio.",
        category="déploiement"
    )

    print("✅ Session initialisée avec succès!\n")
    return memory


def main():
    """Main CLI for session manager"""
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════╗
║           SESSION MANAGER - Hotel Concierge AI              ║
╚══════════════════════════════════════════════════════════════╝

Usage: python session_manager.py [command]

Commandes:
  init       - Initialiser une nouvelle session avec le contexte actuel
  summary    - Afficher le résumé de la session actuelle
  export     - Exporter le rapport de session en Markdown
  archive    - Archiver la session actuelle et en démarrer une nouvelle
  context    - Afficher le contexte pour l'IA (résumé court)

Exemples:
  python session_manager.py init
  python session_manager.py summary
  python session_manager.py export
""")
        return

    command = sys.argv[1].lower()

    if command == "init":
        memory = initialize_project_session()
        print("\n📊 Résumé de la session initialisée:\n")
        print(memory.get_session_summary())

    elif command == "summary":
        memory = SessionMemory()
        print(memory.get_session_summary())

    elif command == "export":
        memory = SessionMemory()
        output_file = memory.export_session_report()
        print(f"\n✅ Rapport exporté: {output_file}")

    elif command == "archive":
        memory = SessionMemory()
        memory.archive_session()
        print("\n✅ Session archivée et nouvelle session créée")

    elif command == "context":
        memory = SessionMemory()
        print(memory.get_context_for_ai())

    else:
        print(f"❌ Commande inconnue: {command}")
        print("Utilisez: init, summary, export, archive, ou context")


if __name__ == "__main__":
    main()
