from models.base_model import BaseModel
from typing import List

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin):
    super().__init__()
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.__password = password
    self.is_admin = is_admin
    self.reservations = []
    self.place = []
    self.review = []

    def register ():
        if self.first_name == "":
            print("First name must not be empty.")
            return False
        elif self.last_name == "":
            print("Last name must not be empty.")
            return False
        elif self.is_valid_email(self.email) is False:
            print("Invalid email address.")
            return False
        elif self.is_strong_password(self.__password) is False:
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
        if len(password) < 8:
            return False
        elif any(c.isupper() for c in password) is False:
            return False
        elif any(c.isdigit() for c in password) is False:
            return False
        else:
            return True

    def authenticate(self, password: str) -> bool:
        return self.__password == password

    @classmethod
    def login(cls, email, password, users_list):
        user = None
        for u in users_list:
            if u.email == email:
                user = u
                break

        if user is None:
            print("User not found.")
            return False
        elif user.authenticate(password) is True:
            print(f"Welcome, {user.first_name}!")
            return True
        else:
            print("Incorrect password.")
            return False

    
    def add_place(self, place):
        if isinstance(place, Place) is False:
            print("Invalid place object.")
            return False
        else:
            self.places.append(place)
            place.owner = self
            print(f"Place '{place.name}' added successfully.")
            return True


    def has_reserved(self, place):
        for res in self.reservations:
            if res.place == place:
                return True
        return False

    def add_review(self, text, rating, place):
        if self.has_reserved(place) is False:
            print("You must reserve the place before adding a review.")
            return False
        elif rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            return False
        else:
            review = Review(text=text, rating=rating, place=place, user=self)
            self.reviews.append(review)
            place.reviews.append(review)
            print("Review added successfully.")
            return True

    def add_amenity(self, place, name, description):
        if isinstance(place, Place) is False:
            print("Invalid place object.")
            return False
        else:
            amenity = Amenity(name=name, description=description)
            place.amenities.append(amenity)
            print(f"Amenity '{name}' added successfully to place '{place.name}'.")
            return True
