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

    def __repr__(self):
        return (
                f"Review(id='{self.id}', user_id='{self.user_id}'," 
                f"place_id='{self.place_id}', text='{self.text}', rating={self.rating})"
                )

    def is_valid_rating(self):
        return 1 <= self.rating <= 5
