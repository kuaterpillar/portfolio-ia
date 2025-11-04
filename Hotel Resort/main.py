"""
Hotel Concierge AI - Main Application
Focus: AI Agent with conversation memory + Recommendations
Note: Booking system disabled for now (not needed)
"""

import os
import json
from dotenv import load_dotenv
from src.core.ai_agent import SelfLearningAgent
from src.core.recommendation_engine import RecommendationEngine
# from src.core.booking_system import BookingSystem  # Disabled for now

# Load environment variables
load_dotenv()

# Import appropriate WhatsApp handler based on provider
WHATSAPP_PROVIDER = os.getenv("WHATSAPP_PROVIDER", "meta").lower()

if WHATSAPP_PROVIDER == "meta":
    from src.integrations.whatsapp_handler_meta import MetaWhatsAppHandler as WhatsAppHandler
    from src.integrations.whatsapp_handler_meta import create_webhook_app_meta as create_webhook_app
    print("📱 Using Meta WhatsApp Business API")
else:
    from src.integrations.whatsapp_handler import WhatsAppHandler, create_webhook_app
    print("📱 Using Twilio WhatsApp API")


class HotelConciergeBot:
    """
    Main orchestrator for the Hotel Concierge AI system

    Features enabled:
    ✅ AI Agent with conversation memory (10 messages history)
    ✅ Recommendation engine (restaurants, activities, services)
    ✅ WhatsApp integration
    ❌ Booking system (disabled - not needed for now)
    """

    def __init__(self):
        # Load hotel configuration
        self.hotel_config = {
            "name": os.getenv("HOTEL_NAME", "Grand Hotel"),
            "city": os.getenv("HOTEL_CITY", "Paris"),
            "address": os.getenv("HOTEL_ADDRESS", "123 Avenue Example"),
            "phone": os.getenv("HOTEL_PHONE", "+33 1 23 45 67 89"),
            "email": os.getenv("HOTEL_EMAIL", "contact@hotel.com"),
            "check_in_time": os.getenv("CHECK_IN_TIME", "15:00"),
            "check_out_time": os.getenv("CHECK_OUT_TIME", "11:00")
        }

        # Initialize components
        print("🔄 Initialisation du système...")

        self.ai_agent = SelfLearningAgent(self.hotel_config)
        print("✅ Agent IA chargé (avec mémoire conversationnelle)")

        self.recommendation_engine = RecommendationEngine(
            self.hotel_config["city"],
            self.hotel_config["address"]
        )
        print("✅ Moteur de recommandations chargé")

        # self.booking_system = BookingSystem()  # Disabled
        self.booking_system = None  # Placeholder

        self.whatsapp = WhatsAppHandler()
        print("✅ WhatsApp handler chargé")

        print(f"\n🏨 {self.hotel_config['name']} Concierge AI initialisé!")
        print(f"📍 Location: {self.hotel_config['city']}")
        print(f"💬 Mémoire conversationnelle: Active (10 messages/client)")
        print(f"🔒 Isolation des clients: Active (pas de confusion possible)\n")

    def handle_message(self, phone: str, message: str) -> str:
        """
        Main message handler - coordinates all AI logic
        This is called by the WhatsApp webhook
        """
        print(f"\n📨 Message from {phone}: {message}")

        # Get client context for personalization
        client_context = self.ai_agent.get_client_context(phone)

        # Check if message is about specific intents
        message_lower = message.lower()

        # Intent: Recommendations
        if self._is_recommendation_intent(message_lower):
            return self._handle_recommendation_intent(phone, message, client_context)

        # Intent: Satisfaction survey response
        if self._is_survey_response(message_lower):
            return self._handle_survey_response(phone, message)

        # Default: Use AI agent for general conversation with memory
        # The AI agent automatically loads the last 10 messages for context continuity
        response, metadata = self.ai_agent.process_message(phone, message)

        print(f"🤖 Response: {response}")
        print(f"⚡ Response time: {metadata['response_time_ms']:.0f}ms")

        return response

    def _is_recommendation_intent(self, message: str) -> bool:
        """Detect if message is asking for recommendations"""
        recommendation_keywords = [
            "restaurant", "manger", "activité", "musée", "visite", "faire",
            "recommander", "conseiller", "proposer", "suggestion",
            "eat", "visit", "do", "activity", "recommend", "suggest"
        ]
        return any(keyword in message for keyword in recommendation_keywords)

    def _is_survey_response(self, message: str) -> bool:
        """Detect if message is a survey response (1-5)"""
        return message.strip() in ["1", "2", "3", "4", "5"]

    def _handle_recommendation_intent(self, phone: str, message: str, client_context) -> str:
        """Handle recommendation requests"""
        # Try to generate personalized recommendation
        recommendation = self.recommendation_engine.generate_personalized_recommendation(
            message,
            client_context
        )

        if recommendation:
            return recommendation

        # Fallback to AI agent if recommendation engine can't handle it
        response, _ = self.ai_agent.process_message(phone, message)
        return response

    def _handle_survey_response(self, phone: str, message: str) -> str:
        """Handle satisfaction survey responses"""
        score = int(message.strip())

        # Convert 1-5 scale to 0-5 (1=best, 5=worst -> 5=best, 1=worst)
        satisfaction_score = 6 - score

        # Store feedback (simplified - in production, link to specific conversation)
        print(f"📊 Satisfaction score from {phone}: {satisfaction_score}/5")

        if score <= 2:
            return f"""
🌟 Merci beaucoup pour votre excellent retour !

Nous serions ravis si vous pouviez partager votre expérience sur Google ou TripAdvisor.

À très bientôt au {self.hotel_config['name']} ! 💙
"""
        elif score == 3:
            return """
👍 Merci pour votre retour !

Nous sommes heureux que vous ayez apprécié votre séjour.

À bientôt ! 😊
"""
        else:
            return """
😔 Merci pour votre retour. Nous sommes désolés que votre expérience n'ait pas été parfaite.

Un membre de notre équipe va vous contacter pour comprendre comment nous améliorer.

Merci de votre confiance.
"""

    def send_welcome_to_client(self, phone: str, client_name: str):
        """Send welcome message before arrival"""
        return self.whatsapp.send_welcome_message(phone, client_name, self.hotel_config)

    def send_checkout_survey(self, phone: str, client_name: str):
        """Send satisfaction survey after checkout"""
        return self.whatsapp.send_checkout_survey(phone, client_name, self.hotel_config['name'])

    def get_performance_report(self) -> dict:
        """Get AI performance analytics"""
        return self.ai_agent.analyze_performance()


def main():
    """Main entry point"""
    # Initialize bot
    bot = HotelConciergeBot()

    # Create message handler for webhook
    def message_handler(phone: str, message: str) -> str:
        return bot.handle_message(phone, message)

    # Create Flask app with webhook
    app = create_webhook_app(message_handler)

    # Get port from environment
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    print(f"🚀 Starting webhook server on port {port}...")
    print(f"📡 Webhook URL: http://localhost:{port}/webhook/whatsapp")

    if WHATSAPP_PROVIDER == "meta":
        print(f"💡 Configure this URL in your Meta Business Console (Webhooks)")
        print(f"   Verify Token: {os.getenv('META_WEBHOOK_VERIFY_TOKEN', 'roomie_hotel_webhook_2025')}\n")
    else:
        print(f"💡 Configure this URL in your Twilio console\n")

    # Run Flask app
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
