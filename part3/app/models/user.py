from __future__ import annotations
from typing import List
from app.models.base_model import BaseModel
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    allowed_update_fields = ['first_name', 'last_name']

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

    

    def __repr__(self):
        return f"User(id='{self.id}', email='{self.email}')"

