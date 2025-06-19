from typing import List
from app.models.review import Review

class ReviewService:
    _reviews: List[Review] = []

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
