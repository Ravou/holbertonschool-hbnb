from app.models.base_model import BaseModel
from app.models.review import Review
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

    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    
    @staticmethod
    def is_strong_password(password: str) -> bool:
        return (len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password))

    def authenticate(self, password: str) -> bool:
        return self.__password == password

    def has_reserved(self, place):
        return place.id in self.reservation_ids

    def __repr__(self):
        return f"User(id='{self.id}', email='{self.email}', is_admin={self.is_admin})"
