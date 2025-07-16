from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4

class Amenity(BaseModel):
    __tablename__ = "Amenity"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    allowed_update_fields = ['name', 'description']

    def __init__(self, name: str, description: str = None):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Amenity(id='{self.id}', name='{self.name}', description='{self.description}')"

