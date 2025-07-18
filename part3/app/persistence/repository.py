from abc import ABC, abstractmethod
from app.models import User, Place, Reservation, Review, Amenity
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import db

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.db = db
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        attr = getattr(self.model, attr_name)
        results = db.session.query(self.model).filter(attr == attr_value).first()
        return results


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        if obj.id in self._storage:
            raise ValueError(f"Object with id {obj.id} already exists.")
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        results = [obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value]
        return results[0] if results else None


class UserRepository(SQLAlchemyRepository):
    def __init__(self, model=User):
        super().__init__(User)

    def get_by_email(self, email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    def get_by_id(self, user_id: str) -> User | None:
        return User.query.get(user_id)

    def list_all(self) -> List[User]:
        return User.query.all()

    def create(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self, model=Place):
        super().__init__(Place)
        self.db = db

    def add_review(self, place: Place, review):
        if review not in place.reviews:
            place.reviews.append(review)
            self.db.commit()
            self.db.refresh(place)

    def add_amenity(self, place: Place, amenity: Amenity):
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            self.db.commit()
            self.db.refresh(place)

    def add_reservation(self, place: Place, reservation):
        if reservation not in place.reservations:
            place.reservations.append(reservation)
            self.db.commit()
            self.db.refresh(place)

    def list_all(self) -> List[Place]:
        return super().get_all()

    def get_by_criteria(self, user_amenities: List[str]) -> List[Place]:

        subquery = (
            self.db.query(Place)
            .join(Place.amenities)
            .filter(Amenity.name.in_(user_amenities))
            .group_by(Place.id)
            .having(
                func.count(Amenity.id) == len(user_amenities)
            )
            .all()
        )
        return subquery

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self, model=Amenity):
        super().__init__(Amenity)
        self.db = db

    def list_all(self) -> List[Amenity]:
        return super().get_all()

    def get_by_id(self, id: str) -> Amenity | None:
        return self.db.query(Amenity).filter_by(id=id).first()

    def save(self, amenity: Amenity) -> Amenity:
        self.db.add(amenity)
        self.db.commit()
        self.db.refresh(amenity)
        return amenity



class ReservationRepository(SQLAlchemyRepository):
    def __init__(self, model=Reservation):
        super().__init__(Reservation)
        self.db = db

    def list_all(self) -> List[Reservation]:
        return super().get_all()

    def reservations_by_user(self, user_id: str) -> list[Reservation]:
        return self.db.query(Reservation).filter_by(user_id=user_id).all()

    def places_reserved_by_user(self, user_id: str) -> list[Place]:
        return (
            self.db.query(Place)
            .join(Reservation)
            .filter(Reservation.user_id == user_id)
            .all()
        )

    def save(self, reservation: Reservation) -> Reservation:
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self, model=Review):
        super().__init__(Review)
        self.db = db


    def list_by_place(self, place_id: str) -> List[Review]:
        return self.db.query(Review).filter_by(place_id=place_id).all()

    def list_by_user(self, user_id: str) -> List[Review]:
        return self.db.query(Review).filter_by(user_id=user_id).all()

    def create_review(self, user_id: str, place_id: str, text: str, rating: int) -> Review:

        past_reservation = (
            self.db.query(Reservation)
            .filter(
                Reservation.user_id == user_id,
                Reservation.place_id == place_id,
                Reservation.end_date < date.today()
            )
            .outerjoin(Review, Reservation.id == Review.reservation_id)
            .filter(Review.id == None)  # Pas encore de review liée
            .first()
        )

        if not past_reservation:
            raise ValueError("User must have a past reservation for this place and must not have reviewed it yet.")

        review = Review(
            user_id=user_id,
            place_id=place_id,
            reservation_id=past_reservation.id,
            text=text,
            rating=rating
        )

        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review
