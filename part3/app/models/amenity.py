from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.config.database import Base  # Le Base SQLAlchemy (déclarative_base)
import uuid

class Amenity(BaseModel):
    __tablename__ = "amenities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    allowed_update_fields = ['name', 'description']


    def __repr__(self):
        return f"Amenity(id='{self.id}', name='{self.name}', description='{self.description}')"

