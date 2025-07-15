from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, DECIMAL, Float, ForeignKey
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.user import User

class Place(BaseModel):
    __tablename__ = 'Place'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)



    allowed_update_fields = ['title', 'description', 'price_per_night', 'address']

    def __repr__(self):
        amenity_names = [amenity.name for amenity in self.amenities]
        return f"Place(id='{self.id}', title='{self.title}', amenities={amenity_names})"

