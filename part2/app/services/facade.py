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
        self.reservation_repo = InMemoryRepository()

# --------- USER ----------
    def create_user(self, first_name: str, last_name: str, email: str, is_admin=False) -> User:
        user = User(first_name, last_name, email, is_admin)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repo.get(user_id)

    def list_users(self) -> List[User]:
        return self.user_repo.all()

    # --------- PLACE ----------
    def create_place(self, title: str, description: str, price: float, latitude: float, longitude: float, owner: User) -> Place:
        place = Place(title, description, price, latitude, longitude, owner)
        self.place_repo.add(place)
        owner.add_place(place)
        return place

    def get_place(self, place_id: str) -> Optional[Place]:
        return self.place_repo.get(place_id)

    def list_places(self) -> List[Place]:
        return self.place_repo.all()

    # --------- REVIEW ----------
    def create_review(self, user: User, place: Place, content: str, rating: int) -> Review:
        review = Review.create_review(user, place, content, rating)
        self.review_repo.add(review)
        user.add_review(review)
        place.add_review(review)
        return review

    def list_reviews(self) -> List[Review]:
        return self.review_repo.all()


    # --------- RESERVATION ----------
    def create_reservation(self, user: User, place: Place, start_date, end_date) -> Reservation:
        reservation = Reservation(user, place, start_date, end_date)
        self.reservation_repo.add(reservation)
        user.add_reservation(reservation)
        return reservation

    def list_reservations(self) -> List[Reservation]:
        return self.reservation_repo.all()

    # --------- AMENITY ----------
    def create_amenity(self, name: str, description: str) -> Amenity:
        amenity = Amenity(name, description)
        self.amenity_repo.add(amenity)
        return amenity

    def list_amenities(self) -> List[Amenity]:
        return self.amenity_repo.all()
