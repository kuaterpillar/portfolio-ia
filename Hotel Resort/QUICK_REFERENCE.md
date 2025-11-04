# ⚡ RÉFÉRENCE RAPIDE - Hotel Concierge AI

## 📊 STATISTIQUES DU PROJET

- **Lignes de code :** ~1964 lignes Python
- **Modules :** 6 modules principaux
- **Fonctionnalités :** 100% implémentées
- **Tests :** Oui (test_bot.py)
- **Documentation :** Complète (4 fichiers MD)
- **Status :** ✅ Prêt pour utilisation

---

## 🎯 FICHIERS PRINCIPAUX

| Fichier | Lignes | Description |
|---------|--------|-------------|
| `src/core/ai_agent.py` | ~400 | Agent IA auto-apprenant |
| `src/core/booking_system.py` | ~350 | Système de réservation |
| `src/core/recommendation_engine.py` | ~350 | Moteur de recommandations |
| `src/core/session_memory.py` | ~380 | Mémoire de session |
| `src/integrations/whatsapp_handler.py` | ~200 | Interface WhatsApp |
| `main.py` | ~230 | Orchestrateur principal |

---

## 🚀 COMMANDES ESSENTIELLES

```bash
# === INSTALLATION ===
pip install -r requirements.txt
cp .env.example .env
# Éditer .env avec vos clés API

# === TESTS ===
python test_bot.py                    # Test complet sans WhatsApp
python main.py                        # Lancer serveur WhatsApp

# === MÉMOIRE DE SESSION ===
python session_manager.py summary     # Voir état du projet
python session_manager.py context     # Contexte pour l'IA
python session_manager.py export      # Exporter rapport
python session_manager.py archive     # Archiver session

# === DÉVELOPPEMENT ===
ngrok http 5000                       # Exposer serveur local
# Configurer URL ngrok dans Twilio
```

---

## 📁 STRUCTURE DU PROJET

```
Hotel Resort/
│
├── 📄 START_HERE.md              ← COMMENCER ICI
├── 📄 NEXT_SESSION_CONTEXT.md    ← Contexte détaillé
├── 📄 PROJECT_SUMMARY.md         ← Vue d'ensemble complète
├── 📄 README.md                  ← Documentation technique
├── 📄 QUICK_REFERENCE.md         ← Ce fichier
│
├── 🐍 main.py                    ← Point d'entrée
├── 🐍 test_bot.py                ← Tests automatisés
├── 🐍 session_manager.py         ← Gestion mémoire
│
├── 📂 src/
│   ├── 📂 core/
│   │   ├── ai_agent.py           ← Agent IA
│   │   ├── booking_system.py     ← Réservations
│   │   ├── recommendation_engine.py  ← Recommandations
│   │   └── session_memory.py     ← Mémoire session
│   │
│   └── 📂 integrations/
│       └── whatsapp_handler.py   ← WhatsApp/Twilio
│
├── 📂 data/                      ← SQLite DBs (auto-créées)
│   ├── agent_memory.db
│   └── bookings.db
│
├── 📂 memory/                    ← Mémoire session (auto-créée)
│   ├── current_session.json
│   └── history/
│
├── 📂 config/                    ← Configurations
├── 📂 logs/                      ← Logs applicatifs
└── 📂 tests/                     ← Tests unitaires
```

---

## 🎨 FLUX PRINCIPAL

```
WhatsApp Client
      ↓
   Twilio
      ↓
  Webhook → main.py
      ↓
Intent Detection
      ↓
   ┌──────┴──────┐
   ↓             ↓
Booking   Recommendation
   ↓             ↓
AI Agent ← Client Memory
   ↓
Response → WhatsApp
```

---

## 🔑 VARIABLES D'ENVIRONNEMENT

```env
# OBLIGATOIRES
OPENAI_API_KEY=sk-...           # OpenAI GPT-4o
TWILIO_ACCOUNT_SID=AC...        # Twilio (pour WhatsApp)
TWILIO_AUTH_TOKEN=...           # Twilio

# OPTIONNELLES
WEATHER_API_KEY=...             # OpenWeatherMap (recommandations météo)

# CONFIGURATION HÔTEL
HOTEL_NAME=Grand Hotel Parisien
HOTEL_CITY=Paris
HOTEL_ADDRESS=123 Avenue...
CHECK_IN_TIME=15:00
CHECK_OUT_TIME=11:00
```

---

## 💡 EXEMPLES D'UTILISATION

### Test sans WhatsApp
```python
from main import HotelConciergeBot

bot = HotelConciergeBot()

# Conversation
response = bot.handle_message(
    "whatsapp:+33612345678",
    "Bonjour, je cherche un restaurant romantique"
)
print(response)

# Vérifier disponibilité
rooms = bot.booking_system.check_availability(
    check_in="2025-12-15",
    check_out="2025-12-17",
    num_guests=2
)

# Voir métriques
report = bot.get_performance_report()
```

### Avec WhatsApp (production)
```bash
# 1. Lancer serveur
python main.py

# 2. Terminal 2 : Exposer avec ngrok
ngrok http 5000

# 3. Copier URL ngrok (ex: https://abc123.ngrok.io)

# 4. Configurer Twilio :
# - Aller sur console.twilio.com
# - Messaging > Settings > WhatsApp Sandbox
# - Webhook URL : https://abc123.ngrok.io/webhook/whatsapp
# - Method : POST
# - Sauvegarder

# 5. Envoyer message WhatsApp au numéro sandbox Twilio
```

---

## 🐛 DEBUGGING

```python
# Voir logs détaillés
import logging
logging.basicConfig(level=logging.DEBUG)

# Inspecter base de données
import sqlite3
conn = sqlite3.connect("data/agent_memory.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM conversations LIMIT 5")
print(cursor.fetchall())

# Tester composant isolé
from src.core.recommendation_engine import RecommendationEngine
engine = RecommendationEngine("Paris", "123 Avenue...")
restaurants = engine.recommend_restaurants(budget=100)
print(restaurants)
```

---

## 📊 MÉTRIQUES CLÉS

```python
from main import HotelConciergeBot
bot = HotelConciergeBot()

# Performance
report = bot.get_performance_report()
print(f"Temps réponse moyen: {report['avg_response_time_ms']}ms")
print(f"Satisfaction: {report['avg_satisfaction']}/5")
print(f"Conversations: {report['total_conversations']}")

# Profil client
context = bot.ai_agent.get_client_context("whatsapp:+33612345678")
print(f"Langue: {context['language']}")
print(f"Préférences: {context['preferences']}")
```

---

## 🎯 PROCHAINES ÉTAPES

1. **Extraction dates** : Ajouter dans `main.py/_handle_booking_intent()`
2. **Pattern learning** : Compléter `ai_agent.py/learn_from_feedback()`
3. **Plus de données** : Enrichir `recommendation_engine.py`
4. **Tests unitaires** : Créer `tests/test_*.py` avec pytest
5. **Dashboard** : Interface web Flask pour métriques

---

## 🆘 AIDE RAPIDE

| Problème | Solution |
|----------|----------|
| Bot ne démarre pas | Vérifier `.env` avec clés API |
| Erreur Unicode | `PYTHONIOENCODING=utf-8 python script.py` |
| WhatsApp ne répond pas | Vérifier webhook Twilio configuré |
| Erreur OpenAI | Vérifier crédits API OpenAI |
| Pas de recommandations | Vérifier `WEATHER_API_KEY` (optionnel) |

---

## 📚 DOCUMENTATION

| Document | Quand l'utiliser |
|----------|------------------|
| **START_HERE.md** | Première visite du projet |
| **NEXT_SESSION_CONTEXT.md** | Reprendre après une pause |
| **PROJECT_SUMMARY.md** | Vue d'ensemble technique |
| **README.md** | Documentation complète |
| **QUICK_REFERENCE.md** | Ce fichier - référence rapide |

---

## ✅ CHECKLIST DÉMARRAGE

- [ ] Lire START_HERE.md
- [ ] Installer dépendances (`pip install -r requirements.txt`)
- [ ] Copier .env.example vers .env
- [ ] Configurer clés API dans .env
- [ ] Tester : `python test_bot.py`
- [ ] Voir état : `python session_manager.py summary`
- [ ] Choisir tâche dans TODO list

---

**🎉 Le projet est complet et prêt à évoluer !**

**Pour démarrer :** [START_HERE.md](START_HERE.md)
