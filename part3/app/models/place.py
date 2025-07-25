from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Table, String, DECIMAL, Float, ForeignKey
from typing import List, Optional
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.user import User

place_amenities = db.Table(
    "place_amenities",
    db.metadata,
    db.Column("place_id", ForeignKey("Place.id"), primary_key=True),
    db.Column("amenity_id", ForeignKey("Amenity.id"), primary_key=True),
)

class Place(BaseModel):
    __tablename__ = "Place"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey('User.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships

    reservations: Mapped[List["Reservation"]] = relationship("Reservation", back_populates="place")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="place")
    owner: Mapped["User"] = relationship("User", back_populates="places")
    amenities: Mapped[List["Amenity"]] = relationship("Amenity", secondary="place_amenities", back_populates="places")

    allowed_update_fields = ['title', 'description', 'price', 'address', 'city', 'state']


    def __init__(self, title: str, description: str, price: float, address: str, city: str, state: str, latitude: float = None, longitude: float = None, owner: "User" = None):
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.city = city
        self.state = state
        self.owner = owner
    
    def full_address(self):
        return f"{self.address}, {self.city}, {self.state}"


    def __repr__(self):
        amenity_names = [amenity.name for amenity in self.amenities]
        return (
            f"Place(id={repr(self.id)}, title={repr(self.title)}, address={repr(self.address)}, "
            f"city={repr(self.city)}, state={repr(self.state)}, price={self.price}, "
            f"latitude={self.latitude}, longitude={self.longitude}, "
            f"amenities={amenity_names})"
        )

