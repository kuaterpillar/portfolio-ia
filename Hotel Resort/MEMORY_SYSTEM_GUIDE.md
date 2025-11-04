# 🧠 GUIDE DU SYSTÈME DE MÉMOIRE CONVERSATIONNELLE

## 📌 PROBLÈME RÉSOLU

**Besoin :** Le bot doit se souvenir de chaque conversation individuelle sans confondre les clients entre eux.

**Solution :** Mémoire conversationnelle isolée par numéro de téléphone + chargement automatique des 10 derniers messages.

---

## ✅ COMMENT ÇA FONCTIONNE

### 🔒 Isolation par client

Chaque numéro WhatsApp = Une mémoire séparée

```
Client A (+33612345678)
├── Message 1: "Bonjour, je m'appelle Marie"
├── Réponse 1: "Bonjour Marie ! Comment puis-je vous aider ?"
├── Message 2: "Je cherche un restaurant"
└── Réponse 2: "Avec plaisir Marie ! Quel type de cuisine ?"

Client B (+33687654321)
├── Message 1: "Salut, moi c'est Jean"
├── Réponse 1: "Bonjour Jean ! Que puis-je faire pour vous ?"
├── Message 2: "Je veux du japonais"
└── Réponse 2: "Très bon choix Jean ! Voici mes suggestions..."
```

**→ Le bot ne confondra JAMAIS Marie et Jean**

---

### 💾 Stockage automatique

À chaque échange, le système stocke dans SQLite :

| Colonne | Valeur | Usage |
|---------|--------|-------|
| `client_phone` | whatsapp:+33612345678 | Identifiant unique |
| `message_text` | "Je cherche un restaurant" | Message client |
| `response_text` | "Quel type de cuisine ?" | Réponse bot |
| `timestamp` | 2025-10-14 17:30:45 | Horodatage |
| `language` | fr | Langue détectée |
| `context_used` | {...} | Contexte appliqué |

**Base de données :** `data/agent_memory.db` (créée automatiquement)

---

### 🔄 Chargement du contexte

Quand un client envoie un message :

```python
# 1. Le système récupère les 10 derniers messages de CE CLIENT
conversation_history = get_recent_conversation(phone, limit=10)

# 2. Construit la conversation pour l'IA
messages = [
    {"role": "system", "content": "Tu es le concierge..."},
    {"role": "user", "content": "Bonjour"},
    {"role": "assistant", "content": "Bonjour ! ..."},
    {"role": "user", "content": "Je cherche un restaurant"},
    {"role": "assistant", "content": "Quel type de cuisine ?"},
    # ... jusqu'à 10 messages
    {"role": "user", "content": message_actuel}  # Nouveau message
]

# 3. L'IA génère la réponse AVEC tout le contexte
response = openai.chat.completions.create(messages=messages)
```

---

## 🎯 EXEMPLES CONCRETS

### Exemple 1 : Continuité de conversation

```
👤 Marie: Bonjour
🤖 Bot: Bonjour ! Comment puis-je vous aider ?

👤 Marie: Je cherche un restaurant romantique
🤖 Bot: Excellente idée ! Quel est votre budget approximatif par personne ?

👤 Marie: 80 euros
🤖 Bot: Parfait ! Voici mes recommandations dans votre budget de 80€...
      1. Le Gourmet Parisien (120€)
      2. Bistrot du Coin (35€)
      3. Sushi Zen (65€)

👤 Marie: Le dernier m'intéresse
🤖 Bot: Excellent choix Marie ! Le Sushi Zen est à 65€/personne...
      [Le bot SAIT que "le dernier" = Sushi Zen de sa liste]
```

**→ Le bot comprend "le dernier" car il a la mémoire de sa propre liste**

---

### Exemple 2 : Pas de confusion entre clients

**Simultanément :**

```
👤 Marie: Mon budget est 80 euros
🤖 → Marie: Parfait ! Dans votre budget de 80€...

👤 Jean: Mon budget est 40 euros
🤖 → Jean: Très bien ! Dans votre budget de 40€...

👤 Marie: Vous vous souvenez de mon budget ?
🤖 → Marie: Oui bien sûr, 80 euros par personne !

👤 Jean: Et le mien ?
🤖 → Jean: Votre budget est de 40 euros par personne !
```

**→ Aucune confusion, chaque client a sa propre mémoire**

---

## 🔧 CONFIGURATION ACTUELLE

### Paramètres de mémoire

| Paramètre | Valeur | Impact |
|-----------|--------|--------|
| **Messages historiques** | 10 | Nombre de messages chargés |
| **Base de données** | SQLite | Stockage local |
| **Isolation** | Par téléphone | Un client = Une mémoire |
| **Détection langue** | Automatique | FR, EN, ES, IT, DE |

### Fichiers concernés

- **[src/core/ai_agent.py](src/core/ai_agent.py)** : Logique de mémoire (lignes 320-344)
- **[main.py](main.py)** : Orchestration (ligne 86-88)
- **data/agent_memory.db** : Base de données (auto-créée)

---

## 🧪 TESTER LA MÉMOIRE

### Test rapide

```bash
python test_conversation_memory.py
```

Ce script teste :
✅ Continuité de conversation (6 messages)
✅ Pas de confusion entre clients
✅ Bascule rapide entre clients
✅ Stats de mémoire

### Test manuel

```python
from main import HotelConciergeBot

bot = HotelConciergeBot()

# Client 1
bot.handle_message("whatsapp:+33612345678", "Bonjour, je m'appelle Marie")
bot.handle_message("whatsapp:+33612345678", "Mon budget est 80 euros")
bot.handle_message("whatsapp:+33612345678", "Vous vous souvenez de mon budget ?")
# → Devrait répondre "Oui, 80 euros"

# Client 2
bot.handle_message("whatsapp:+33687654321", "Salut, moi c'est Jean")
bot.handle_message("whatsapp:+33687654321", "Mon budget est 40 euros")
bot.handle_message("whatsapp:+33687654321", "C'était quoi mon budget ?")
# → Devrait répondre "40 euros" (pas 80)
```

---

## 📊 VÉRIFIER LA MÉMOIRE EN BASE

```python
import sqlite3

conn = sqlite3.connect("data/agent_memory.db")
cursor = conn.cursor()

# Voir les conversations d'un client
cursor.execute("""
    SELECT message_text, response_text, timestamp
    FROM conversations
    WHERE client_phone = 'whatsapp:+33612345678'
    ORDER BY timestamp DESC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(f"Client: {row[0]}")
    print(f"Bot: {row[1]}")
    print(f"Date: {row[2]}")
    print("-" * 50)

conn.close()
```

---

## 🎛️ PERSONNALISER LA MÉMOIRE

### Changer le nombre de messages historiques

Dans [src/core/ai_agent.py](src/core/ai_agent.py) ligne 290 :

```python
# Avant
conversation_history = self._get_recent_conversation(phone, limit=10)

# Après (pour 20 messages)
conversation_history = self._get_recent_conversation(phone, limit=20)
```

**Note :** Plus de messages = Plus de contexte mais plus de tokens (coût OpenAI)

### Ajouter un profil client riche

```python
# Mettre à jour le profil
bot.ai_agent.update_client_profile(phone, {
    "name": "Marie Dubois",
    "language": "fr",
    "preferences": {
        "cuisine_favorite": "japonais",
        "budget_moyen": "80€",
        "style": "romantique"
    },
    "allergies": "gluten"
})

# Le bot utilisera ces infos automatiquement
```

---

## 🚀 AMÉLIORATIONS POSSIBLES

### 1. Résumé automatique

Pour les longues conversations, résumer les anciens messages :

```python
def summarize_old_messages(phone):
    """Condenser les messages > 30 jours en résumé"""
    # Résumer 100 vieux messages en 2-3 phrases
    # Économise des tokens tout en gardant l'essentiel
```

### 2. Oubli programmé

Effacer les conversations après X jours (RGPD) :

```python
def cleanup_old_conversations(days=90):
    """Supprimer les conversations de plus de 90 jours"""
    cursor.execute("""
        DELETE FROM conversations
        WHERE timestamp < datetime('now', '-90 days')
    """)
```

### 3. Export de conversation

```python
def export_conversation(phone, output_file):
    """Exporter une conversation en JSON ou PDF"""
    # Utile pour le service client
```

---

## 🔒 SÉCURITÉ & RGPD

✅ **Données stockées localement** (SQLite)
✅ **Un téléphone = Une identité** (anonyme)
✅ **Pas de données sensibles** stockées par défaut
⚠️ **À faire** : Ajouter un système d'oubli automatique (90 jours)

---

## ❓ FAQ

**Q : Que se passe-t-il si un client supprime la conversation WhatsApp ?**
R : Le bot garde la mémoire en base. Le client peut reprendre où il s'est arrêté.

**Q : La mémoire ralentit-elle le bot ?**
R : Non, la requête SQL est très rapide (<5ms). Le coût est surtout les tokens OpenAI.

**Q : Peut-on utiliser Redis au lieu de SQLite ?**
R : Oui ! Il suffit de modifier `src/core/ai_agent.py` pour utiliser Redis comme cache.

**Q : Comment effacer la mémoire d'un client ?**
R :
```python
cursor.execute("DELETE FROM conversations WHERE client_phone = ?", (phone,))
```

---

**✅ Le système de mémoire est maintenant actif et testé !**

**Pour tester :** `python test_conversation_memory.py`
