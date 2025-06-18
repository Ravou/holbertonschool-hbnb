from typing import List
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    _amenities: List['Amenity'] = []

    def __init__(self, place, name, description):
        super().__init__()
        self.place_id = place.id if hasattr(place, 'id') else place
        self.name = name
        self.description = description
        Amenity._amenities.append(self)

    @classmethod
    def list_all(cls) -> List['Amenity']:
        return cls._amenities

    @classmethod
    def get_by_id(cls, id):
        for amenity in cls._amenities:
            if amenity.id == id:
                return amenity
        return None

    def __repr__(self):
        return f"Amenity(id='{self.id}', place_id='{self.place_id}'," f"name='{self.name}', description='{self.description}')"
