from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.reservation import Reservation
from app.persistence.repository import (UserRepository, PlaceRepository, ReviewRepository, ReservationRepository)

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_by_id(self, user_id):
        return self.user_repository.get_by_id(user_id)

    def register_user(self, first_name, last_name, email, password, is_admin=False):
        if not first_name:
            print("First name must not be empty.")
            return None
        if not last_name:
            print("Last name must not be empty.")
            return None
        if not User.is_valid_email(email):
            print("Invalid email address.")
            return None
        if not User.is_strong_password(password):
            print("Password is not strong enough.")
            return None

        user = User(first_name, last_name, email, password, is_admin)
        self.user_repository.add(user)
        print("User registered successfully.")
        return user

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
            print(f"Place '{place.title}' added successfully.")
            return True
        else:
            print("Place already added.")
            return False


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
        print(f"Amenity '{name}' added successfully to place '{place.title}'.")
        return True
