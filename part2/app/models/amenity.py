from typing import List
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    _amenities: List['Amenity'] = []

    def __init__(self, name: str, description: str):
        super().__init__()
        self.name = name
        self.description = description
        Amenity._amenities.append(self)

    @classmethod
    def list_all(cls) -> List['Amenity']:
        return cls._amenities

    @classmethod
    def get_by_id(cls, id: str) -> 'Amenity' or None:
        for amenity in cls._amenities:
            if amenity.id == id:
                return amenity
        return None

    def __repr__(self):
        return f"Amenity(id='{self.id}', name='{self.name}', description='{self.description}')"

