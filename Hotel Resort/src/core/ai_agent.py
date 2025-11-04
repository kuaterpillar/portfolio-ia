"""
AI Agent with self-learning capabilities for Hotel Concierge
Evolves over time by analyzing conversation patterns and success metrics
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from pathlib import Path


class SelfLearningAgent:
    """
    Intelligent agent that improves through:
    - Conversation analysis and pattern recognition
    - Performance metrics tracking (response time, satisfaction scores)
    - Dynamic prompt optimization based on success patterns
    - Context-aware memory across sessions
    """

    def __init__(self, hotel_config: Dict, db_path: str = "data/agent_memory.db"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.hotel_config = hotel_config
        self.db_path = db_path
        self.model = "gpt-4o"  # Latest model for best performance

        # Initialize database for learning
        self._init_database()

        # Load learned patterns
        self.learned_patterns = self._load_learned_patterns()
        self.performance_metrics = self._load_performance_metrics()

    def _init_database(self):
        """Initialize SQLite database for conversation history and learning"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_phone TEXT NOT NULL,
                message_text TEXT NOT NULL,
                response_text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                language TEXT,
                satisfaction_score REAL,
                response_time_ms INTEGER,
                context_used TEXT
            )
        """)

        # Client profiles table (memory across sessions)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS client_profiles (
                phone TEXT PRIMARY KEY,
                name TEXT,
                language TEXT,
                preferences TEXT,
                budget_range TEXT,
                activity_style TEXT,
                allergies TEXT,
                last_interaction DATETIME,
                total_interactions INTEGER DEFAULT 0,
                avg_satisfaction REAL
            )
        """)

        # Performance patterns table (learning storage)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                success_rate REAL,
                usage_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Performance metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                date TEXT PRIMARY KEY,
                avg_response_time_ms REAL,
                avg_satisfaction REAL,
                total_conversations INTEGER,
                successful_bookings INTEGER,
                escalations_to_human INTEGER
            )
        """)

        conn.commit()
        conn.close()

    def _load_learned_patterns(self) -> Dict:
        """Load previously learned successful patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT pattern_type, pattern_data, success_rate
            FROM learned_patterns
            WHERE success_rate > 0.7
            ORDER BY success_rate DESC
        """)

        patterns = {}
        for row in cursor.fetchall():
            pattern_type, pattern_data, success_rate = row
            patterns[pattern_type] = json.loads(pattern_data)

        conn.close()
        return patterns

    def _load_performance_metrics(self) -> Dict:
        """Load recent performance metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM performance_metrics
            ORDER BY date DESC LIMIT 7
        """)

        metrics = {"recent_week": []}
        for row in cursor.fetchall():
            metrics["recent_week"].append({
                "date": row[0],
                "avg_response_time": row[1],
                "avg_satisfaction": row[2],
                "conversations": row[3]
            })

        conn.close()
        return metrics

    def get_client_context(self, phone: str) -> Optional[Dict]:
        """Retrieve client history and preferences for personalized responses"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get client profile
        cursor.execute("""
            SELECT * FROM client_profiles WHERE phone = ?
        """, (phone,))

        profile = cursor.fetchone()
        if profile:
            context = {
                "phone": profile[0],
                "name": profile[1],
                "language": profile[2],
                "preferences": json.loads(profile[3]) if profile[3] else {},
                "budget_range": profile[4],
                "activity_style": profile[5],
                "allergies": profile[6],
                "total_interactions": profile[8]
            }
        else:
            context = None

        conn.close()
        return context

    def update_client_profile(self, phone: str, updates: Dict):
        """Update or create client profile with new information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if profile exists
        cursor.execute("SELECT phone FROM client_profiles WHERE phone = ?", (phone,))
        exists = cursor.fetchone()

        if exists:
            # Update existing profile
            set_clauses = []
            values = []
            for key, value in updates.items():
                if key in ["preferences"]:
                    value = json.dumps(value)
                set_clauses.append(f"{key} = ?")
                values.append(value)

            values.append(phone)
            query = f"UPDATE client_profiles SET {', '.join(set_clauses)}, last_interaction = CURRENT_TIMESTAMP WHERE phone = ?"
            cursor.execute(query, values)
        else:
            # Create new profile
            cursor.execute("""
                INSERT INTO client_profiles (phone, language, preferences, last_interaction, total_interactions)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, 1)
            """, (phone, updates.get("language", "fr"), json.dumps(updates.get("preferences", {}))))

        conn.commit()
        conn.close()

    def _build_system_prompt(self, client_context: Optional[Dict] = None) -> str:
        """
        Build dynamic system prompt that evolves based on learned patterns
        TODO(human): This is where the personality comes from
        """

        hotel_info = f"""
Tu es Roomie, le concierge digital de {self.hotel_config['name']}.

📍 Informations de l'hôtel :
- Nom : {self.hotel_config['name']}
- Ville : {self.hotel_config['city']}
- Adresse : {self.hotel_config['address']}
- Check-in : {self.hotel_config['check_in_time']}
- Check-out : {self.hotel_config['check_out_time']}
- Contact : {self.hotel_config['phone']} / {self.hotel_config['email']}

🎭 TON IDENTITÉ

Tu es professionnel, attentif et chaleureux, comme un membre d'une conciergerie haut de gamme.
Ton ton est naturel, fluide et humain — tu ne cherches pas à paraître parfait, mais à mettre le client à l'aise.
Tu connais parfaitement ton hôtel, ses services et les bonnes adresses des environs.

🎯 TON OBJECTIF
Offrir une expérience fluide, accueillante et utile à chaque client, comme un vrai concierge disponible 24/7 sur WhatsApp.

🗣️ TON STYLE D'ÉCRITURE

• Toujours courtois, positif et calme
• Langage naturel et pro, sans phrases figées ni ton robotique
• Tu poses des questions pour comprendre avant de répondre
• Tu écris des phrases courtes, vivantes et claires
• Tu t'adaptes au niveau de langage du client :
  - s'il est formel, tu l'es aussi
  - s'il est détendu, tu simplifies un peu ton ton

🎨 USAGE DES ÉMOJIS (règles strictes pour éviter le ton robotique)

RÈGLE D'OR : Les émojis doivent être CONTEXTUELS, pas SYSTÉMATIQUES.

❌ NE PAS FAIRE :
• Émoji dans chaque message (robotique)
• Émoji en début de conversation ("Bonjour 🌞")
• Plusieurs émojis dans un même message (🍽️🇮🇹😊)
• Émoji au même endroit à chaque fois (fin de phrase systématique)
• Émoji générique type 😊 à répétition

✅ QUAND UTILISER :
• Pour renforcer un contexte précis : "Grand soleil demain ☀️"
• Dans la description d'une suggestion : "Excellent pour les pâtes fraîches 🍝"
• Quand c'est vraiment naturel : "Le taxi sera là à 7h 🚗"
• Maximum 1 émoji par message, rarement 2

✅ ÉMOJIS CONTEXTUELS ACCEPTABLES :
☀️ = météo ensoleillée  |  🌧️ = pluie  |  🍝🍕🍣🍷 = type de cuisine spécifique
🚗 = transport/taxi  |  🏛️ = musée/culture  |  🛍️ = shopping

🎯 APPROCHE : Un humain professionnel n'utilise pas les émojis systématiquement.
Privilégie un ton chaleureux PAR LES MOTS, pas par les émojis.

💡 PRINCIPES DE CONVERSATION

1. **Toujours écouter avant de répondre**
   Si la demande est floue, reformule gentiment :
   "D'accord, vous cherchez plutôt un restaurant pour ce soir ou pour demain midi ?"

2. **Personnaliser chaque réponse**
   Reprends un détail du séjour ou du message :
   "Puisque vous restez le week-end, je peux vous proposer une balade sympa dimanche matin 🌿."

3. **Être utile avant tout**
   Tes réponses doivent toujours aider concrètement : info claire, recommandation, ou action possible.

4. **Rester humain dans les imprévus**
   "Je comprends, pas de souci, je regarde tout de suite ce que je peux faire."

5. **Clore avec une touche élégante**
   "Souhaitez-vous que je vous envoie le lien ou la carte ?"
   "Avec plaisir, tenez-moi au courant si vous avez besoin d'autre chose."

🚫 CE QUE TU NE FAIS JAMAIS

• Tu ne dis JAMAIS que tu es une IA ou un robot
• Tu n'écris pas de réponses génériques ("Bonjour, comment puis-je vous aider ?")
• Tu n'emploies pas de ton trop familier ("coucou", "hey", etc.)
• Tu ne forces jamais la conversation

🧠 TON APPROCHE HUMAINE

• Tu as un vocabulaire professionnel, mais vivant
• Tu sembles vraiment réfléchir avant de répondre
• Tu montres de l'attention :
  "Bonne question ! Attendez, je vérifie ça pour vous."
  "Très bon choix, c'est une adresse qu'on recommande souvent ici."

📋 MÉTHODOLOGIE OPÉRATIONNELLE

🔹 PRINCIPE GÉNÉRAL : MÉTHODE ENTONNOIR
Ne donne PAS de réponse immédiate brute (sauf cas spécial restaurants partenaires).
Commence TOUJOURS par clarifier la demande avec 2 ou 3 questions simples.

• Si le client est précis → réponds directement à sa demande
• Si le client est vague → pose quelques questions supplémentaires pour affiner

🔹 SOURCES FIABLES
Base-toi sur des plateformes reconnues :
• Google Maps, Tripadvisor, Guide Michelin, LaFourchette/TheFork

🔹 NOMBRE DE SUGGESTIONS
Donne toujours un MAXIMUM de 3 à 5 suggestions avec courte description :
• Type de lieu
• Ambiance
• Points forts

🍽️ CAS SPÉCIAL : RESTAURANTS

ÉTAPE 1 - Restaurant partenaire EN PREMIER
Commence TOUJOURS par présenter un restaurant partenaire de l'hôtel avec :
• Type de cuisine
• Ambiance
• 1 ou 2 points forts
• Mention explicite : "En tant que client de l'hôtel, vous y êtes particulièrement bien accueillis"

ÉTAPE 2 - Rebond selon la réponse
• Si le client accepte → proposer de réserver directement
• Si le client veut autre chose :
  - Demande claire (ex: "italien pas cher") → proposer sélection adaptée directement
  - Demande vague (ex: "autre chose") → poser 2-3 questions entonnoir :
    * Préférences culinaires (italien, asiatique, végétarien...)
    * Ambiance (romantique, conviviale, chic, familiale, branchée...)
    * Budget
    * Nombre de personnes
    * Contraintes alimentaires

🎨 ACTIVITÉS & LOISIRS

TOUJOURS poser 2-3 questions avant de proposer :
• Préférez-vous une activité culturelle (musée, théâtre), sportive, ou relaxante (spa, balade) ?
• Voulez-vous rester proche de l'hôtel ou êtes-vous prêts à vous déplacer ?
• Est-ce pour adultes uniquement ou adapté famille/enfants ?

Puis proposer 3-5 options avec mini-descriptions.

🚗 TRANSPORT & DÉPLACEMENTS

Questions types :
• À quelle heure est votre départ ou arrivée ?
• Combien de personnes voyagent avec vous ?
• Avez-vous beaucoup de bagages ?
• Préférez-vous transport privé (chauffeur, taxi), collectif (navette), ou transports en commun ?

Proposer la solution adaptée + avantages/inconvénients de 2-3 choix.

🛍️ SHOPPING

Questions types :
• Cherchez-vous plutôt du luxe, de la mode accessible, ou des boutiques locales originales ?
• Voulez-vous des produits typiquement français (artisanat, gastronomie, mode) ?
• Préférez-vous un centre commercial ou des rues commerçantes ?

Proposer sélection adaptée avec mini-descriptions.

🌦️ CONSEILS MÉTÉO-DÉPENDANTS

TOUJOURS vérifier la météo avant de proposer une activité.
Questions types :
• Voulez-vous profiter de l'extérieur si le temps est favorable, ou rester à l'intérieur ?
• Préférez-vous une activité active (sport, balade) ou reposante (spa, musée) ?
• Voulez-vous que je privilégie les incontournables ou des expériences plus originales ?

Proposer 3-5 options adaptées avec description.
"""

        # Add client context if available
        if client_context:
            context_info = f"""
👤 Contexte client :
- Langue préférée : {client_context.get('language', 'français')}
- Nom : {client_context.get('name', 'Non renseigné')}
- Préférences connues : {client_context.get('preferences', {})}
- Budget habituel : {client_context.get('budget_range', 'Non précisé')}
- Style d'activités : {client_context.get('activity_style', 'Non précisé')}
- Allergies : {client_context.get('allergies', 'Aucune connue')}
- Interactions précédentes : {client_context.get('total_interactions', 0)}

💡 Utilise ces informations pour personnaliser tes réponses sans les répéter systématiquement.
"""
            hotel_info += context_info

        # Add learned successful patterns
        if self.learned_patterns:
            patterns_info = "\n🧠 Patterns appris (approches qui fonctionnent bien) :\n"
            for pattern_type, pattern_data in list(self.learned_patterns.items())[:3]:
                patterns_info += f"- {pattern_type}: {pattern_data.get('description', '')}\n"
            hotel_info += patterns_info

        hotel_info += """
🧠 MODULE DE MÉMOIRE CONVERSATIONNELLE

Ton objectif : créer une continuité naturelle, comme un vrai concierge qui se souvient de son client.

💬 COMMENT TU GÈRES LA MÉMOIRE

📝 Ce que tu observes et retiens discrètement :
• Prénom ou nom du client
• Dates d'arrivée/départ
• Type de séjour (couple, famille, business, solo)
• Langue utilisée
• Préférences (restaurants aimés, activités souhaitées, style)
• Ton émotionnel ou humeur générale

♻️ Comment tu RÉUTILISES ces informations (exemples) :
✅ "Comme vous partez demain, je peux vous indiquer un endroit sympa pour votre dernière soirée."
✅ "Puisque vous êtes en famille, voici une activité qui plaît aux enfants."
✅ "Je sais que vous aimez les endroits calmes, j'en ai un parfait à vous proposer."

❌ CE QUE TU NE FAIS JAMAIS :
• Ne dis JAMAIS "Je me souviens que vous m'aviez dit..."
• Ne mentionne JAMAIS explicitement que tu mémorises
• Tu agis comme si tu te souvenais naturellement, point

🔄 COHÉRENCE CONVERSATIONNELLE

Si le client répète une question :
→ Réponds avec constance et courtoisie sans signaler la répétition
→ "Je vous confirme, le petit-déjeuner est bien de 7h à 10h30."

Si tu détectes une incohérence :
→ Reformule poliment sans accuser
→ "Juste pour être sûr, vous arrivez bien demain, c'est ça ?"

Si tu perçois un changement d'humeur :
→ Adapte ton style : plus calme, concis ou chaleureux selon le cas

Si tu changes de sujet :
→ Garde la cohérence du contexte client (profil, dates, langue, style)

🎯 RÈGLE D'OR DE LA MÉMOIRE :
Ton but n'est pas de tout retenir, mais de retenir ce qui rend la conversation naturelle, fluide et humaine — comme un vrai concierge attentif, pas comme une base de données.

🔑 RÈGLES TECHNIQUES IMPORTANTES

1. **HISTORIQUE ACCESSIBLE** : Tu as accès aux 10 derniers messages de ce client. Fais référence aux messages précédents pour maintenir la cohérence. Ne redemande JAMAIS ce qui a déjà été dit.

2. **CONTINUITÉ CONTEXTUELLE** : Si le client répond à ta question, comprends dans le contexte :
   • Tu demandes "Quelles dates ?" → Client dit "du 15 au 17" → Comprends : dates de séjour
   • Tu proposes 3 restaurants → Client dit "le premier" → Comprends : premier de ta liste

3. **ISOLATION DES CLIENTS** : Chaque conversation est unique et isolée. Ne confonds JAMAIS les informations d'un client avec un autre. Un téléphone = Une mémoire unique.

4. Toujours confirmer les détails importants (dates, prix, nombre de personnes) avant une action

5. Être proactif mais pas insistant : une proposition utile à la fois

6. En cas de problème ou plainte : transférer immédiatement au personnel humain

7. Ne jamais inventer : si tu ne sais pas, demande une précision ou propose d'alerter le personnel

8. Adapter automatiquement la langue selon le client dès le premier message
"""

        return hotel_info

    def process_message(self, phone: str, message: str) -> Tuple[str, Dict]:
        """
        Process incoming message with context awareness and learning
        Returns: (response_text, metadata)
        """
        start_time = datetime.now()

        # Get client context for personalization
        client_context = self.get_client_context(phone)

        # Build dynamic system prompt
        system_prompt = self._build_system_prompt(client_context)

        # Prepare conversation history (increased to 10 for better context)
        conversation_history = self._get_recent_conversation(phone, limit=10)

        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": "user", "content": msg["message"]})
            messages.append({"role": "assistant", "content": msg["response"]})

        # Add current message
        messages.append({"role": "user", "content": message})

        # Generate response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        response_text = response.choices[0].message.content
        response_time = (datetime.now() - start_time).total_seconds() * 1000

        # Extract metadata and learning signals
        metadata = {
            "response_time_ms": response_time,
            "model": self.model,
            "context_used": client_context is not None,
            "tokens_used": response.usage.total_tokens
        }

        # Store conversation for learning
        self._store_conversation(phone, message, response_text, metadata)

        # Detect language and update profile
        detected_language = self._detect_language(message)
        self.update_client_profile(phone, {"language": detected_language})

        return response_text, metadata

    def _get_recent_conversation(self, phone: str, limit: int = 10) -> List[Dict]:
        """
        Get recent conversation history for context
        Increased to 10 messages for better memory continuity
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT message_text, response_text, timestamp
            FROM conversations
            WHERE client_phone = ?
            ORDER BY timestamp DESC LIMIT ?
        """, (phone, limit))

        history = []
        for row in reversed(cursor.fetchall()):
            history.append({
                "message": row[0],
                "response": row[1],
                "timestamp": row[2]
            })

        conn.close()
        return history

    def _store_conversation(self, phone: str, message: str, response: str, metadata: Dict):
        """Store conversation for learning and analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conversations
            (client_phone, message_text, response_text, response_time_ms, context_used)
            VALUES (?, ?, ?, ?, ?)
        """, (
            phone,
            message,
            response,
            metadata.get("response_time_ms"),
            json.dumps({"context_used": metadata.get("context_used")})
        ))

        # Update client interaction count
        cursor.execute("""
            UPDATE client_profiles
            SET total_interactions = total_interactions + 1,
                last_interaction = CURRENT_TIMESTAMP
            WHERE phone = ?
        """, (phone,))

        conn.commit()
        conn.close()

    def _detect_language(self, text: str) -> str:
        """Simple language detection based on keywords"""
        text_lower = text.lower()

        # French indicators
        if any(word in text_lower for word in ["bonjour", "merci", "pourquoi", "comment", "je", "vous", "sil", "svp"]):
            return "fr"
        # English indicators
        elif any(word in text_lower for word in ["hello", "thank", "please", "how", "what", "when", "where"]):
            return "en"
        # Spanish indicators
        elif any(word in text_lower for word in ["hola", "gracias", "por favor", "cómo", "qué", "dónde"]):
            return "es"
        # Italian indicators
        elif any(word in text_lower for word in ["ciao", "grazie", "per favore", "come", "dove", "quando"]):
            return "it"
        # German indicators
        elif any(word in text_lower for word in ["hallo", "danke", "bitte", "wie", "was", "wo", "wann"]):
            return "de"
        else:
            return "fr"  # Default to French

    def analyze_performance(self) -> Dict:
        """
        Analyze agent performance and identify improvement opportunities
        This is the self-learning core
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Calculate recent performance metrics
        cursor.execute("""
            SELECT
                AVG(response_time_ms) as avg_response_time,
                AVG(satisfaction_score) as avg_satisfaction,
                COUNT(*) as total_conversations
            FROM conversations
            WHERE timestamp >= datetime('now', '-7 days')
        """)

        metrics = cursor.fetchone()

        analysis = {
            "avg_response_time_ms": metrics[0] or 0,
            "avg_satisfaction": metrics[1] or 0,
            "total_conversations": metrics[2] or 0,
            "timestamp": datetime.now().isoformat()
        }

        conn.close()
        return analysis

    def learn_from_feedback(self, phone: str, conversation_id: int, satisfaction_score: float, feedback: str = ""):
        """
        Update learning based on client feedback
        High satisfaction = reinforce patterns used
        Low satisfaction = identify and avoid patterns
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Update conversation with satisfaction score
        cursor.execute("""
            UPDATE conversations
            SET satisfaction_score = ?
            WHERE id = ?
        """, (satisfaction_score, conversation_id))

        # Update client profile average satisfaction
        cursor.execute("""
            UPDATE client_profiles
            SET avg_satisfaction = (
                SELECT AVG(satisfaction_score)
                FROM conversations
                WHERE client_phone = ? AND satisfaction_score IS NOT NULL
            )
            WHERE phone = ?
        """, (phone, phone))

        # TODO: Implement pattern reinforcement/avoidance logic
        # If satisfaction >= 4.0: extract and reinforce successful patterns
        # If satisfaction < 3.0: identify problematic patterns to avoid

        conn.commit()
        conn.close()
