# Système de Tri Automatique d'Emails - Conciergerie

## Description
Système automatisé pour trier et classer 500+ emails/jour par ordre d'importance pour entreprise de conciergerie.

## Fonctionnalités
- **Classification automatique** en 4 niveaux de priorité
- **Interface graphique** pour visualisation et gestion
- **Base de données** SQLite pour stockage
- **IA optionnelle** avec OpenAI pour classification avancée
- **Statistiques** en temps réel

## Niveaux de Priorité
1. **URGENT** - Urgences, pannes, réclamations graves
2. **HAUTE** - Nouvelles demandes, réservations, RDV
3. **MOYENNE** - Confirmations, demandes d'info
4. **BASSE** - Newsletters, promotions, spam

## Installation

### Prérequis
- Python 3.8+
- Compte email avec IMAP activé

### Étapes
1. Installer les dépendances:
```bash
pip install -r requirements.txt
```

2. Configurer vos identifiants dans `config.env`:
```
EMAIL_ADDRESS=votre@email.com
EMAIL_PASSWORD=votre_mot_de_passe_application
IMAP_SERVER=imap.gmail.com
OPENAI_API_KEY=sk-xxx (optionnel)
```

## Utilisation

### Lancement de l'interface
```bash
python interface.py
```

### Classification manuelle
```bash
python email_classifier.py
```

## Configuration Gmail
1. Activer l'authentification à 2 facteurs
2. Générer un mot de passe d'application
3. Utiliser ce mot de passe dans la configuration

## Sécurité
- Mots de passe stockés en variables d'environnement
- Connexion SSL/TLS sécurisée
- Base de données locale

## Support
- Gmail, Outlook, Yahoo Mail
- Serveurs IMAP personnalisés