"""
WhatsApp Integration using Meta WhatsApp Business API
Handles incoming/outgoing messages and webhook management
"""

import os
import requests
from typing import Dict, Optional
from flask import Flask, request, jsonify


class MetaWhatsAppHandler:
    """
    Manages WhatsApp communication via Meta WhatsApp Business API
    Handles webhooks, message sending, and template messages
    """

    def __init__(self):
        self.access_token = os.getenv("META_WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("META_WHATSAPP_PHONE_NUMBER_ID")
        self.verify_token = os.getenv("META_WEBHOOK_VERIFY_TOKEN", "roomie_hotel_webhook_2025")
        self.api_version = os.getenv("META_API_VERSION", "v18.0")

        if not self.access_token or not self.phone_number_id:
            raise ValueError("Meta WhatsApp credentials not found in environment variables")

        self.api_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def send_message(self, to_number: str, message: str) -> bool:
        """
        Send a WhatsApp message to a client via Meta API

        Args:
            to_number: Client's phone number (format: +33123456789 or whatsapp:+33123456789)
            message: Text message to send

        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Clean phone number (remove whatsapp: prefix if present)
            clean_number = to_number.replace("whatsapp:", "").replace("+", "")

            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": clean_number,
                "type": "text",
                "text": {
                    "preview_url": False,
                    "body": message
                }
            }

            response = requests.post(self.api_url, headers=self.headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                print(f"Message sent successfully. Message ID: {result.get('messages', [{}])[0].get('id')}")
                return True
            else:
                print(f"Error sending message: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False

    def send_template_message(self, to_number: str, template_name: str, language_code: str = "fr", params: Optional[Dict] = None) -> bool:
        """
        Send a pre-approved WhatsApp template message
        Templates must be approved in Meta Business Manager

        Args:
            to_number: Client's phone number
            template_name: Name of the approved template
            language_code: Template language (fr, en, etc.)
            params: Template parameters (optional)

        Returns:
            bool: Success status
        """
        try:
            # Clean phone number
            clean_number = to_number.replace("whatsapp:", "").replace("+", "")

            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": clean_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": language_code
                    }
                }
            }

            # Add parameters if provided
            if params:
                components = []
                if "body" in params:
                    components.append({
                        "type": "body",
                        "parameters": [{"type": "text", "text": str(p)} for p in params["body"]]
                    })
                if components:
                    payload["template"]["components"] = components

            response = requests.post(self.api_url, headers=self.headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                print(f"Template message sent. Message ID: {result.get('messages', [{}])[0].get('id')}")
                return True
            else:
                print(f"Error sending template: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error sending template message: {e}")
            return False

    def send_welcome_message(self, to_number: str, client_name: str, hotel_config: Dict) -> bool:
        """
        Send welcome message before arrival
        """
        message = f"""👋 Bonjour {client_name} !

Bienvenue au {hotel_config['name']} ! Nous sommes ravis de vous accueillir.

📍 Informations pratiques :
• Adresse : {hotel_config['address']}
• Check-in : {hotel_config['check_in_time']}
• Check-out : {hotel_config['check_out_time']}

💬 Je suis votre concierge IA disponible 24/7 via WhatsApp. N'hésitez pas à me poser toutes vos questions !

Que puis-je faire pour vous aujourd'hui ?"""

        return self.send_message(to_number, message)

    def send_checkout_survey(self, to_number: str, client_name: str, hotel_name: str) -> bool:
        """
        Send satisfaction survey after checkout
        """
        message = f"""👋 Au revoir {client_name} !

Merci d'avoir séjourné au {hotel_name}. Nous espérons que vous avez passé un excellent moment.

⭐ Votre avis compte !
Pourriez-vous prendre 30 secondes pour évaluer votre séjour ?

1️⃣ Excellent
2️⃣ Très bien
3️⃣ Bien
4️⃣ Moyen
5️⃣ À améliorer

Répondez simplement avec le chiffre correspondant.

À très bientôt ! 💙"""

        return self.send_message(to_number, message)

    @staticmethod
    def parse_incoming_webhook(request_data: Dict) -> Optional[Dict]:
        """
        Parse incoming WhatsApp webhook from Meta

        Args:
            request_data: Flask request JSON data

        Returns:
            Dict with message details or None if not a message
        """
        try:
            # Meta webhook structure is nested
            entry = request_data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})

            messages = value.get("messages", [])
            if not messages:
                return None

            message = messages[0]

            return {
                "from": message.get("from", ""),  # Phone number without whatsapp: prefix
                "message_id": message.get("id", ""),
                "timestamp": message.get("timestamp", ""),
                "type": message.get("type", "text"),
                "body": message.get("text", {}).get("body", "") if message.get("type") == "text" else "",
                "name": value.get("contacts", [{}])[0].get("profile", {}).get("name", ""),
            }

        except Exception as e:
            print(f"Error parsing webhook: {e}")
            return None

    @staticmethod
    def verify_webhook(request_args: Dict, verify_token: str) -> Optional[str]:
        """
        Verify webhook challenge from Meta

        Args:
            request_args: Flask request.args
            verify_token: Your verify token

        Returns:
            Challenge string if valid, None otherwise
        """
        mode = request_args.get("hub.mode")
        token = request_args.get("hub.verify_token")
        challenge = request_args.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            print("Webhook verified successfully!")
            return challenge
        else:
            print("Webhook verification failed!")
            return None


def create_webhook_app_meta(message_handler_callback):
    """
    Create Flask app for Meta WhatsApp webhook handling

    Args:
        message_handler_callback: Function to handle incoming messages
                                  Signature: callback(phone: str, message: str) -> str
    """
    app = Flask(__name__)

    # Get verify token from environment
    verify_token = os.getenv("META_WEBHOOK_VERIFY_TOKEN", "roomie_hotel_webhook_2025")

    @app.route("/webhook/whatsapp", methods=["GET"])
    def whatsapp_webhook_verify():
        """Handle webhook verification from Meta"""
        challenge = MetaWhatsAppHandler.verify_webhook(request.args, verify_token)

        if challenge:
            return challenge, 200
        else:
            return "Forbidden", 403

    @app.route("/webhook/whatsapp", methods=["POST"])
    def whatsapp_webhook():
        """Handle incoming WhatsApp messages from Meta"""
        try:
            # Parse incoming message
            data = request.get_json()

            # Meta sends status updates too, ignore those
            if not data or "messages" not in str(data):
                return jsonify({"status": "ok"}), 200

            incoming = MetaWhatsAppHandler.parse_incoming_webhook(data)

            if not incoming:
                return jsonify({"status": "ok"}), 200

            phone = incoming["from"]
            message_text = incoming["body"]
            sender_name = incoming.get("name", "Client")

            print(f"Received message from {sender_name} ({phone}): {message_text}")

            # Process message through callback
            response_text = message_handler_callback(f"whatsapp:+{phone}", message_text)

            # Send response via Meta API
            handler = MetaWhatsAppHandler()
            handler.send_message(f"+{phone}", response_text)

            return jsonify({"status": "success"}), 200

        except Exception as e:
            print(f"Error handling webhook: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "service": "Hotel Concierge WhatsApp Bot (Meta API)",
            "provider": "Meta WhatsApp Business"
        }), 200

    return app
