"""
Test de la mémoire conversationnelle
Démontre que le bot se souvient du contexte de chaque client individuellement
"""

import os
from dotenv import load_dotenv
from main import HotelConciergeBot

# Load environment
load_dotenv()


def test_conversation_continuity():
    """Test que le bot maintient le fil de la conversation"""
    print("=" * 70)
    print("🧪 TEST DE MÉMOIRE CONVERSATIONNELLE")
    print("=" * 70)
    print()

    bot = HotelConciergeBot()

    # Client 1 : Marie
    client1 = "whatsapp:+33612345678"
    print("👤 CLIENT 1 (Marie) - +33612345678")
    print("-" * 70)

    conversation1 = [
        "Bonjour, je m'appelle Marie",
        "Je cherche un restaurant romantique",
        "Mon budget est de 80 euros par personne",
        "Le premier de votre liste m'intéresse, c'est quoi ?",
        "Parfait, et vous avez des activités pour demain ?",
        "Je préfère les musées",
    ]

    for i, message in enumerate(conversation1, 1):
        print(f"\n📨 Marie: {message}")
        response = bot.handle_message(client1, message)
        print(f"🤖 Bot: {response[:200]}..." if len(response) > 200 else f"🤖 Bot: {response}")

    print("\n" + "=" * 70)
    print()

    # Client 2 : Jean (conversation simultanée)
    client2 = "whatsapp:+33687654321"
    print("👤 CLIENT 2 (Jean) - +33687654321")
    print("-" * 70)

    conversation2 = [
        "Salut, moi c'est Jean",
        "Je veux manger japonais",
        "Pas cher si possible, max 40 euros",
        "Le dernier restaurant, il est où ?",
        "Et pour des activités avec des enfants ?",
    ]

    for i, message in enumerate(conversation2, 1):
        print(f"\n📨 Jean: {message}")
        response = bot.handle_message(client2, message)
        print(f"🤖 Bot: {response[:200]}..." if len(response) > 200 else f"🤖 Bot: {response}")

    print("\n" + "=" * 70)
    print()

    # Retour à Marie pour vérifier que le contexte est toujours là
    print("🔄 RETOUR À MARIE (vérification de la mémoire)")
    print("-" * 70)

    marie_return = [
        "Vous vous souvenez de mon budget ?",
        "Et c'était quoi le restaurant que je voulais ?",
    ]

    for message in marie_return:
        print(f"\n📨 Marie: {message}")
        response = bot.handle_message(client1, message)
        print(f"🤖 Bot: {response}")

    print("\n" + "=" * 70)
    print()

    # Retour à Jean
    print("🔄 RETOUR À JEAN (vérification de la mémoire)")
    print("-" * 70)

    jean_return = [
        "C'était quoi mon budget déjà ?",
        "Et je voulais quel type de cuisine ?",
    ]

    for message in jean_return:
        print(f"\n📨 Jean: {message}")
        response = bot.handle_message(client2, message)
        print(f"🤖 Bot: {response}")

    print("\n" + "=" * 70)
    print("✅ TEST TERMINÉ")
    print("=" * 70)
    print()
    print("📊 VÉRIFICATIONS ATTENDUES :")
    print("✓ Le bot devrait se souvenir du nom de Marie")
    print("✓ Le bot devrait se souvenir du budget de Marie (80€)")
    print("✓ Le bot devrait se souvenir que Marie préfère les musées")
    print("✓ Le bot NE devrait PAS confondre Marie avec Jean")
    print("✓ Le bot devrait se souvenir que Jean veut du japonais pas cher (40€)")
    print("✓ Chaque client a son propre contexte isolé")
    print()


def test_context_switching():
    """Test rapide de bascule entre clients"""
    print("=" * 70)
    print("🔄 TEST DE BASCULE RAPIDE ENTRE CLIENTS")
    print("=" * 70)
    print()

    bot = HotelConciergeBot()

    # Conversations entrelacées
    client_a = "whatsapp:+33611111111"
    client_b = "whatsapp:+33622222222"

    exchanges = [
        (client_a, "Alice", "Je veux un restaurant français"),
        (client_b, "Bob", "Je cherche un restaurant italien"),
        (client_a, "Alice", "Budget 100 euros"),
        (client_b, "Bob", "Budget 50 euros"),
        (client_a, "Alice", "Vous vous souvenez de ce que je cherche ?"),
        (client_b, "Bob", "Et moi, c'était quoi déjà ?"),
    ]

    for client, name, message in exchanges:
        print(f"\n👤 {name}: {message}")
        response = bot.handle_message(client, message)
        print(f"🤖 Bot: {response[:150]}..." if len(response) > 150 else f"🤖 Bot: {response}")

    print("\n" + "=" * 70)
    print("✅ Le bot devrait répondre correctement à chaque client")
    print("✓ Alice → français, 100€")
    print("✓ Bob → italien, 50€")
    print("=" * 70)
    print()


def show_memory_stats(bot):
    """Afficher les stats de mémoire"""
    print("\n" + "=" * 70)
    print("📊 STATISTIQUES DE MÉMOIRE")
    print("=" * 70)

    import sqlite3
    conn = sqlite3.connect("data/agent_memory.db")
    cursor = conn.cursor()

    # Nombre de clients uniques
    cursor.execute("SELECT COUNT(DISTINCT client_phone) FROM conversations")
    unique_clients = cursor.fetchone()[0]

    # Nombre total de conversations
    cursor.execute("SELECT COUNT(*) FROM conversations")
    total_convs = cursor.fetchone()[0]

    # Conversations par client
    cursor.execute("""
        SELECT client_phone, COUNT(*) as count
        FROM conversations
        GROUP BY client_phone
        ORDER BY count DESC
    """)
    client_stats = cursor.fetchall()

    print(f"\n👥 Clients uniques : {unique_clients}")
    print(f"💬 Total conversations : {total_convs}")
    print(f"\n📋 Détail par client :")
    for phone, count in client_stats:
        print(f"   {phone}: {count} messages")

    conn.close()
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("\n🏨 TEST DE MÉMOIRE CONVERSATIONNELLE - Hotel Concierge AI\n")

    # Test 1 : Continuité de conversation
    test_conversation_continuity()

    # Test 2 : Bascule rapide entre clients
    test_context_switching()

    # Stats finales
    from main import HotelConciergeBot
    bot = HotelConciergeBot()
    show_memory_stats(bot)

    print("\n✅ TOUS LES TESTS TERMINÉS\n")
