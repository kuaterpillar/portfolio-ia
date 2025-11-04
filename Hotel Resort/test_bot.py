"""
Script de test pour le Hotel Concierge AI Bot
Teste les fonctionnalités principales sans WhatsApp
"""

import os
from dotenv import load_dotenv
from main import HotelConciergeBot

# Load environment
load_dotenv()


def test_bot_initialization():
    """Test bot initialization"""
    print("🧪 Test 1: Initialisation du bot...")
    try:
        bot = HotelConciergeBot()
        print("✅ Bot initialisé avec succès\n")
        return bot
    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}\n")
        return None


def test_conversation(bot):
    """Test conversation handling"""
    print("🧪 Test 2: Traitement de conversations...")

    test_messages = [
        ("whatsapp:+33612345678", "Bonjour ! Je cherche des informations sur l'hôtel"),
        ("whatsapp:+33612345678", "Quels sont les horaires du petit-déjeuner ?"),
        ("whatsapp:+33612345678", "Je voudrais un restaurant romantique, budget 100€"),
    ]

    for phone, message in test_messages:
        print(f"\n👤 Client: {message}")
        try:
            response = bot.handle_message(phone, message)
            print(f"🤖 Bot: {response[:200]}..." if len(response) > 200 else f"🤖 Bot: {response}")
            print("✅ Réponse générée\n")
        except Exception as e:
            print(f"❌ Erreur: {e}\n")


def test_booking_availability(bot):
    """Test booking system"""
    print("\n🧪 Test 3: Système de réservation...")

    try:
        # Check availability
        available = bot.booking_system.check_availability(
            check_in="2025-12-15",
            check_out="2025-12-17",
            num_guests=2
        )

        if available:
            print(f"✅ Trouvé {len(available)} types de chambres disponibles:")
            for room in available:
                print(f"   - {room['name']}: {room['price_per_night']}€/nuit")

            # Try to create a booking
            success, message, booking_id = bot.booking_system.create_booking(
                client_phone="whatsapp:+33612345678",
                room_type_id=available[0]['room_type_id'],
                check_in="2025-12-15",
                check_out="2025-12-17",
                num_guests=2,
                client_name="Test Client"
            )

            if success:
                print(f"✅ Réservation créée: {message}")
                print(f"   Booking ID: {booking_id}\n")
            else:
                print(f"❌ Échec réservation: {message}\n")
        else:
            print("⚠️ Aucune chambre disponible\n")

    except Exception as e:
        print(f"❌ Erreur booking: {e}\n")


def test_recommendations(bot):
    """Test recommendation engine"""
    print("🧪 Test 4: Moteur de recommandations...")

    try:
        # Test restaurant recommendations
        restaurants = bot.recommendation_engine.recommend_restaurants(
            budget=100,
            ambiance="romantique"
        )

        if restaurants:
            print(f"✅ Trouvé {len(restaurants)} restaurants:")
            for resto in restaurants:
                print(f"   - {resto['name']} ({resto['avg_price_per_person']}€)")

        # Test activity recommendations
        weather = bot.recommendation_engine.get_weather()
        if weather:
            print(f"\n✅ Météo actuelle: {weather['description']}, {weather['temp']}°C")

        activities = bot.recommendation_engine.recommend_activities(
            weather=weather,
            budget=50
        )

        if activities:
            print(f"✅ Trouvé {len(activities)} activités:")
            for activity in activities:
                print(f"   - {activity['name']} ({activity['price']}€)")

        print()

    except Exception as e:
        print(f"❌ Erreur recommandations: {e}\n")


def test_client_memory(bot):
    """Test client memory and context"""
    print("🧪 Test 5: Mémoire client et contexte...")

    try:
        phone = "whatsapp:+33612345678"

        # Update client profile
        bot.ai_agent.update_client_profile(phone, {
            "language": "fr",
            "preferences": {
                "budget": "moyen",
                "activity_style": "culture"
            }
        })

        # Retrieve context
        context = bot.ai_agent.get_client_context(phone)

        if context:
            print(f"✅ Contexte client récupéré:")
            print(f"   - Langue: {context.get('language')}")
            print(f"   - Préférences: {context.get('preferences')}")
            print(f"   - Interactions: {context.get('total_interactions')}")
            print()
        else:
            print("⚠️ Aucun contexte trouvé\n")

    except Exception as e:
        print(f"❌ Erreur mémoire: {e}\n")


def test_performance_analytics(bot):
    """Test performance tracking"""
    print("🧪 Test 6: Analyse de performance...")

    try:
        report = bot.get_performance_report()
        print(f"✅ Rapport de performance:")
        print(f"   - Temps de réponse moyen: {report.get('avg_response_time_ms', 0):.0f}ms")
        print(f"   - Satisfaction moyenne: {report.get('avg_satisfaction', 0):.2f}/5")
        print(f"   - Total conversations: {report.get('total_conversations', 0)}")
        print()

    except Exception as e:
        print(f"❌ Erreur analytics: {e}\n")


def main():
    """Run all tests"""
    print("=" * 60)
    print("🏨 HOTEL CONCIERGE AI - TESTS AUTOMATIQUES")
    print("=" * 60)
    print()

    # Initialize bot
    bot = test_bot_initialization()

    if not bot:
        print("❌ Impossible de continuer sans bot initialisé")
        return

    # Run tests
    test_conversation(bot)
    test_booking_availability(bot)
    test_recommendations(bot)
    test_client_memory(bot)
    test_performance_analytics(bot)

    print("=" * 60)
    print("✅ Tests terminés !")
    print("=" * 60)


if __name__ == "__main__":
    main()
