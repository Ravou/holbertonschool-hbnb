from __future__ import annotations

from typing import Union, TYPE_CHECKING, List
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.place import Place

class Review(BaseModel):
    _reviews: List['Review'] = []

    def __init__(self, user: Union["User", str], place: Union["Place", str], text: str, rating: int):
        from app.models.user import User
        from app.models.place import Place

        super().__init__()
        self.user_id = user.id if isinstance(user, User) else user
        self.place_id = place.id if isinstance(place, Place) else place
        self.text = text
        self.rating = rating
        Review._reviews.append(self)
        if isinstance(user, User):
            user.add_review(self)
        if isinstance(place, Place):
            place.add_review(self)

    def is_valid_rating(self) -> bool:
        return 1 <= self.rating <= 5

    @classmethod
    def create_review(cls, user: Union[User, str], place: Union[Place, str], text: str, rating: int) -> 'Review':
        return cls(user, place, text, rating)

    @classmethod
    def list_by_place(cls, place_id: str) -> List['Review']:
        return [review for review in cls._reviews if review.place_id == place_id]

    @classmethod
    def list_by_user(cls, user_id: str) -> List['Review']:
        return [review for review in cls._reviews if review.user_id == user_id]

    def __repr__(self):
        return (
            f"Review(id='{self.id}', user_id='{self.user_id}', "
            f"place_id='{self.place_id}', text='{self.text}', rating={self.rating})"
        )
