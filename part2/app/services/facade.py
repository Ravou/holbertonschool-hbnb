from app.services.user_service import UserService
from app.services.place_service import PlaceService
from app.services.review_service import ReviewService
from app.services.amenity_service import AmenityService
from app.services.reservation_service import ReservationService

class HBnBFacade:
    def __init__(self):
        self.user_service = UserService()
        self.place_service = PlaceService()
        self.review_service = ReviewService()
        self.amenity_service = AmenityService()
        self.reservation_service = ReservationService()

    from app.services.user_service import UserService
from app.services.place_service import PlaceService
from app.services.review_service import ReviewService
from app.services.amenity_service import AmenityService
from app.services.reservation_service import ReservationService

class HBnBFacade:
    def __init__(self):
        self.user_service = UserService()
        self.place_service = PlaceService()
        self.review_service = ReviewService()
        self.amenity_service = AmenityService()
        self.reservation_service = ReservationService()

    # === User Operations ===
    def register_user(self, first_name, last_name, email, password, is_admin=False):
        return self.user_service.register_user(first_name, last_name, email, password, is_admin)

    def login_user(self, email, password):
        return self.user_service.login(email, password)

    def add_place_to_user(self, user_id, place_data):
        user = self.user_service.get_by_id(user_id)
        place = self.place_service.create_place(**place_data)
        return self.user_service.add_place_to_user(user, place)

    # === Place Operations ===
    def create_place(self, title, description, price, latitude, longitude, owner_id):
        owner = self.user_service.get_by_id(owner_id)
        return self.place_service.create_place(title, description, price, latitude, longitude, owner)

    def get_place(self, place_id):
        return self.place_service.get_place_by_id(place_id)

    def search_places(self, amenities=None):
        return self.place_service.find_places_by_amenities(amenities or [])

    # === Review Operations ===
    def add_review(self, user_id, place_id, text, rating):
        user = self.user_service.get_by_id(user_id)
        place = self.place_service.get_place_by_id(place_id)
        return self.review_service.create_review(user, place, text, rating)

    def get_reviews_for_place(self, place_id):
        return self.review_service.list_by_place(place_id)

    # === Reservation Operations ===
    def create_reservation(self, user_id, place_id, date):
        user = self.user_service.get_by_id(user_id)
        place = self.place_service.get_place_by_id(place_id)
        return self.reservation_service.create_reservation(user, place, date)

    def get_user_reservations(self, user_id):
        return self.reservation_service.reservations_by_user(user_id)

    # === Amenity Operations ===
    def add_amenity_to_place(self, place_id, name, description):
        place = self.place_service.get_place_by_id(place_id)
        return self.amenity_service.add_amenity_to_place(place, name, description)

