# 📱 Guide de Configuration Meta WhatsApp Business API

Ce guide t'accompagne étape par étape pour connecter Roomie à WhatsApp via Meta Business.

---

## 🎯 Ce dont tu as besoin

1. Un compte Facebook Business
2. Un numéro de téléphone dédié (pas utilisé sur WhatsApp actuellement)
3. Un serveur accessible publiquement (on utilisera ngrok pour les tests)

---

## 📝 ÉTAPE 1 : Créer un compte Meta Business

### 1.1 Créer un Meta Business Manager

1. Va sur [business.facebook.com](https://business.facebook.com)
2. Clique sur **"Créer un compte"**
3. Entre les informations de ton hôtel :
   - Nom : **Hôtel 121 Paris** (ou ton nom)
   - Ton nom
   - Email professionnel

### 1.2 Vérifier ton compte

Meta va te demander de vérifier ton compte :
- Vérification email (reçois un code)
- Éventuellement vérification d'identité (carte d'identité)

⏱️ **Temps d'attente** : La vérification peut prendre 24-48h

---

## 📝 ÉTAPE 2 : Créer une application Meta

### 2.1 Accéder au Meta for Developers

1. Va sur [developers.facebook.com](https://developers.facebook.com)
2. Connecte-toi avec ton compte Facebook
3. Clique sur **"Mes applications"** (en haut à droite)
4. Clique sur **"Créer une application"**

### 2.2 Configurer l'application

1. **Type d'application** : Sélectionne **"Autre"**
2. **Cas d'usage** : Sélectionne **"Entreprise"**
3. **Nom de l'application** : `Roomie Concierge` (ou ce que tu veux)
4. **Email de contact** : Ton email
5. **Meta Business Account** : Sélectionne ton compte créé à l'étape 1
6. Clique sur **"Créer une application"**

---

## 📝 ÉTAPE 3 : Ajouter WhatsApp Business

### 3.1 Ajouter le produit WhatsApp

1. Dans ton application, cherche **"WhatsApp"** dans la liste des produits
2. Clique sur **"Configurer"** à côté de **"WhatsApp"**
3. Meta va te guider dans la configuration

### 3.2 Choisir le compte WhatsApp Business

Deux options :

**Option A : Créer un nouveau compte WhatsApp Business**
- Clique sur **"Créer un compte WhatsApp Business"**
- Nom du compte : `Hôtel 121 Paris`
- Fuseau horaire : `Europe/Paris`

**Option B : Utiliser un compte existant**
- Sélectionne ton compte WhatsApp Business existant

---

## 📝 ÉTAPE 4 : Obtenir les credentials

### 4.1 Obtenir le ACCESS TOKEN (temporaire pour tests)

1. Dans ton application, va dans **"WhatsApp" > "Démarrage rapide"**
2. Tu verras une section **"Access Token temporaire"**
3. **Copie ce token** → C'est ton `META_WHATSAPP_ACCESS_TOKEN`

⚠️ **Important** : Ce token expire après 24h. Pour la production, il faut créer un token permanent (voir étape 6).

### 4.2 Obtenir le PHONE NUMBER ID

1. Toujours dans **"Démarrage rapide"**
2. Tu verras une section **"Numéro de téléphone"**
3. En dessous du numéro, il y a un ID (ex: `123456789012345`)
4. **Copie cet ID** → C'est ton `META_WHATSAPP_PHONE_NUMBER_ID`

### 4.3 Configurer le .env

Ouvre ton fichier [.env](c:\Users\kuate\Desktop\Hotel Resort\.env) et remplace :

```env
META_WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
META_WHATSAPP_PHONE_NUMBER_ID=123456789012345
META_WEBHOOK_VERIFY_TOKEN=roomie_hotel_webhook_2025
```

---

## 📝 ÉTAPE 5 : Tester l'envoi de message (optionnel)

Avant de configurer les webhooks, tu peux tester l'envoi :

1. Dans **"Démarrage rapide"**, il y a une section **"Envoyer un message de test"**
2. Entre ton numéro de téléphone personnel (avec indicatif : +33...)
3. Clique sur **"Envoyer un message"**
4. Tu devrais recevoir un message WhatsApp de Meta !

---

## 📝 ÉTAPE 6 : Configurer le webhook

### 6.1 Exposer ton serveur local avec ngrok

```bash
# Dans un terminal, lance ngrok
ngrok http 5000
```

Tu obtiendras une URL comme : `https://abc123.ngrok.io`

**⚠️ Note cette URL, tu en auras besoin !**

### 6.2 Lancer le serveur Roomie

Dans un **autre terminal** :

```bash
cd "c:\Users\kuate\Desktop\Hotel Resort"
python main.py
```

Tu devrais voir :
```
📱 Using Meta WhatsApp Business API
🚀 Starting webhook server on port 5000...
📡 Webhook URL: http://localhost:5000/webhook/whatsapp
💡 Configure this URL in your Meta Business Console
   Verify Token: roomie_hotel_webhook_2025
```

### 6.3 Configurer le webhook dans Meta

1. Dans ton application Meta, va dans **"WhatsApp" > "Configuration"**
2. Section **"Webhooks"**, clique sur **"Modifier"**
3. **Callback URL** : `https://abc123.ngrok.io/webhook/whatsapp`
   - Remplace `abc123.ngrok.io` par ton URL ngrok
4. **Verify Token** : `roomie_hotel_webhook_2025`
   - (Ou la valeur dans ton .env si tu l'as changée)
5. Clique sur **"Vérifier et enregistrer"**

✅ Si tout est bon, tu verras **"Webhook vérifié"**

### 6.4 S'abonner aux événements

1. Toujours dans **"Webhooks"**
2. Section **"Champs de webhook"**
3. Clique sur **"Gérer"**
4. Abonne-toi à ces événements :
   - ✅ **messages** (obligatoire)
   - ✅ **message_status** (optionnel, pour voir si le message est lu)
5. Clique sur **"Enregistrer"**

---

## 📝 ÉTAPE 7 : Tester la conversation complète

### 7.1 Ajouter ton numéro de test

⚠️ **Important** : Par défaut, seuls certains numéros peuvent recevoir des messages.

1. Va dans **"WhatsApp" > "Démarrage rapide"**
2. Section **"Numéros de téléphone de test"**
3. Clique sur **"Ajouter un numéro de téléphone"**
4. Entre ton numéro : `+33612345678` (exemple)
5. Tu recevras un code par SMS → Entre-le
6. ✅ Ton numéro est maintenant autorisé !

### 7.2 Envoyer le premier message

1. Ouvre WhatsApp sur ton téléphone
2. **Nouveau message**
3. Entre le numéro Meta (visible dans "Démarrage rapide")
4. Envoie : **"Bonjour"**

🎉 **Roomie devrait te répondre !**

Si tu vois dans ton terminal :
```
Received message from Marie (+33612345678): Bonjour
🤖 Response: Bonjour ! Bienvenue à l'Hôtel 121 Paris...
```

**✅ C'EST CONNECTÉ !**

---

## 📝 ÉTAPE 8 : Créer un token permanent (pour production)

Le token temporaire expire après 24h. Pour la production :

### 8.1 Créer un utilisateur système

1. Va dans ton **Meta Business Manager**
2. **Paramètres du compte** > **Utilisateurs** > **Utilisateurs système**
3. Clique sur **"Ajouter"**
4. Nom : `Roomie Bot`
5. Rôle : **Administrateur**
6. Clique sur **"Créer un utilisateur système"**

### 8.2 Générer le token permanent

1. Sélectionne l'utilisateur système **"Roomie Bot"**
2. Clique sur **"Générer un nouveau token"**
3. Sélectionne ton application **"Roomie Concierge"**
4. Permissions nécessaires :
   - ✅ `whatsapp_business_management`
   - ✅ `whatsapp_business_messaging`
5. **Expire** : Sélectionne **"Jamais"**
6. Clique sur **"Générer le token"**
7. **⚠️ COPIE CE TOKEN IMMÉDIATEMENT** (il ne sera plus affiché)

### 8.3 Remplacer dans .env

```env
META_WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxx_TON_TOKEN_PERMANENT
```

---

## 🎛️ ÉTAPE 9 : Configuration avancée (optionnel)

### 9.1 Vérifier ton numéro de téléphone

Pour passer en production, Meta exige la vérification :

1. **WhatsApp** > **Paramètres**
2. **Numéros de téléphone** > Clique sur ton numéro
3. Clique sur **"Vérifier le numéro"**
4. Choisis la méthode (SMS ou appel vocal)
5. Entre le code reçu

### 9.2 Créer un profil Business

1. **WhatsApp** > **Paramètres**
2. **Profil de l'entreprise**
3. Remplis :
   - Photo de profil (logo hôtel)
   - Nom : `Hôtel 121 Paris`
   - Description : `Votre concierge IA 24/7`
   - Catégorie : `Hôtel`
   - Adresse : `121 Rue de la Boétie, 75008 Paris`
   - Site web : `https://hotel121paris.com`

### 9.3 Demander l'accès à la production

Pour envoyer des messages illimités :

1. **WhatsApp** > **Démarrage**
2. Clique sur **"Commencer la vérification"**
3. Meta va demander :
   - Vérification de l'entreprise (documents)
   - Vérification du numéro
   - Cas d'usage (décris le concierge IA)

⏱️ **Temps d'attente** : 1-2 semaines

---

## 🔧 DÉPANNAGE

### Problème : "Webhook verification failed"

**Solution :**
- Vérifie que ngrok tourne : `ngrok http 5000`
- Vérifie que le serveur Flask tourne : `python main.py`
- Vérifie le **Verify Token** dans `.env` et dans Meta (doivent être identiques)

### Problème : "Invalid phone number ID"

**Solution :**
- Va dans **WhatsApp > Démarrage rapide**
- Copie l'ID sous le numéro de téléphone
- Colle-le dans `.env` → `META_WHATSAPP_PHONE_NUMBER_ID`

### Problème : "Access token expired"

**Solution :**
- Si tu utilises le token temporaire, il expire après 24h
- Génère un token permanent (voir Étape 8)

### Problème : Roomie ne répond pas

**Checklist :**
- [ ] Le serveur Flask est lancé (`python main.py`)
- [ ] Ngrok est lancé (`ngrok http 5000`)
- [ ] Le webhook est configuré dans Meta (URL ngrok + verify token)
- [ ] Tu es abonné aux événements **"messages"**
- [ ] Ton numéro est dans les numéros de test autorisés
- [ ] L'`OPENAI_API_KEY` est valide dans `.env`

**Regarde les logs** dans le terminal où tourne `python main.py` :
```
Received message from +33612345678: Bonjour
```

Si ce message n'apparaît pas → Problème webhook
Si ce message apparaît mais pas de réponse → Problème OpenAI API

---

## 📊 RÉCAPITULATIF DES CREDENTIALS

Tu as besoin de 3 informations dans ton `.env` :

| Variable | Où la trouver | Exemple |
|----------|---------------|---------|
| `META_WHATSAPP_ACCESS_TOKEN` | Application Meta > WhatsApp > Démarrage rapide | `EAAxxxxx...` |
| `META_WHATSAPP_PHONE_NUMBER_ID` | Sous le numéro de téléphone dans Démarrage rapide | `123456789012345` |
| `META_WEBHOOK_VERIFY_TOKEN` | Tu le définis toi-même (dans .env ET dans Meta) | `roomie_hotel_webhook_2025` |

---

## 🚀 PROCHAINES ÉTAPES

Une fois que tout fonctionne :

1. **Teste la conversation complète** (voir l'exemple dans le README)
2. **Personnalise le profil WhatsApp** (photo, description)
3. **Crée des templates pré-approuvés** pour les messages automatiques
4. **Passe en production** (vérification Meta + token permanent)

---

## 💡 RESSOURCES

- [Documentation Meta WhatsApp API](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Meta Business Manager](https://business.facebook.com)
- [Meta for Developers](https://developers.facebook.com)
- [Guide ngrok](https://ngrok.com/docs)

---

**✅ Si tu suis ce guide, Roomie sera connecté à WhatsApp en 30 minutes !**

**Des questions ? Reviens vers moi à n'importe quelle étape.**
