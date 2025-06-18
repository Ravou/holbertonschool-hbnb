from models.base_model import BaseModel
from typing import List

class Review(BaseModel):
    _reviews: List['Review'] = []
    

    def __init__(self, user, place, text, rating):
        super().__init__()
        self.user_id = user.id if hasattr(user, 'id') else user
        self.place_id = place.id if hasattr(place, 'id') else place
        self.text = text
        self.rating = rating
        Review._reviews.append(self)

    @classmethod
    def list_by_place(cls, place_id: str) -> List['Review']:
        return [review for review in cls._reviews if review.place_id == place_id]

    def __repr__(self):
        return (
                f"Review(id='{self.id}', user_id='{self.user_id}'," 
                f"place_id='{self.place_id}', text='{self.text}', rating={self.rating})"
                )
