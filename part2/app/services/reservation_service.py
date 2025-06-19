from typing import List
from app.models.reservation import Reservation
from app.models.user import User
from app.models.place import Place


class ReservationService:
    @classmethod
    def get_all_reservation(cls) -> List['Reservation']:
        return cls._reservations

    @classmethod
    def all(cls):
        return cls._reservations

    @classmethod
    def reservations_by(cls, user_id: str) -> List['Place']:
        from .place import Place
        reserved_place_ids = [
                r.place_id for r in cls._reservations
                if r.user_id == user_id
                ]
        return [
                place for place in Place._places
                if place.id in reserved_place_ids
                ]
