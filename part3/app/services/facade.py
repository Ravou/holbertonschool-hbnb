from app.persistence.repository import UserRepository
from app.persistence.repository import PlaceRepository
from app.persistence.repository import ReviewRepository
from app.persistence.repository import ReservationRepository
from app.persistence.repository import AmenityRepository

from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.reservation import Reservation
from app.models.amenity import Amenity
from typing import Optional, List
from datetime import datetime
from app import db

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository(User)
        self.place_repo = PlaceRepository(Place)
        self.review_repo = ReviewRepository(Review)
        self.amenity_repo = AmenityRepository(Amenity)
        self.reservation_repo = ReservationRepository(Reservation)

# --------- USER ----------
    def create_user(self, first_name: str, last_name: str, email: str, password, is_admin=False) -> User:
        if self.get_user_by_email(email):
            raise ValueError("Email already registered.")
        user = User(first_name, last_name, email, password, is_admin)
        user.hash_password(password)
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
        db.session.commit()
        return user

    def get_user_by_email(self, email) -> Optional[User]:
        return self.user_repo.get_by_attribute('email', email)

    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)
        if not user:
            return None
        if user.verify_password(password):
            return user
        else:
            return None


    # --------- PLACE ----------
    def create_place(self, title: str, description: str, price: float, latitude: float, longitude: float, owner: User, amenities: Optional[List[Amenity]] = None) -> Place:
        place = Place(title=title, description=description, price=price, latitude=latitude, longitude=longitude, owner=owner)

        if amenities:
            for amenity in amenities:
                place.add_amenity(amenity)

        self.place_repo.add(place)
        owner.add_place(place)
        db.session.commit()

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
        reservation_id = review_data.get('reservation_id')
        text = review_data.get('text', '')
        rating = review_data.get('rating')

        if not user_id or not place_id or rating is None or not text or not reservation_id:
            raise ValueError

        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        reservations = self.reservation_repo.get_all()

        reservation = next(
           (r for r in reservations if r.user_id == user_id and r.place_id == place_id),
           None
        )
        if not reservation:
            raise ValueError("User must have a reservation for this place to leave a review")

        review = Review(user, place, reservation, text, rating)
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

        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id: str, current_user_id: str) -> bool:
        review = self.review_repo.get(review_id)
        if not review:
            return False

        if review.user_id != current_user_id:
            raise PermissionError('You can delete someone else review.')

        self.review_repo.delete(review_id)
        return True

    # --------- RESERVATION ----------
    def create_reservation(self, user_id, place_id, start_date, end_date, number_of_guests):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        reservation = Reservation(user, place, start_date, end_date, number_of_guests)
        self.reservation_repo.add(reservation)
        user.add_reservation(reservation)
        return reservation

    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        return self.reservation_repo.get(reservation_id)

    def get_all_reservations(self) -> List[Reservation]:
        return self.reservation_repo.get_all()

    def update_reservation(self, reservation_id: str, data: dict) -> Optional[Reservation]:
        reservation = self.get_reservation(reservation_id)
        if not reservation:
            return None

        allowed_fields = ['start_date', 'end_date', 'number_of_guests']
        for key, value in data.items():
            if key in allowed_fields and hasattr(reservation, key):
                setattr(reservation, key, value)

        db.session.commit()
        
        self.reservation_repo.update(reservation_id, data)
        return reservation

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
