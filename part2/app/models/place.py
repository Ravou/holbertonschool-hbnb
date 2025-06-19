from app.models.base_model import BaseModel
from app.models.amenity import Amenity
from typing import List

class Place(BaseModel):

    _places = []

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner.id if hasattr(owner, 'id') else owner
        self.amenity_ids = []
        self.reservation_ids = []
        self.review_ids = []
        Place._places.append(self)


    @classmethod
    def list_all(cls) -> List['Place']:
        return cls._places

    def __repr__(self):
        amenity_names = [Amenity.get_by_id(aid).name for aid in self.amenity_ids]
        return f"Place(id='{self.id}', title='{self.title}', amenities={amenity_names})"

