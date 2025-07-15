from sqlalchemy import String, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'Review'

    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    place_id: Mapped[str] = mapped_column(String(36), nullable=False)
    reservation_id: Mapped[str] = mapped_column(String(36), nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    allowed_update_fields = ['rating', 'text']

    def is_valid_rating(self) -> bool:
        return 1 <= self.rating <= 5

    def __repr__(self):
        return (
            f"Review(id='{self.id}', user_id='{self.user_id}', "
            f"place_id='{self.place_id}', text='{self.text}', rating={self.rating})"
        )
