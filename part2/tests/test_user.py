from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.reservation import Reservation
from app.models.amenity import Amenity

def test_user_relationships():
    # Create a user
    user = User(
        first_name="Alice",
        last_name="Dupont",
        email="alice@example.com",
        is_admin=True
    )

    # Check user is saved
    assert user in User.list_all()

    # Create a place
    place = Place(
        title="Vacation Home",
        description="Beautiful house by the sea",
        price=150,
        latitude=43.6108,
        longitude=3.8767,
        owner=user
    )
    user.add_place(place)
    assert place in user.places

    # Create a review
    review = Review(
        user=user,
        place=place,
        text="Amazing experience!",
        rating=5
    )
    place.add_review(review)
    assert review in place.reviews

    # Create a reservation
    reservation = Reservation(
        user=user,
        place=place,
        date="2025-07-01 to 2025-07-07"
    )
    place.add_reservation(reservation)
    assert reservation in place.reservations

    # Create an amenity
    amenity = Amenity(
            name="WiFi",
            description="Wireless internet access"
    )
    place.add_amenity(amenity)
    assert amenity in place.amenities

