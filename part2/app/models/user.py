from __future__ import annotations
from typing import List
from app.models.base_model import BaseModel

class User(BaseModel):
    _users: List['User'] = []

    allowed_update_fields = ['first_name', 'last_name', 'email', 'is_admin', 'password']

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password = password
        self._is_admin = is_admin
        self.reservations: List[Reservation] =[]
        self.places: List[Place] = []
        self.reviews: List[Review] = []

        User._users.append(self)

    def hash_password(self, password):
        "Hashes the password before storing it."
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        "Verifies if the provided password matches the hashed password."
        return bcrypt.check_password_hash(self.password, password)

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
    def get_by_email(cls, email: str) -> 'User' | None:
        return next((user for user in cls._users if user.email == email), None)


    @property
    def is_admin(self):
        return self._is_admin
    
    @is_admin.setter
    def is_admin(self, value: bool):
        self._is_admin = value

    @classmethod
    def list_all(cls) -> List['User']:
        return cls._users

    @classmethod
    def get_by_id(cls, id):
        return next((user for user in cls._users if user.id == id), None)

    def __repr__(self):
        return f"User(id='{self.id}', email='{self.email}')"

