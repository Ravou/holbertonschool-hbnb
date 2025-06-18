from models.base_model import BaseModel
from typing import List

class Place(BaseModel):

    _places = []

    def __init__(self, name, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.name = name
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner
        self.amenities = []
        self.reservations = []
        Place._places.append(self)


    @classmethod
    def list_all(cls) -> List['Place']:
        return cls._places
        
    @classmethod
    def get_by_criteria(cls, user_amenities: List[str]) -> List['Place']:
        return [
                place for place in cls._places
                if all(any(amenity.name == user_amenity for amenity in place.amenities) for user_amenity in user_amenities)
                ]

    def __repr__(self):
        return f"Place(id='{self.id}', name='{self.name}', amenities={self.amenities})"

