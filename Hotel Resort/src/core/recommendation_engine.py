"""
Recommendation Engine with Context Awareness
Provides personalized recommendations based on:
- Client profile and preferences
- Weather conditions
- Budget constraints
- Location and neighborhood
- Time of day and season
"""

import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime


class RecommendationEngine:
    """
    Intelligent recommendation system that considers multiple factors
    for personalized suggestions
    """

    def __init__(self, hotel_city: str, hotel_address: str):
        self.hotel_city = hotel_city
        self.hotel_address = hotel_address
        self.weather_api_key = os.getenv("WEATHER_API_KEY")

        # Local knowledge base (can be expanded)
        self.recommendations_db = self._load_recommendations_db()

    def _load_recommendations_db(self) -> Dict:
        """
        Load curated recommendations database
        In production, this would come from a database or CMS
        """
        return {
            "restaurants": [
                {
                    "name": "Le Gourmet Parisien",
                    "type": "gastronomique",
                    "cuisine": "française",
                    "district": "8e",
                    "price_range": "€€€€",
                    "avg_price_per_person": 120,
                    "ambiance": "romantique",
                    "specialties": ["foie gras", "homard", "desserts signatures"],
                    "distance_from_hotel": "500m",
                    "booking_recommended": True
                },
                {
                    "name": "Bistrot du Coin",
                    "type": "bistrot",
                    "cuisine": "française traditionnelle",
                    "district": "8e",
                    "price_range": "€€",
                    "avg_price_per_person": 35,
                    "ambiance": "décontractée",
                    "specialties": ["steak-frites", "boeuf bourguignon", "tarte tatin"],
                    "distance_from_hotel": "200m",
                    "booking_recommended": False
                },
                {
                    "name": "Sushi Zen",
                    "type": "japonais",
                    "cuisine": "japonaise",
                    "district": "8e",
                    "price_range": "€€€",
                    "avg_price_per_person": 65,
                    "ambiance": "moderne",
                    "specialties": ["omakase", "sashimi", "tempura"],
                    "distance_from_hotel": "800m",
                    "booking_recommended": True
                }
            ],
            "activities": [
                {
                    "name": "Musée du Louvre",
                    "type": "musée",
                    "category": "culture",
                    "district": "1er",
                    "price": 17,
                    "duration_hours": 3,
                    "weather_dependent": False,
                    "best_time": "matin",
                    "distance_from_hotel": "2km",
                    "booking_required": True,
                    "description": "Le plus grand musée du monde avec la Joconde et des milliers d'œuvres"
                },
                {
                    "name": "Croisière sur la Seine",
                    "type": "activité",
                    "category": "romantique",
                    "district": "centre",
                    "price": 15,
                    "duration_hours": 1,
                    "weather_dependent": True,
                    "best_time": "soir",
                    "distance_from_hotel": "1.5km",
                    "booking_required": True,
                    "description": "Vue imprenable sur les monuments de Paris illuminés"
                },
                {
                    "name": "Balade aux Champs-Élysées",
                    "type": "promenade",
                    "category": "shopping",
                    "district": "8e",
                    "price": 0,
                    "duration_hours": 2,
                    "weather_dependent": True,
                    "best_time": "après-midi",
                    "distance_from_hotel": "100m",
                    "booking_required": False,
                    "description": "La plus belle avenue du monde avec boutiques de luxe et cafés"
                },
                {
                    "name": "Musée d'Orsay",
                    "type": "musée",
                    "category": "culture",
                    "district": "7e",
                    "price": 16,
                    "duration_hours": 2.5,
                    "weather_dependent": False,
                    "best_time": "après-midi",
                    "distance_from_hotel": "2.5km",
                    "booking_required": True,
                    "description": "Collection impressionniste exceptionnelle dans une ancienne gare"
                }
            ],
            "services": [
                {
                    "name": "Navette aéroport CDG",
                    "type": "transport",
                    "price": 35,
                    "duration_minutes": 45,
                    "description": "Service de navette privée vers l'aéroport Charles de Gaulle"
                },
                {
                    "name": "Spa & Massage",
                    "type": "bien-être",
                    "price": 80,
                    "duration_minutes": 60,
                    "description": "Massage relaxant dans notre spa partenaire à 5 minutes"
                },
                {
                    "name": "Late Check-out",
                    "type": "hébergement",
                    "price": 50,
                    "description": "Profitez de votre chambre jusqu'à 16h (selon disponibilité)"
                }
            ]
        }

    def get_weather(self) -> Optional[Dict]:
        """Fetch current weather for the hotel city"""
        if not self.weather_api_key:
            return None

        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": self.hotel_city,
                "appid": self.weather_api_key,
                "units": "metric",
                "lang": "fr"
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()
            return {
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"],
                "main": data["weather"][0]["main"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
        except Exception as e:
            print(f"Weather API error: {e}")
            return None

    def recommend_restaurants(
        self,
        budget: Optional[float] = None,
        cuisine_type: Optional[str] = None,
        ambiance: Optional[str] = None,
        max_distance: Optional[str] = None
    ) -> List[Dict]:
        """
        Recommend restaurants based on preferences and constraints
        """
        restaurants = self.recommendations_db["restaurants"].copy()

        # Filter by budget
        if budget:
            restaurants = [
                r for r in restaurants
                if r["avg_price_per_person"] <= budget
            ]

        # Filter by cuisine
        if cuisine_type:
            restaurants = [
                r for r in restaurants
                if cuisine_type.lower() in r["cuisine"].lower() or cuisine_type.lower() in r["type"].lower()
            ]

        # Filter by ambiance
        if ambiance:
            restaurants = [
                r for r in restaurants
                if ambiance.lower() in r["ambiance"].lower()
            ]

        # Sort by distance (closest first)
        restaurants.sort(key=lambda x: int(x["distance_from_hotel"].replace("m", "").replace("km", "000")))

        return restaurants[:3]  # Return top 3

    def recommend_activities(
        self,
        weather: Optional[Dict] = None,
        preferences: Optional[List[str]] = None,
        budget: Optional[float] = None,
        time_available: Optional[float] = None
    ) -> List[Dict]:
        """
        Recommend activities considering weather, preferences, and constraints
        """
        activities = self.recommendations_db["activities"].copy()

        # Filter by weather
        if weather:
            # If bad weather (rain, snow), prefer indoor activities
            if weather["main"] in ["Rain", "Snow", "Thunderstorm"]:
                activities = [a for a in activities if not a["weather_dependent"]]

        # Filter by budget
        if budget:
            activities = [a for a in activities if a["price"] <= budget]

        # Filter by time available
        if time_available:
            activities = [a for a in activities if a["duration_hours"] <= time_available]

        # Filter by preferences (categories)
        if preferences:
            filtered = []
            for activity in activities:
                for pref in preferences:
                    if pref.lower() in activity["category"].lower() or pref.lower() in activity["type"].lower():
                        filtered.append(activity)
                        break
            if filtered:
                activities = filtered

        # Sort by distance
        activities.sort(key=lambda x: float(x["distance_from_hotel"].replace("km", "")))

        return activities[:3]

    def recommend_services(self, context: Optional[str] = None) -> List[Dict]:
        """Recommend hotel services based on context"""
        services = self.recommendations_db["services"].copy()

        # Context-based filtering
        if context:
            if "aéroport" in context.lower() or "vol" in context.lower() or "taxi" in context.lower():
                services = [s for s in services if s["type"] == "transport"]
            elif "massage" in context.lower() or "spa" in context.lower() or "détente" in context.lower():
                services = [s for s in services if s["type"] == "bien-être"]
            elif "check-out" in context.lower() or "partir" in context.lower() or "tard" in context.lower():
                services = [s for s in services if s["type"] == "hébergement"]

        return services

    def generate_personalized_recommendation(
        self,
        request: str,
        client_profile: Optional[Dict] = None
    ) -> str:
        """
        Generate a complete personalized recommendation response
        This is the main entry point for the chatbot
        """
        request_lower = request.lower()

        # Determine recommendation type
        is_restaurant = any(word in request_lower for word in ["restaurant", "manger", "dîner", "déjeuner", "cuisine", "repas"])
        is_activity = any(word in request_lower for word in ["activité", "musée", "visite", "faire", "voir", "balade", "sortie"])
        is_service = any(word in request_lower for word in ["taxi", "navette", "spa", "massage", "check-out"])

        # Extract context from client profile
        budget = None
        preferences = []
        if client_profile:
            budget_range = client_profile.get("budget_range", "")
            if "€" in budget_range:
                # Extract numeric budget
                budget = 100  # Default mid-range
            preferences = client_profile.get("preferences", {}).get("activity_style", [])

        # Get weather
        weather = self.get_weather()

        response_parts = []

        if is_restaurant:
            # Extract restaurant preferences from request
            cuisine = None
            ambiance = None
            if "romantique" in request_lower:
                ambiance = "romantique"
            if "japonais" in request_lower or "sushi" in request_lower:
                cuisine = "japonais"
            elif "français" in request_lower or "francais" in request_lower:
                cuisine = "français"

            restaurants = self.recommend_restaurants(
                budget=budget,
                cuisine_type=cuisine,
                ambiance=ambiance
            )

            if restaurants:
                response_parts.append("🍽️ Voici mes recommandations de restaurants :\n")
                for i, resto in enumerate(restaurants, 1):
                    response_parts.append(
                        f"{i}. **{resto['name']}** ({resto['type']})\n"
                        f"   • Cuisine : {resto['cuisine']}\n"
                        f"   • Prix moyen : {resto['avg_price_per_person']}€/pers ({resto['price_range']})\n"
                        f"   • Distance : {resto['distance_from_hotel']}\n"
                        f"   • Ambiance : {resto['ambiance']}\n"
                        f"   • Spécialités : {', '.join(resto['specialties'])}\n"
                    )
                    if resto['booking_recommended']:
                        response_parts.append(f"   ℹ️ Réservation recommandée\n")
                    response_parts.append("\n")

        elif is_activity:
            activities = self.recommend_activities(
                weather=weather,
                preferences=preferences,
                budget=budget
            )

            if activities:
                # Add weather context
                if weather:
                    response_parts.append(f"🌤️ Météo actuelle : {weather['description']}, {weather['temp']:.1f}°C\n\n")

                response_parts.append("🎨 Voici mes recommandations d'activités :\n\n")
                for i, activity in enumerate(activities, 1):
                    response_parts.append(
                        f"{i}. **{activity['name']}**\n"
                        f"   • Type : {activity['type']} ({activity['category']})\n"
                        f"   • Prix : {activity['price']}€\n"
                        f"   • Durée : {activity['duration_hours']}h\n"
                        f"   • Distance : {activity['distance_from_hotel']}\n"
                        f"   • {activity['description']}\n"
                    )
                    if activity['booking_required']:
                        response_parts.append(f"   ℹ️ Réservation nécessaire\n")
                    response_parts.append("\n")

        elif is_service:
            services = self.recommend_services(context=request)

            if services:
                response_parts.append("✨ Services disponibles :\n\n")
                for i, service in enumerate(services, 1):
                    response_parts.append(
                        f"{i}. **{service['name']}**\n"
                        f"   • {service['description']}\n"
                        f"   • Prix : {service['price']}€\n"
                    )
                    if "duration_minutes" in service:
                        response_parts.append(f"   • Durée : {service['duration_minutes']} min\n")
                    response_parts.append("\n")

        if not response_parts:
            return None

        response_parts.append("\nSouhaitez-vous que je vous aide à réserver l'une de ces options ? 😊")

        return "".join(response_parts)
