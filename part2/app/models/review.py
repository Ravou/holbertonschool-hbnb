from models.base_model import BaseModel
from typing import List

class Review(BaseModel):
    _reviews: List['Review'] = []
    

    def __init__(self, name, place, text, rating):
        super().__init__()
        self.name = name
        self.place = place
        self.text = text
        self.rating = rating

        Review._reviews.append(self)

    @classmethod
    def list_by_place(cls, place_id: str) -> List['Review']:
        return [review for review in cls.reviews if review.place_id == place_id]

    def __repr__(self):
    return f"Review(id='{self.id}', user_id='{self.user_id}',"
           f"place_id='{self.place_id}', comment='{self.comment}', rating={self.rating})"
