from typing import List
from models.base_model import BaseModel

class Amenity(BaseModel):
    _amenities: List['Amenity'] = []

    def __init__(self, place, name, description):
        super.__init__()
        self.place = place
        self.name = name
        self.description = description

        Amenity._amenities.append(self)

        @clasmethod
        def list_all(cls) -> List['Amenity']:
            return cls._amenities

        def __repr__(self):
        return f"Amenity(name='{self.name}')"
