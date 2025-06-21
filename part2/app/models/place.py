from app.models.base_model import BaseModel
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.reservation import Reservation
from typing import List

class Place(BaseModel):
    _places: List['Place'] = []

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # Lien direct vers un objet User
        self.amenities: List[Amenity] = []
        self.reviews: List[Review] = []
        self.reservations: List[Reservation] = []
        Place._places.append(self)

    def add_review(self, review: Review):
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity: Amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_reservation(self, reservation: Reservation):
        if reservation not in self.reservations:
            self.reservations.append(reservation)

    @classmethod
    def list_all(cls) -> List['Place']:
        return cls._places

    @classmethod
    def get_by_criteria(cls, user_amenities: List[str]) -> List['Place']:
        return [
                place for place in cls._places
                if all(
                    any(amenity.name == user_amenity for amenity in place.amenities)
                    for user_amenity in user_amenities
                    )
                ]


    def __repr__(self):
        amenity_names = [amenity.name for amenity in self.amenities]
        return f"Place(id='{self.id}', title='{self.title}', amenities={amenity_names})"

