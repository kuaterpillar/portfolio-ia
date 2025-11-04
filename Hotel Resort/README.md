# 🏨 Hotel Concierge AI - WhatsApp Bot

Un concierge IA intelligent qui s'améliore automatiquement au fil du temps, disponible 24/7 via WhatsApp pour assister vos clients.

## ✨ Fonctionnalités principales

### 🤖 Agent IA auto-apprenant
- **Mémoire persistante** : Se souvient des préférences de chaque client
- **Optimisation continue** : Analyse les conversations réussies pour s'améliorer
- **Métriques de performance** : Suivi du taux de satisfaction et temps de réponse
- **Adaptation automatique** : Détecte la langue et personnalise les réponses

### 💬 Communication WhatsApp
- Messages en temps réel via Twilio
- Support multilingue automatique (FR, EN, ES, IT, DE)
- Templates pour les notifications hors fenêtre 24h
- Messages d'accueil et sondages de satisfaction automatisés

### 🎯 Recommandations intelligentes
- **Restaurants** : Filtrage par budget, cuisine, ambiance
- **Activités** : Suggestions basées sur la météo en temps réel
- **Services hôtel** : Spa, navette, late check-out...
- Base de données locale facilement extensible

### 📅 Système de réservation
- Vérification de disponibilité en temps réel
- Gestion des chambres par type (Simple, Double, Suite...)
- Confirmation et annulation de réservations
- Historique complet par client

## 🚀 Installation

### Prérequis
- Python 3.9+
- Compte Twilio avec WhatsApp activé
- Clé API OpenAI
- (Optionnel) Clé API OpenWeatherMap pour les recommandations météo

### Configuration

1. **Cloner et installer les dépendances**
```bash
pip install -r requirements.txt
```

2. **Configurer les variables d'environnement**

Copier `.env.example` vers `.env` et remplir :
```bash
cp .env.example .env
```

Éditer `.env` avec vos clés :
```env
# OpenAI
OPENAI_API_KEY=sk-...

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Configuration hôtel
HOTEL_NAME=Grand Hotel Parisien
HOTEL_CITY=Paris
HOTEL_ADDRESS=123 Avenue des Champs-Élysées, 75008 Paris
...
```

3. **Lancer le serveur**
```bash
python main.py
```

Le serveur démarre sur `http://localhost:5000`

## 🔗 Configuration Twilio

1. Aller sur [Twilio Console](https://console.twilio.com/)
2. Dans **Messaging > Settings > WhatsApp sandbox**
3. Configurer le webhook :
   - URL : `https://votre-domaine.com/webhook/whatsapp`
   - Méthode : `POST`

**Pour le développement local**, utiliser [ngrok](https://ngrok.com/) :
```bash
ngrok http 5000
```
Puis utiliser l'URL ngrok dans Twilio.

## 📊 Architecture du système

```
Hotel Resort/
├── main.py                    # Point d'entrée principal
├── src/
│   ├── core/
│   │   ├── ai_agent.py       # Agent IA auto-apprenant
│   │   ├── booking_system.py  # Gestion réservations
│   │   └── recommendation_engine.py  # Recommandations
│   └── integrations/
│       └── whatsapp_handler.py  # Interface WhatsApp/Twilio
├── data/                      # Bases de données SQLite
│   ├── agent_memory.db       # Conversations et apprentissage
│   └── bookings.db           # Réservations
├── config/                    # Configurations
└── logs/                      # Logs applicatifs
```

## 💡 Utilisation

### Scénarios typiques

#### 1. Avant l'arrivée
Envoyer un message de bienvenue :
```python
bot = HotelConciergeBot()
bot.send_welcome_to_client("whatsapp:+33612345678", "Jean Dupont")
```

#### 2. Pendant le séjour
Le client envoie : *"Je cherche un restaurant romantique, budget 80€/personne"*

Le bot répond avec des suggestions personnalisées basées sur :
- Budget spécifié
- Préférences passées du client
- Proximité de l'hôtel

#### 3. Après le départ
Envoyer un sondage de satisfaction :
```python
bot.send_checkout_survey("whatsapp:+33612345678", "Jean Dupont")
```

### Exemples de demandes comprises

```
✅ "Avez-vous une chambre double du 12 au 15 novembre ?"
✅ "Quels sont les horaires du petit-déjeuner ?"
✅ "Je cherche un restaurant italien dans le 8e"
✅ "Il pleut demain, que faire ?"
✅ "Pouvez-vous me réserver un taxi pour CDG à 7h ?"
```

## 🧠 Système d'apprentissage

L'agent IA s'améliore automatiquement en :

1. **Stockant chaque conversation** avec métadonnées (temps de réponse, contexte)
2. **Analysant les patterns réussis** (taux de satisfaction élevé)
3. **Ajustant dynamiquement** le prompt système selon les patterns appris
4. **Mémorisant les préférences** clients (langue, budget, style d'activités)

### Métriques suivies
- Temps de réponse moyen
- Taux de satisfaction client
- Nombre de réservations réussies
- Escalades vers personnel humain

Accéder aux métriques :
```python
bot = HotelConciergeBot()
report = bot.get_performance_report()
print(report)
```

## 🎨 Personnalisation

### Ajouter des restaurants/activités

Éditer `src/core/recommendation_engine.py` :

```python
"restaurants": [
    {
        "name": "Mon Nouveau Restaurant",
        "type": "gastronomique",
        "cuisine": "française",
        "price_range": "€€€",
        "avg_price_per_person": 90,
        ...
    }
]
```

### Modifier la personnalité du bot

Éditer le prompt système dans `src/core/ai_agent.py`, méthode `_build_system_prompt()`.

### Ajouter des types de chambres

Les chambres sont dans la base de données. Pour les modifier :
1. Supprimer `data/bookings.db`
2. Éditer `src/core/booking_system.py`, méthode `_init_database()`
3. Relancer l'application

## 🔒 Sécurité & RGPD

- Les données clients sont stockées localement dans SQLite
- Pas de conservation inutile de données sensibles
- Les conversations peuvent être supprimées automatiquement après X jours
- Respecte la fenêtre de 24h de WhatsApp pour les messages non-template

## 🐛 Dépannage

### Le bot ne répond pas
- Vérifier que le serveur Flask est lancé
- Vérifier l'URL du webhook dans Twilio
- Vérifier les logs : `tail -f logs/app.log`

### Erreur OpenAI API
- Vérifier que `OPENAI_API_KEY` est correcte
- Vérifier les crédits OpenAI disponibles

### Erreur Twilio
- Vérifier `TWILIO_ACCOUNT_SID` et `TWILIO_AUTH_TOKEN`
- Vérifier que WhatsApp est activé sur le compte Twilio

## 📈 Évolutions futures

- [ ] Interface web d'administration
- [ ] Support de plus de langues
- [ ] Intégration avec systèmes PMS existants
- [ ] Chatbot vocal (WhatsApp voice messages)
- [ ] Analytics dashboard temps réel
- [ ] A/B testing automatique des réponses

## 🤝 Support

Pour toute question ou problème, contacter l'équipe de développement.

## 📄 Licence

Propriétaire - Tous droits réservés
