from __future__ import annotations
from typing import List
from app.models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer
from flask_bcrypt import Bcrypt
from app import db
from uuid import uuid4
from typing import TYPE_CHECKING
bcrypt = Bcrypt()

if TYPE_CHECKING:
    from .place import Place
    from .review import Review
    from .reservation import Reservation

class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda:str(uuid4()))
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    places: Mapped[List["Place"]] = relationship("Place", back_populates="owner", lazy="select")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user", lazy="select")
    reservations: Mapped[List["Reservation"]] = relationship("Reservation", back_populates="user", lazy="select")

    allowed_update_fields = ['first_name', 'last_name']

    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin: bool = False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)  # utilise directement le hash
        
        if isinstance(is_admin, str):
            self.is_admin = is_admin.lower() == "true"
        else:
            self.is_admin = bool(is_admin)


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

