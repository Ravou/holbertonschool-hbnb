from app.models.base_model import BaseModel
from typing import List

class Review(BaseModel):
    _reviews: List['Review'] = []
    

    def __init__(self, user_id, place_id, text, rating):
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.text = text
        self.rating = rating
        Review._reviews.append(self)

    def is_valid_rating(self):
        return 1 <= self.rating <= 5

    @classmethod
    def create_review(cls, user_id, place_id, text, rating):
        review = Review(user_id, place_id, text, rating)
        cls._reviews.append(review)
        return review

    @classmethod
    def list_by_place(cls, place_id: str) -> List[Review]:
        return [review for review in cls._reviews if review.place_id]

    @classmethod
    def list_by_user(cls, user_id: str) -> List[Review]:
        return [review for review in cls._reviews if review.user_id]

    def __repr__(self):
        return (
                f"Review(id='{self.id}', user_id='{self.user_id}',"
                f"place_id='{self.place_id}', text='{self.text}', rating={self.rating})"
                )
