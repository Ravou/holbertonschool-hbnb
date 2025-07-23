from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column

class Reservation(BaseModel):
    __tablename__ = 'Reservation'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    place_id: Mapped[str] = mapped_column(String(36), nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    number_of_guests: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="reservations")
    place: Mapped["Place"] = relationship("Place", back_populates="reservations")
    review: Mapped[Optional["Review"]] = relationship("Review", back_populates="reservation", uselist=False)

    allowed_update_fields = ['start_date', 'end_date', 'number_of_guests']

    def __init__(self, user_id: str, place_id: str, start_date, end_date, number_of_guests: int):
        self.user_id = user_id
        self.place_id = place_id
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_guests = number_of_guests

    def __repr__(self):
        return (f"Reservation(id='{self.id}', user_id='{self.user_id}', "
                f"place_id='{self.place_id}', start_date='{self.start_date}'," 
                f"end_date='{self.end_date}', guests={self.number_of_guests})") 

