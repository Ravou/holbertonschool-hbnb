from typing import List
from models.base_model import BaseModel

class Reservation(BaseModel):

    _reservations: List['Reservation'] = []

    def __init__(self, user, place, date):
        super().__init__()
        self.user_id = user.id if hasattr(user, 'id') else user
        self.place_id = place.id if hasattr(place, 'id') else place
        self.date = date

        
        user.reservation_ids.append(self.id)
        place.reservation_ids.append(self.id)

        Reservation._reservations.append(self)

    @classmethod
    def get_all_reservation(cls) -> List['Reservation']:
        return cls._reservations

    @classmethod
    def all(cls):
        return cls._reservations

    @classmethod
    def reservations_by(cls, user_id: str) -> List['Place']:
        from models.place import Place
        reserved_place_ids = [
                r.place_id for r in cls._reservations
                if r.user_id == user_id
                ]
        return [
                place for place in Place._places
                if place.id in reserved_place_ids
                ]

    def __repr__(self):
        return f"Reservation(id='{self.id}', user_id='{self.user_id}', place_id='{self.place_id}', date='{self.date}')"
