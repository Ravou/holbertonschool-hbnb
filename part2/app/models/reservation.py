from typing import List
from app.models.base_model import BaseModel

class Reservation(BaseModel):

    _reservations: List['Reservation'] = []

    def __init__(self, user, place, date):
        super().__init__()
        self.user_id = user.id if hasattr(user, 'id') else user
        self.place_id = place.id if hasattr(place, 'id') else place
        self.date = date

        # Add this Reservation object to the user's reservations list if not already present
        if hasattr(user, 'reservations') and self not in user.reservations:
            user.reservations.append(self)

        # Add this Reservation object to the place's reservations list if not already present
        if hasattr(place, 'reservations') and self not in place.reservations:
            place.reservations.append(self)

        # Add this Reservation instance to the class-level list of all reservations
        Reservation._reservations.append(self)

    @classmethod
    def list_all(cls) -> List['Reservation']:
        """Return all reservations."""
        return cls._reservations

    @classmethod
    def reservations_by_user(cls, user_id: str) -> List['Reservation']:
        """Return all reservations made by a specific user."""
        return [r for r in cls._reservations if r.user_id == user_id]

    @classmethod
    def places_reserved_by_user(cls, user_id: str) -> List['Place']:
        """Return all Place objects reserved by a specific user."""
        from app.models.place import Place
        reserved_place_ids = [r.place_id for r in cls._reservations if r.user_id == user_id]
        return [place for place in Place.list_all() if place.id in reserved_place_ids]

    def __repr__(self):
        return (f"Reservation(id='{self.id}', user_id='{self.user_id}', "
                f"place_id='{self.place_id}', date='{self.date}')")

