from typing import List
from app.models.place import Place
from app.models.amenity import Amenity

class PlaceService:
    _place = []

    @classmethod
    def get_by_criteria(cls, user_amenities: List[str]) -> List['Place']:
        return [
            place for place in cls._place
            if all(
                any(
                    Amenity.get_by_id(amenity_id).name == user_amenity
                    for amenity_id in place.amenity_ids
                )
                for user_amenity in user_amenities
            )
        ]

