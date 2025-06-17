Class Place(BaseModel):
    def __init__(self, name, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.name = name
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.amenities = []
        self.reservations = []

    def get_all_reservations(self):
        return self.reservations
