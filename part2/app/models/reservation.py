class Reservation(BaseModel):
    def __init__(self, user, place, date):
        super().__init__()
        self.user = user
        self.place = place
        self.date = date

        
        user.reservations.append(self)
        place.reservations.append(self)

