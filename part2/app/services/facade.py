from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.reservation import Reservation
from app.models.amenity import Amenity
from typing import Optional, List

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

# --------- USER ----------
    def create_user(self, first_name: str, last_name: str, email: str, is_admin=False) -> User:
        user = User(first_name, last_name, email, is_admin)
        self.users.append(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return next((u for u in self.users if u.id == user_id), None)

    def list_users(self) -> List[User]:
        return self.users

    # --------- PLACE ----------
    def create_place(self, title: str, description: str, price: float, latitude: float, longitude: float, owner: User) -> Place:
        place = Place(title, description, price, latitude, longitude, owner)
        self.places.append(place)
        owner.add_place(place)
        return place

    def get_place(self, place_id: str) -> Optional[Place]:
        return next((p for p in self.places if p.id == place_id), None)

    def list_places(self) -> List[Place]:
        return self.places

    # --------- REVIEW ----------
    def create_review(self, user: User, place: Place, content: str, rating: int) -> Review:
        review = Review(user, place, content, rating)
        self.reviews.append(review)
        user.add_review(review)
        place.add_review(review)
        return review

    def list_reviews(self) -> List[Review]:
        return self.reviews

    # --------- RESERVATION ----------
    def create_reservation(self, user: User, place: Place, start_date, end_date) -> Reservation:
        reservation = Reservation(user, place, start_date, end_date)
        self.reservations.append(reservation)
        user.add_reservation(reservation)
        return reservation

    def list_reservations(self) -> List[Reservation]:
        return self.reservations

    # --------- AMENITY ----------
    def create_amenity(self, name: str, description: str) -> Amenity:
        amenity = Amenity(name, description)
        self.amenities.append(amenity)
        return amenity

    def list_amenities(self) -> List[Amenity]:
        return self.amenities
