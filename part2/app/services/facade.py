from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.reservation import Reservation
from app.models.amenity import Amenity
from typing import Optional, List
from datetime import datetime
class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.reservation_repo = InMemoryRepository()

# --------- USER ----------
    def create_user(self, first_name: str, last_name: str, email: str, is_admin=False) -> User:
        if self.get_user_by_email(email):
            raise ValueError("Email already registered.")
        user = User(first_name, last_name, email, is_admin)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repo.get(user_id)

    def list_users(self) -> List[User]:
        return self.user_repo.get_all()

    def update_user(self, user_id, new_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in new_data.items():
            setattr(user, key, value)
        return user

    def get_user_by_email(self, email):
        users = self.user_repo.get_by_attribute('email', email)
        return users[0] if users else None


    # --------- PLACE ----------
    def create_place(self, title: str, description: str, price: float, latitude: float, longitude: float, owner: User) -> Place:
        place = Place(title, description, price, latitude, longitude, owner)
        self.place_repo.add(place)
        owner.add_place(place)
        return place

    def get_place(self, place_id: str) -> Optional[Place]:
        return self.place_repo.get(place_id)

    def get_all_places(self) -> List[Place]:
        return self.place_repo.get_all()

    def update_place(self, place_id: str, data: dict) -> Optional[Place]:
        place = self.place_repo.get(place_id)
        if not place:
            return None
        protected_fields = {
                "id", "owner_id", "created_at", "updated_at",
                "owner", "reviews", "reservations", "amenities"
                }
        filtered_data = {k: v for k, v in data.items() if k not in protected_fields}
        self.place_repo.update(place_id, filtered_data)

        return place


    # --------- REVIEW ----------
    
    def create_review(self, review_data: dict) -> Review:
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        text = review_data.get('text', '')
        rating = review_data.get('rating')

        if not user_id or not place_id or rating is None:
            raise ValueError("Missing required fields: user_id, place_id, rating")
        reservations = self.reservation_repo.get_all()

        has_reservation = any(
            r for r in reservations if r.user_id == user_id and r.place_id == place_id
        )
        if not has_reservation:
            raise ValueError("User must have a reservation for this place to leave a review")
        review = Review(user_id=user_id, place_id=place_id, text=text, rating=rating)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id: str) -> Optional[Review]:
        return self.review_repo.get(review_id)

    def get_all_reviews(self) -> List[Review]:
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        return self.review_repo.list_by_place(place_id)

    def update_review(self, review_id: str, review_data: dict) -> Optional[Review]:
        review = self.review_repo.get(review_id)
        if not review:
            return None

        for key, value in review_data.items():
            if key in review.allowed_update_fields and hasattr(review, key):
                setattr(review, key, value)

        review.updated_at = datetime.utcnow()
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id: str) -> bool:
        review = self.review_repo.get(review_id)
        if not review:
            return False

        self.review_repo.delete(review_id)
        return True

    # --------- RESERVATION ----------
    def create_reservation(self, user: User, place: Place, start_date, end_date) -> Reservation:
        reservation = Reservation(user, place, start_date, end_date)
        self.reservation_repo.add(reservation)
        user.add_reservation(reservation)
        return reservation

    def list_reservations(self) -> List[Reservation]:
        return self.reservation_repo.all()

    # --------- AMENITY ----------
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)
    
    def get_amenity_by_name(self, amenity_name):
        return self.amenity_repo.get_by_attribute('name', amenity_name)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
            self.amenity_repo.update(amenity_id, amenity_data)
            return amenity

facade = HBnBFacade()
