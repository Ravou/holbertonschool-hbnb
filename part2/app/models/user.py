from app.models.base_model import BaseModel
from typing import List
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__password = password
        self.is_admin = is_admin
        self.reservation_ids = []
        self.place_ids = []
        self.review_ids = []

    def register(self):
        if not self.first_name:
            print("First name must not be empty.")
            return False
        elif not self.last_name:
            print("Last name must not be empty.")
            return False
        elif not self.is_valid_email(self.email):
            print("Invalid email address.")
            return False
        elif not self.is_strong_password(self.__password):
            print("Password is not strong enough.")
            return False
        else:
            print("User registered successfully.")
            return True

    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    
    @staticmethod
    def is_strong_password(password: str) -> bool:
        return (len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password))

    def authenticate(self, password: str) -> bool:
        return self.__password == password

    @classmethod
    def login(cls, email, password, users_list):
        user = next ((u for u in users_list if u.email == email), None)
        if user is None:
            print("User not found.")
            return False
        elif user.authenticate(password):
            print(f"Welcome, {user.first_name}!")
            return True
        else:
            print("Incorrect password.")
            return False

    
    def add_place(self, place):
        if not isinstance(place, Place):
            print("Invalid place object.")
            return False
        if place.id not in self.place_ids:
            self.place_ids.append(place.id)
            place.owner_id = self.id
            print(f"Place '{place.name}' added successfully.")
            return True
        else:
            print("Place already added.")
            return False

    def has_reserved(self, place):
        return place.id in self.reservation_ids

    def add_review(self, text, rating, place):
        if not self.has_reserved(place):
            print("You must reserve the place before adding a review.")
            return False
        elif not 1 <= rating <= 5:
            print("Rating must be between 1 and 5.")
            return False

        review = Review(text=text, rating=rating, place_id=place.id, user_id=self.id)
        self.review_ids.append(review.id)
        place.review_ids.append(review.id)
        print("Review added successfully.")
        return True

    def add_amenity(self, place, name, description):
        if not isinstance(place, Place):
            print("Invalid place object.")
            return False
        amenity = Amenity(name=name, description=description)
        place.amenity_ids.append(amenity.id)
        print(f"Amenity '{name}' added successfully to place '{place.name}'.")
        return True

    def __repr__(self):
        return f"User(id='{self.id}', email='{self.email}')"
