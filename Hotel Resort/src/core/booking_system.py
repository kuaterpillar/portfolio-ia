"""
Booking and Availability Management System
Handles room reservations, availability checks, and booking confirmations
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class BookingSystem:
    """
    Manages hotel room bookings with availability checking
    """

    def __init__(self, db_path: str = "data/bookings.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize booking database"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Room types table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS room_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_name TEXT NOT NULL,
                description TEXT,
                capacity INTEGER,
                price_per_night REAL,
                total_rooms INTEGER,
                amenities TEXT
            )
        """)

        # Bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_phone TEXT NOT NULL,
                client_name TEXT,
                client_email TEXT,
                room_type_id INTEGER,
                check_in_date TEXT NOT NULL,
                check_out_date TEXT NOT NULL,
                num_guests INTEGER,
                total_price REAL,
                status TEXT DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                confirmed_at DATETIME,
                special_requests TEXT,
                FOREIGN KEY (room_type_id) REFERENCES room_types(id)
            )
        """)

        # Initialize default room types if empty
        cursor.execute("SELECT COUNT(*) FROM room_types")
        if cursor.fetchone()[0] == 0:
            default_rooms = [
                ("Chambre Simple", "Chambre confortable avec lit simple", 1, 89.0, 10, "WiFi, TV, Climatisation"),
                ("Chambre Double", "Chambre spacieuse avec lit double", 2, 129.0, 15, "WiFi, TV, Climatisation, Minibar"),
                ("Suite Junior", "Suite avec salon séparé", 2, 199.0, 5, "WiFi, TV, Climatisation, Minibar, Vue panoramique"),
                ("Suite Deluxe", "Suite luxueuse avec terrasse", 4, 349.0, 3, "WiFi, TV, Climatisation, Minibar, Vue panoramique, Jacuzzi")
            ]

            cursor.executemany("""
                INSERT INTO room_types (type_name, description, capacity, price_per_night, total_rooms, amenities)
                VALUES (?, ?, ?, ?, ?, ?)
            """, default_rooms)

        conn.commit()
        conn.close()

    def check_availability(
        self,
        check_in: str,
        check_out: str,
        num_guests: int = 1,
        room_type_id: Optional[int] = None
    ) -> List[Dict]:
        """
        Check room availability for given dates

        Args:
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)
            num_guests: Number of guests
            room_type_id: Specific room type (optional)

        Returns:
            List of available room types with details
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get all room types that can accommodate the guests
        query = """
            SELECT id, type_name, description, capacity, price_per_night, total_rooms, amenities
            FROM room_types
            WHERE capacity >= ?
        """
        params = [num_guests]

        if room_type_id:
            query += " AND id = ?"
            params.append(room_type_id)

        cursor.execute(query, params)
        room_types = cursor.fetchall()

        available_rooms = []

        for room_type in room_types:
            rt_id, name, desc, capacity, price, total, amenities = room_type

            # Count booked rooms for this type in the date range
            cursor.execute("""
                SELECT COUNT(*) FROM bookings
                WHERE room_type_id = ?
                AND status IN ('pending', 'confirmed')
                AND (
                    (check_in_date <= ? AND check_out_date > ?)
                    OR (check_in_date < ? AND check_out_date >= ?)
                    OR (check_in_date >= ? AND check_out_date <= ?)
                )
            """, (rt_id, check_in, check_in, check_out, check_out, check_in, check_out))

            booked = cursor.fetchone()[0]
            available = total - booked

            if available > 0:
                # Calculate total price
                days = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
                total_price = price * days

                available_rooms.append({
                    "room_type_id": rt_id,
                    "name": name,
                    "description": desc,
                    "capacity": capacity,
                    "price_per_night": price,
                    "available_rooms": available,
                    "amenities": amenities.split(", "),
                    "total_price": total_price,
                    "num_nights": days
                })

        conn.close()
        return available_rooms

    def create_booking(
        self,
        client_phone: str,
        room_type_id: int,
        check_in: str,
        check_out: str,
        num_guests: int,
        client_name: Optional[str] = None,
        client_email: Optional[str] = None,
        special_requests: Optional[str] = None
    ) -> Tuple[bool, str, Optional[int]]:
        """
        Create a new booking

        Returns:
            (success, message, booking_id)
        """
        # Validate dates
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")

            if check_in_date >= check_out_date:
                return False, "La date de départ doit être après la date d'arrivée", None

            if check_in_date < datetime.now():
                return False, "La date d'arrivée ne peut pas être dans le passé", None

        except ValueError:
            return False, "Format de date invalide (utilisez YYYY-MM-DD)", None

        # Check availability
        available = self.check_availability(check_in, check_out, num_guests, room_type_id)

        if not available:
            return False, "Aucune chambre disponible pour ces dates", None

        # Create booking
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        room_info = available[0]
        total_price = room_info["total_price"]

        cursor.execute("""
            INSERT INTO bookings
            (client_phone, client_name, client_email, room_type_id, check_in_date, check_out_date,
             num_guests, total_price, status, special_requests)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)
        """, (
            client_phone,
            client_name,
            client_email,
            room_type_id,
            check_in,
            check_out,
            num_guests,
            total_price,
            special_requests
        ))

        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return True, f"Réservation créée avec succès ! ID: {booking_id}", booking_id

    def confirm_booking(self, booking_id: int) -> Tuple[bool, str]:
        """Confirm a pending booking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE bookings
            SET status = 'confirmed', confirmed_at = CURRENT_TIMESTAMP
            WHERE id = ? AND status = 'pending'
        """, (booking_id,))

        if cursor.rowcount == 0:
            conn.close()
            return False, "Réservation introuvable ou déjà confirmée"

        conn.commit()
        conn.close()
        return True, "Réservation confirmée avec succès !"

    def cancel_booking(self, booking_id: int, client_phone: str) -> Tuple[bool, str]:
        """Cancel a booking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE bookings
            SET status = 'cancelled'
            WHERE id = ? AND client_phone = ? AND status != 'cancelled'
        """, (booking_id, client_phone))

        if cursor.rowcount == 0:
            conn.close()
            return False, "Réservation introuvable ou déjà annulée"

        conn.commit()
        conn.close()
        return True, "Réservation annulée avec succès"

    def get_booking_details(self, booking_id: int) -> Optional[Dict]:
        """Get detailed information about a booking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT b.*, rt.type_name, rt.price_per_night, rt.amenities
            FROM bookings b
            JOIN room_types rt ON b.room_type_id = rt.id
            WHERE b.id = ?
        """, (booking_id,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return {
            "booking_id": row[0],
            "client_phone": row[1],
            "client_name": row[2],
            "client_email": row[3],
            "room_type": row[13],
            "check_in": row[5],
            "check_out": row[6],
            "num_guests": row[7],
            "total_price": row[8],
            "status": row[9],
            "created_at": row[10],
            "confirmed_at": row[11],
            "special_requests": row[12],
            "price_per_night": row[14],
            "amenities": row[15].split(", ")
        }

    def get_client_bookings(self, client_phone: str) -> List[Dict]:
        """Get all bookings for a client"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT b.id, b.check_in_date, b.check_out_date, b.status, b.total_price, rt.type_name
            FROM bookings b
            JOIN room_types rt ON b.room_type_id = rt.id
            WHERE b.client_phone = ?
            ORDER BY b.check_in_date DESC
        """, (client_phone,))

        bookings = []
        for row in cursor.fetchall():
            bookings.append({
                "booking_id": row[0],
                "check_in": row[1],
                "check_out": row[2],
                "status": row[3],
                "total_price": row[4],
                "room_type": row[5]
            })

        conn.close()
        return bookings

    def format_availability_message(self, available_rooms: List[Dict]) -> str:
        """Format availability results for WhatsApp message"""
        if not available_rooms:
            return "❌ Désolé, aucune chambre n'est disponible pour ces dates."

        message = "✅ Chambres disponibles :\n\n"

        for i, room in enumerate(available_rooms, 1):
            message += f"{i}. **{room['name']}**\n"
            message += f"   • {room['description']}\n"
            message += f"   • Capacité : {room['capacity']} personne(s)\n"
            message += f"   • Prix : {room['price_per_night']}€/nuit\n"
            message += f"   • Total ({room['num_nights']} nuits) : {room['total_price']}€\n"
            message += f"   • Équipements : {', '.join(room['amenities'])}\n"
            message += f"   • Chambres disponibles : {room['available_rooms']}\n\n"

        message += "Souhaitez-vous réserver l'une de ces chambres ? 😊"
        return message

    def format_booking_confirmation(self, booking_details: Dict) -> str:
        """Format booking confirmation message"""
        message = f"""
✅ **Réservation confirmée !**

📋 Détails de votre réservation :
• N° de réservation : #{booking_details['booking_id']}
• Chambre : {booking_details['room_type']}
• Arrivée : {booking_details['check_in']}
• Départ : {booking_details['check_out']}
• Nombre de personnes : {booking_details['num_guests']}
• Prix total : {booking_details['total_price']}€

"""
        if booking_details['special_requests']:
            message += f"• Demandes spéciales : {booking_details['special_requests']}\n"

        message += """
Un email de confirmation vous sera envoyé sous peu.

Avez-vous besoin d'aide pour préparer votre séjour ? (restaurants, activités, transport...) 😊
"""
        return message.strip()
