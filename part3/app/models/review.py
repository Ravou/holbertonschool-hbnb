from sqlalchemy import String, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'Review'

    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    place_id: Mapped[str] = mapped_column(String(36), nullable=False)
    reservation_id: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)

    text: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="reviews")
    place: Mapped["Place"] = relationship("Place", back_populates="reviews")
    reservation: Mapped["Reservation"] = relationship("Reservation", back_populates="review")

    allowed_update_fields = ['rating', 'text']

    def __init__(self, user_id: str, place_id: str, reservation_id: str, text: str, rating: int):
        self.user_id = user_id
        self.place_id = place_id
        self.reservation_id = reservation_id
        self.text = text
        self.rating = rating


    def is_valid_rating(self) -> bool:
        return 1 <= self.rating <= 5

    def __repr__(self):
        return (
            f"Review(id='{self.id}', user_id='{self.user_id}', "
            f"place_id='{self.place_id}', text='{self.text}', rating={self.rating})"
        )
