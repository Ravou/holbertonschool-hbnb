Class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin)
    super().__init__()
    self.first_name = first_name
    self.last_name = las_name
    self.email = email
    self.__password = password
    self.is_admin = is_admin
    self.reservations = []

    def register ():
        if not self.first_name or not self.last_name:
            print ("First name and last name must not be empty.")
            return False

        if not self.is_valid_email(self.mail):
            print("Invalid email adress.")
            return False
        
        if not self.is_strong_password(self.__password):
            print("Password is not strong enough.")
            return False

        print("User registered successfully.")
        return True

    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    
    @staticmethod
    def is_strong_password(password: str) -> bool:
        if len(password) < 8:
            return False

        if not any(c.isupper() for c in password):
            return False

        if not any(c.isdigit() for c in password):
            return False
        return True

    
    def login(email, password):
        user = next((u for u in users if u.email == email), None)
        if user is None:
            print("User not found.")
            return False

        if user.authenticate(password):
            print(f"Welcome, {user.first_name}!")
            return True
        else:
            print("Incorrect password.")
            return False

    
    def add_place(self, name, title, description, price, latitude, longitude, owner, amenities):
        if not name:
            print("Place name is required.")
            return False

        if not title:
            print("Place title is required.")
            return False

        if price < 0:
            print("Price cannot be negative.")
            return False

        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            print("Latitude and longitude must be numbers.")
            return False
        if not isinstance(amenities, list):
            print("Amenities must be a list.")
            return False

        place = {
            "name": name,
            "title": title,
            "description": description,
            "price": price,
            "latitude": latitude,
            "longitude": longitude,
            "owner": owner,
            "amenities": amenities
        }

        self.place.append(place)

        print(f"Place '{name}' added successfully.")
        return True


    def has_reserved(self, place):
        return any(res.place == place for res in self.reservations)

    place.reserved_by.append(user)

    def add_review(self, text, rating, place, user):
        if not user.has_reserved(place):
            print("You must reserve the place before adding a review.")
            return False
        if not (1 <= rating <= 5):
            print("Rating must be between 1 and 5.")
            return False

        review = {
                "text": text,
                "rating": rating,
                "place": place,
                "user": user
                }

        if not hasattr(place, 'review'):
            place.reviews = []
        place.reviews.append(review)

        print("Review added successfully.")
        return True

    def add_amenity(self, name, description):
        amenity = {
                "name": name,
                "description": description
                }
        if not hasattr(place, 'amenities'):
            place.amenities = []

        place.amenities.append(amenity)

        print(f"Amenity '{name}' added successfully to place '{place.name}'.")
        return True
