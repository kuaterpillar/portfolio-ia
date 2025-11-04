# 🚀 Démarrage Rapide - Connexion WhatsApp

## ✅ Ce qui a été fait

Le code est maintenant prêt pour **Meta WhatsApp Business API** :

- ✅ Nouveau handler Meta créé : [whatsapp_handler_meta.py](src/integrations/whatsapp_handler_meta.py)
- ✅ Support multi-provider (Meta + Twilio) : [main.py](main.py)
- ✅ Variables d'environnement configurées : [.env](.env)
- ✅ Guide complet créé : [GUIDE_META_WHATSAPP_SETUP.md](GUIDE_META_WHATSAPP_SETUP.md)

---

## 🎯 Prochaines étapes (Dans l'ordre)

### 1️⃣ Obtenir les credentials Meta (30 min)

Suis le guide détaillé : [GUIDE_META_WHATSAPP_SETUP.md](GUIDE_META_WHATSAPP_SETUP.md)

**En résumé :**
1. Crée un compte Meta Business : [business.facebook.com](https://business.facebook.com)
2. Crée une application : [developers.facebook.com](https://developers.facebook.com)
3. Ajoute le produit **WhatsApp Business**
4. Récupère :
   - `ACCESS_TOKEN` (dans "Démarrage rapide")
   - `PHONE_NUMBER_ID` (sous le numéro de téléphone)

### 2️⃣ Configurer le .env

Édite [.env](.env) et remplace :

```env
META_WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxx  # ← Ton token Meta
META_WHATSAPP_PHONE_NUMBER_ID=123456789012345  # ← Ton phone ID
```

### 3️⃣ Installer ngrok (si pas déjà fait)

```bash
# Windows : Télécharge depuis https://ngrok.com/download
# Ou avec Chocolatey :
choco install ngrok

# Vérifie l'installation
ngrok version
```

### 4️⃣ Lancer le système

**Terminal 1 - Serveur Roomie :**
```bash
cd "c:\Users\kuate\Desktop\Hotel Resort"
python main.py
```

Tu devrais voir :
```
📱 Using Meta WhatsApp Business API
✅ Agent IA chargé (avec mémoire conversationnelle)
✅ Moteur de recommandations chargé
✅ WhatsApp handler chargé
🏨 Hôtel 121 Paris Concierge AI initialisé!
🚀 Starting webhook server on port 5000...
```

**Terminal 2 - Ngrok :**
```bash
ngrok http 5000
```

Tu obtiendras une URL comme :
```
Forwarding  https://abc123.ngrok.io -> http://localhost:5000
```

**⚠️ NOTE CETTE URL** : `https://abc123.ngrok.io`

### 5️⃣ Configurer le webhook Meta

1. Va dans ton application Meta : [developers.facebook.com/apps](https://developers.facebook.com/apps)
2. **WhatsApp** > **Configuration** > **Webhooks** > **Modifier**
3. **Callback URL** : `https://abc123.ngrok.io/webhook/whatsapp`
4. **Verify Token** : `roomie_hotel_webhook_2025`
5. Clique sur **"Vérifier et enregistrer"**

✅ Tu devrais voir **"Webhook vérifié"**

### 6️⃣ Ajouter ton numéro de test

1. **WhatsApp** > **Démarrage rapide**
2. Section **"Numéros de téléphone de test"**
3. Ajoute ton numéro personnel (ex: `+33612345678`)
4. Entre le code SMS reçu

### 7️⃣ Tester !

1. Ouvre WhatsApp sur ton téléphone
2. Nouveau message vers le numéro Meta (visible dans "Démarrage rapide")
3. Envoie : **"Bonjour"**

🎉 **Roomie devrait te répondre !**

---

## 🔍 Vérifier que ça marche

Dans le terminal où tourne `python main.py`, tu devrais voir :

```
Received message from Marie (+33612345678): Bonjour
📨 Message from whatsapp:+33612345678: Bonjour
🤖 Response: Bonjour ! Bienvenue à l'Hôtel 121 Paris...
⚡ Response time: 850ms
Message sent successfully. Message ID: wamid.xxx
```

---

## ⚠️ Problèmes courants

### Roomie ne répond pas

**Checklist :**
- [ ] `python main.py` est lancé dans terminal 1
- [ ] `ngrok http 5000` est lancé dans terminal 2
- [ ] Le webhook est configuré dans Meta avec l'URL ngrok
- [ ] Ton numéro est dans les numéros de test
- [ ] L'`OPENAI_API_KEY` est valide dans `.env`

### "Webhook verification failed"

- Vérifie que le **Verify Token** est identique dans `.env` et dans Meta
- Valeur par défaut : `roomie_hotel_webhook_2025`

### "Invalid access token"

- Le token temporaire expire après 24h
- Génère un token permanent (voir [GUIDE_META_WHATSAPP_SETUP.md](GUIDE_META_WHATSAPP_SETUP.md) - Étape 8)

---

## 📚 Documentation complète

Pour plus de détails, consulte :
- [GUIDE_META_WHATSAPP_SETUP.md](GUIDE_META_WHATSAPP_SETUP.md) - Guide complet pas à pas
- [README.md](README.md) - Documentation technique du projet
- [MEMORY_SYSTEM_GUIDE.md](MEMORY_SYSTEM_GUIDE.md) - Comment fonctionne la mémoire

---

## 🎯 Exemple de conversation

Une fois connecté, tu peux tester :

```
👤 Toi : Bonjour
🤖 Roomie : Bonjour ! Bienvenue à l'Hôtel 121 Paris 👋
           Je suis Roomie, votre concierge virtuel...

👤 Toi : Je m'appelle Sophie
🤖 Roomie : Ravi de vous rencontrer Sophie ! Comment puis-je vous aider ?

👤 Toi : Je cherche un restaurant italien
🤖 Roomie : Avec plaisir ! Côté ambiance, vous voyez plutôt :
           🕯️ Romantique
           👥 Convivial
           ✨ Chic

👤 Toi : Romantique
🤖 Roomie : Parfait ! Et niveau budget, vous pensez à combien par personne ?

👤 Toi : 50€
🤖 Roomie : Très bien, dans votre budget de 50€/personne, voici 3 restaurants...
```

---

**✅ Une fois que tu as les credentials Meta, la connexion prend 5 minutes !**

**Des questions ? Reviens vers moi !**
