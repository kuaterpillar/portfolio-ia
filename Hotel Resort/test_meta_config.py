"""
Test script to verify Meta WhatsApp configuration
Run this BEFORE connecting to Meta to check if everything is properly set up
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_env_variable(name, required=True):
    """Check if environment variable is set"""
    value = os.getenv(name)
    if value and value not in ["your_meta_access_token_here", "your_phone_number_id_here", "sk-proj-your-key-here"]:
        print(f"[OK] {name}: Configure")
        return True
    else:
        if required:
            print(f"[ERROR] {name}: NON configure (requis)")
        else:
            print(f"[WARN] {name}: NON configure (optionnel)")
        return False

def test_imports():
    """Test if all required packages are installed"""
    print("\n[PACKAGES] Test des imports...")

    try:
        import openai
        print("[OK] openai")
    except ImportError:
        print("[ERROR] openai - Installer avec: pip install openai")
        return False

    try:
        import requests
        print("[OK] requests")
    except ImportError:
        print("[ERROR] requests - Installer avec: pip install requests")
        return False

    try:
        import flask
        print("[OK] flask")
    except ImportError:
        print("[ERROR] flask - Installer avec: pip install flask")
        return False

    try:
        from dotenv import load_dotenv
        print("[OK] python-dotenv")
    except ImportError:
        print("[ERROR] python-dotenv - Installer avec: pip install python-dotenv")
        return False

    return True

def test_whatsapp_handler():
    """Test if WhatsApp handler can be imported"""
    print("\n[WHATSAPP] Test du handler WhatsApp Meta...")

    try:
        from src.integrations.whatsapp_handler_meta import MetaWhatsAppHandler
        print("[OK] MetaWhatsAppHandler importe correctement")
        return True
    except Exception as e:
        print(f"[ERROR] Erreur d'import: {e}")
        return False

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n[OPENAI] Test de la connexion OpenAI...")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "sk-proj-your-key-here":
        print("[ERROR] OPENAI_API_KEY non configure")
        return False

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)

        # Test simple API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )

        print("[OK] Connexion OpenAI reussie")
        print(f"   Modele utilise: {response.model}")
        return True

    except Exception as e:
        print(f"[ERROR] Erreur OpenAI: {e}")
        return False

def main():
    print("=" * 60)
    print("TEST DE CONFIGURATION ROOMIE - META WHATSAPP")
    print("=" * 60)

    # Test 1: Environment variables
    print("\n[ENV] Variables d'environnement:")
    print("-" * 60)

    provider = os.getenv("WHATSAPP_PROVIDER", "meta")
    print(f"[INFO] Provider WhatsApp: {provider}")

    all_ok = True

    # Required for OpenAI
    all_ok &= check_env_variable("OPENAI_API_KEY", required=True)

    if provider == "meta":
        # Required for Meta
        all_ok &= check_env_variable("META_WHATSAPP_ACCESS_TOKEN", required=True)
        all_ok &= check_env_variable("META_WHATSAPP_PHONE_NUMBER_ID", required=True)
        check_env_variable("META_WEBHOOK_VERIFY_TOKEN", required=False)
        check_env_variable("META_API_VERSION", required=False)

    # Hotel config
    print("\n[HOTEL] Configuration hotel:")
    check_env_variable("HOTEL_NAME", required=False)
    check_env_variable("HOTEL_CITY", required=False)
    check_env_variable("HOTEL_ADDRESS", required=False)

    # Test 2: Package imports
    if not test_imports():
        all_ok = False

    # Test 3: WhatsApp handler
    if not test_whatsapp_handler():
        all_ok = False

    # Test 4: OpenAI connection
    if not test_openai_connection():
        all_ok = False

    # Summary
    print("\n" + "=" * 60)
    if all_ok:
        print("[SUCCESS] TOUS LES TESTS REUSSIS !")
        print("=" * 60)
        print("\n[NEXT] Prochaines etapes:")
        print("1. Lance le serveur: python main.py")
        print("2. Lance ngrok: ngrok http 5000")
        print("3. Configure le webhook dans Meta Business Console")
        print("4. Envoie un message WhatsApp pour tester !")
        print("\n[DOC] Voir: QUICK_START_META_WHATSAPP.md")
    else:
        print("[FAIL] CERTAINS TESTS ONT ECHOUE")
        print("=" * 60)
        print("\n[TODO] Actions a faire:")
        print("1. Verifie ton fichier .env")
        print("2. Si Meta credentials manquent, suis: GUIDE_META_WHATSAPP_SETUP.md")
        print("3. Installer les packages manquants: pip install -r requirements.txt")

    print("\n")

if __name__ == "__main__":
    main()
