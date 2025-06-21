from typing import List, Optional
from app.models.base_model import BaseModel
from app.models.review import Review
from app.models.place import Place
from app.models.reservation import Reservation
from typing import List
import re

class User(BaseModel):
    _user: List['User'] = []

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.reservations: List[Reservation] =[]
        self.places: List[Place] = []
        self.reviews: List[Review] = []

    def add_place(self, place: Place):
        if place not in self.places:
            self.places.append(place)
            place.owner = self
            print(f"Place '{place.title}' added to user '{self.first_name}'.")
        else:
            print("Place already added.")

    def add_review(self, review: Review):
        self.reviews.append(review)
        print("Review added to user.")

    def add_reservation(self, reservation: Reservation):
        self.reservations.append(reservation)
        print("Reservation added to user.")

    @classmethod
    def list_all(cls) -> List['User']:
        return cls._users

    @classmethod
    def get_by_id(cls, id):
        return next((user for user in cls._users if user.id == id), None)

    def __repr__(self):
        return f"User(id='{self.id}', email='{self.email}')"

