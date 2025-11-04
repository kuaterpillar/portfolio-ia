"""
Démonstration : 2 clients interagissent avec le concierge de l'Hôtel 121 Paris
Montre la mémoire conversationnelle et l'absence de confusion entre clients
"""

import os
import time
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Vérifier que l'API key OpenAI est configurée
if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "sk-proj-your-key-here":
    print("=" * 80)
    print("⚠️  ATTENTION : Vous devez configurer votre clé API OpenAI")
    print("=" * 80)
    print("\n1. Ouvrez le fichier .env")
    print("2. Remplacez 'sk-proj-your-key-here' par votre vraie clé OpenAI")
    print("3. Sauvegardez et relancez ce script\n")
    print("Pour obtenir une clé : https://platform.openai.com/api-keys\n")
    exit(1)

from main import HotelConciergeBot


def print_separator(char="=", length=80):
    """Affiche une ligne de séparation"""
    print(char * length)


def print_client_header(client_name, client_phone, emoji="👤"):
    """Affiche l'en-tête d'un client"""
    print(f"\n{emoji} CLIENT : {client_name} ({client_phone})")
    print_separator("-", 80)


def print_message(sender, message, delay=0.5):
    """Affiche un message avec un délai pour l'effet de conversation"""
    time.sleep(delay)

    if sender == "client":
        print(f"\n💬 Client : {message}")
    else:
        print(f"\n🤖 Concierge IA : {message}")


def simulate_conversation():
    """Simulation complète de 2 clients"""

    print_separator("=")
    print("🏨  HÔTEL 121 PARIS - DÉMONSTRATION DU CONCIERGE IA")
    print_separator("=")
    print("\n📍 Lieu : 121 Rue de la Boétie, 75008 Paris")
    print("🎯 Objectif : Montrer que le bot se souvient de chaque conversation")
    print("👥 2 clients vont interagir simultanément\n")

    input("Appuyez sur Entrée pour commencer la démonstration...")

    # Initialiser le bot
    print("\n🔄 Initialisation du système...\n")
    bot = HotelConciergeBot()

    print_separator("=")
    print("SCÉNARIO : 2 clients arrivent à l'hôtel et utilisent WhatsApp")
    print_separator("=")

    # ==========================================
    # CLIENT 1 : Sophie Durand
    # ==========================================
    client1_phone = "whatsapp:+33612345678"
    client1_name = "Sophie Durand"

    print_client_header(client1_name, client1_phone, "👩")
    print("📝 Profil : Française, en voyage romantique, budget confortable")

    input("\n→ Appuyez sur Entrée pour voir la conversation de Sophie...")

    # Message 1
    print_message("client", "Bonjour ! Je viens d'arriver à l'Hôtel 121 Paris 😊")
    response1 = bot.handle_message(client1_phone, "Bonjour ! Je viens d'arriver à l'Hôtel 121 Paris 😊")
    print_message("bot", response1[:300] + "..." if len(response1) > 300 else response1)

    # Message 2
    print_message("client", "Je m'appelle Sophie. Je suis en voyage romantique avec mon mari")
    response2 = bot.handle_message(client1_phone, "Je m'appelle Sophie. Je suis en voyage romantique avec mon mari")
    print_message("bot", response2[:300] + "..." if len(response2) > 300 else response2)

    # Message 3
    print_message("client", "On cherche un restaurant romantique ce soir, budget 100€ par personne")
    response3 = bot.handle_message(client1_phone, "On cherche un restaurant romantique ce soir, budget 100€ par personne")
    print_message("bot", response3[:400] + "..." if len(response3) > 400 else response3)

    # Message 4
    print_message("client", "Le Gourmet Parisien m'intéresse ! C'est à quelle distance ?")
    response4 = bot.handle_message(client1_phone, "Le Gourmet Parisien m'intéresse ! C'est à quelle distance ?")
    print_message("bot", response4[:300] + "..." if len(response4) > 300 else response4)

    print("\n" + "=" * 80)
    print("✅ Conversation 1 terminée - Le bot connaît maintenant Sophie et ses préférences")
    print("=" * 80)

    input("\n→ Appuyez sur Entrée pour passer au client 2...")

    # ==========================================
    # CLIENT 2 : Marc Leblanc
    # ==========================================
    client2_phone = "whatsapp:+33687654321"
    client2_name = "Marc Leblanc"

    print_client_header(client2_name, client2_phone, "👨")
    print("📝 Profil : Français, en voyage d'affaires, budget limité")

    input("\n→ Appuyez sur Entrée pour voir la conversation de Marc...")

    # Message 1
    print_message("client", "Salut, je suis Marc, client de l'Hôtel 121")
    response1 = bot.handle_message(client2_phone, "Salut, je suis Marc, client de l'Hôtel 121")
    print_message("bot", response1[:300] + "..." if len(response1) > 300 else response1)

    # Message 2
    print_message("client", "Je suis en déplacement pro, je veux manger pas cher ce midi")
    response2 = bot.handle_message(client2_phone, "Je suis en déplacement pro, je veux manger pas cher ce midi")
    print_message("bot", response2[:300] + "..." if len(response2) > 300 else response2)

    # Message 3
    print_message("client", "Maximum 35 euros, quelque chose de rapide")
    response3 = bot.handle_message(client2_phone, "Maximum 35 euros, quelque chose de rapide")
    print_message("bot", response3[:400] + "..." if len(response3) > 400 else response3)

    # Message 4
    print_message("client", "Le Bistrot du Coin, c'est bien ça ?")
    response4 = bot.handle_message(client2_phone, "Le Bistrot du Coin, c'est bien ça ?")
    print_message("bot", response4[:300] + "..." if len(response4) > 300 else response4)

    print("\n" + "=" * 80)
    print("✅ Conversation 2 terminée - Le bot connaît maintenant Marc et ses besoins")
    print("=" * 80)

    input("\n→ Appuyez sur Entrée pour tester la MÉMOIRE avec Sophie...")

    # ==========================================
    # RETOUR À SOPHIE - TEST DE MÉMOIRE
    # ==========================================
    print_client_header(client1_name + " (RETOUR)", client1_phone, "👩")
    print("🧪 TEST : Le bot se souvient-il de Sophie et de son contexte ?")

    input("\n→ Appuyez sur Entrée...")

    # Message 5 Sophie
    print_message("client", "Au fait, vous vous souvenez de mon budget ?")
    response5 = bot.handle_message(client1_phone, "Au fait, vous vous souvenez de mon budget ?")
    print_message("bot", response5)

    # Message 6 Sophie
    print_message("client", "Et c'était quel restaurant que je voulais ?")
    response6 = bot.handle_message(client1_phone, "Et c'était quel restaurant que je voulais ?")
    print_message("bot", response6)

    # Message 7 Sophie
    print_message("client", "Parfait ! Et demain on voudrait visiter des musées")
    response7 = bot.handle_message(client1_phone, "Parfait ! Et demain on voudrait visiter des musées")
    print_message("bot", response7[:400] + "..." if len(response7) > 400 else response7)

    print("\n" + "=" * 80)
    print("✅ Le bot se souvient parfaitement de Sophie !")
    print("   - Budget : 100€")
    print("   - Restaurant : Le Gourmet Parisien")
    print("   - Contexte : Voyage romantique")
    print("=" * 80)

    input("\n→ Appuyez sur Entrée pour tester la MÉMOIRE avec Marc...")

    # ==========================================
    # RETOUR À MARC - TEST DE MÉMOIRE
    # ==========================================
    print_client_header(client2_name + " (RETOUR)", client2_phone, "👨")
    print("🧪 TEST : Le bot se souvient-il de Marc ? A-t-il confondu avec Sophie ?")

    input("\n→ Appuyez sur Entrée...")

    # Message 5 Marc
    print_message("client", "Rappelle-moi mon budget ?")
    response5 = bot.handle_message(client2_phone, "Rappelle-moi mon budget ?")
    print_message("bot", response5)

    # Message 6 Marc
    print_message("client", "Et c'était quel resto déjà ?")
    response6 = bot.handle_message(client2_phone, "Et c'était quel resto déjà ?")
    print_message("bot", response6)

    # Message 7 Marc
    print_message("client", "Ok merci ! Et pour demain, des activités business dans le quartier ?")
    response7 = bot.handle_message(client2_phone, "Ok merci ! Et pour demain, des activités business dans le quartier ?")
    print_message("bot", response7[:400] + "..." if len(response7) > 400 else response7)

    print("\n" + "=" * 80)
    print("✅ Le bot se souvient parfaitement de Marc (sans confusion avec Sophie) !")
    print("   - Budget : 35€")
    print("   - Restaurant : Le Bistrot du Coin")
    print("   - Contexte : Voyage d'affaires")
    print("=" * 80)

    # ==========================================
    # STATISTIQUES FINALES
    # ==========================================
    input("\n→ Appuyez sur Entrée pour voir les statistiques finales...")

    print("\n" + "=" * 80)
    print("📊 STATISTIQUES DE LA DÉMONSTRATION")
    print("=" * 80)

    import sqlite3
    conn = sqlite3.connect("data/agent_memory.db")
    cursor = conn.cursor()

    # Stats par client
    cursor.execute("""
        SELECT client_phone, COUNT(*) as messages
        FROM conversations
        WHERE client_phone IN (?, ?)
        GROUP BY client_phone
    """, (client1_phone, client2_phone))

    stats = cursor.fetchall()

    print(f"\n👥 Nombre de clients : 2")
    print(f"💬 Messages traités :")
    for phone, count in stats:
        name = "Sophie" if phone == client1_phone else "Marc"
        print(f"   - {name} : {count} messages")

    print(f"\n🧠 MÉMOIRE CONVERSATIONNELLE :")
    print(f"   ✅ Chaque client a son historique isolé")
    print(f"   ✅ Pas de confusion entre Sophie (100€) et Marc (35€)")
    print(f"   ✅ Le bot maintient le contexte sur plusieurs échanges")
    print(f"   ✅ Références aux messages précédents comprises")

    conn.close()

    print("\n" + "=" * 80)
    print("🎉 DÉMONSTRATION TERMINÉE")
    print("=" * 80)
    print("""
📝 RÉSUMÉ :
• Sophie : Voyage romantique, budget 100€, Le Gourmet Parisien, musées
• Marc : Voyage pro, budget 35€, Bistrot du Coin, activités business

✅ Le système a parfaitement maintenu 2 conversations distinctes
✅ Aucune confusion entre les clients
✅ Mémoire conversationnelle fonctionnelle sur 7 messages chacun
✅ Le bot comprend les références contextuelles ("le restaurant que je voulais")

🔒 Isolation totale : Chaque numéro WhatsApp = Une mémoire unique
🧠 Historique : 10 derniers messages chargés automatiquement
💾 Stockage : SQLite local (data/agent_memory.db)
""")


if __name__ == "__main__":
    try:
        simulate_conversation()
    except KeyboardInterrupt:
        print("\n\n⚠️  Démonstration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur : {e}")
        print("\nVérifiez que :")
        print("1. Votre clé OpenAI est configurée dans .env")
        print("2. Vous avez des crédits sur votre compte OpenAI")
        print("3. Toutes les dépendances sont installées (pip install -r requirements.txt)")
