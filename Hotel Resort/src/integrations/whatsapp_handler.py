"""
WhatsApp Integration using Twilio
Handles incoming/outgoing messages and webhook management
"""

import os
from typing import Dict, Optional
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request


class WhatsAppHandler:
    """
    Manages WhatsApp communication via Twilio API
    Handles webhooks, message sending, and template messages
    """

    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

        if not self.account_sid or not self.auth_token:
            raise ValueError("Twilio credentials not found in environment variables")

        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, to_number: str, message: str) -> bool:
        """
        Send a WhatsApp message to a client

        Args:
            to_number: Client's phone number (format: whatsapp:+33123456789)
            message: Text message to send

        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Ensure number is in WhatsApp format
            if not to_number.startswith("whatsapp:"):
                to_number = f"whatsapp:{to_number}"

            message_obj = self.client.messages.create(
                from_=self.whatsapp_number,
                body=message,
                to=to_number
            )

            print(f"Message sent successfully. SID: {message_obj.sid}")
            return True

        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False

    def send_template_message(self, to_number: str, template_name: str, params: Dict) -> bool:
        """
        Send a pre-approved WhatsApp template message
        Useful for messages outside the 24-hour window

        Args:
            to_number: Client's phone number
            template_name: Name of the approved template
            params: Template parameters

        Returns:
            bool: Success status
        """
        try:
            # Ensure number is in WhatsApp format
            if not to_number.startswith("whatsapp:"):
                to_number = f"whatsapp:{to_number}"

            # Templates need to be pre-approved in Twilio
            # This is a placeholder for template functionality
            message_obj = self.client.messages.create(
                from_=self.whatsapp_number,
                to=to_number,
                content_sid=template_name,  # Template SID from Twilio
                content_variables=params
            )

            print(f"Template message sent. SID: {message_obj.sid}")
            return True

        except Exception as e:
            print(f"Error sending template message: {e}")
            return False

    def send_welcome_message(self, to_number: str, client_name: str, hotel_config: Dict) -> bool:
        """
        Send welcome message before arrival
        """
        message = f"""
👋 Bonjour {client_name} !

Bienvenue au {hotel_config['name']} ! Nous sommes ravis de vous accueillir.

📍 **Informations pratiques :**
• Adresse : {hotel_config['address']}
• Check-in : {hotel_config['check_in_time']}
• Check-out : {hotel_config['check_out_time']}

💬 Je suis votre concierge IA disponible 24/7 via WhatsApp. N'hésitez pas à me poser toutes vos questions !

Que puis-je faire pour vous aujourd'hui ? 😊
"""
        return self.send_message(to_number, message.strip())

    def send_checkout_survey(self, to_number: str, client_name: str, hotel_name: str) -> bool:
        """
        Send satisfaction survey after checkout
        """
        message = f"""
👋 Au revoir {client_name} !

Merci d'avoir séjourné au {hotel_name}. Nous espérons que vous avez passé un excellent moment.

⭐ **Votre avis compte !**
Pourriez-vous prendre 30 secondes pour évaluer votre séjour ?

1️⃣ Excellent
2️⃣ Très bien
3️⃣ Bien
4️⃣ Moyen
5️⃣ À améliorer

Répondez simplement avec le chiffre correspondant.

À très bientôt ! 💙
"""
        return self.send_message(to_number, message.strip())

    @staticmethod
    def parse_incoming_webhook(request_data: Dict) -> Dict:
        """
        Parse incoming WhatsApp webhook from Twilio

        Args:
            request_data: Flask request.values or request.form

        Returns:
            Dict with message details
        """
        return {
            "from": request_data.get("From", ""),
            "to": request_data.get("To", ""),
            "body": request_data.get("Body", ""),
            "message_sid": request_data.get("MessageSid", ""),
            "media_url": request_data.get("MediaUrl0", None),  # If media attached
            "num_media": int(request_data.get("NumMedia", 0))
        }

    @staticmethod
    def create_response(message: str) -> str:
        """
        Create a TwiML response for immediate reply
        """
        resp = MessagingResponse()
        resp.message(message)
        return str(resp)


def create_webhook_app(message_handler_callback):
    """
    Create Flask app for WhatsApp webhook handling

    Args:
        message_handler_callback: Function to handle incoming messages
                                  Signature: callback(phone: str, message: str) -> str
    """
    app = Flask(__name__)

    @app.route("/webhook/whatsapp", methods=["POST"])
    def whatsapp_webhook():
        """Handle incoming WhatsApp messages"""
        try:
            # Parse incoming message
            incoming = WhatsAppHandler.parse_incoming_webhook(request.values)

            phone = incoming["from"]
            message_text = incoming["body"]

            print(f"Received message from {phone}: {message_text}")

            # Process message through callback
            response_text = message_handler_callback(phone, message_text)

            # Create TwiML response
            return WhatsAppHandler.create_response(response_text)

        except Exception as e:
            print(f"Error handling webhook: {e}")
            return WhatsAppHandler.create_response(
                "Désolé, une erreur s'est produite. Un membre de notre équipe vous contactera bientôt."
            ), 500

    @app.route("/webhook/whatsapp/status", methods=["POST"])
    def whatsapp_status():
        """Handle message status updates"""
        status = request.values.get("MessageStatus", "")
        message_sid = request.values.get("MessageSid", "")

        print(f"Message {message_sid} status: {status}")
        return "", 200

    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "service": "Hotel Concierge WhatsApp Bot"}, 200

    return app
