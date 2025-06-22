from app.models.user import User
from app.models.place import Place
from app.models.reservation import Reservation
from app.models.user import User
from app.models.place import Place
from app.models.reservation import Reservation

def test_reservation_relationship_and_logic():
    user = User(first_name="Alice", last_name="Dupont", email="alice@example.com")

    place = Place(
        title="Seaside Villa",
        description="A beautiful villa by the sea",
        price=150,
        latitude=45.0,
        longitude=-73.0,
        owner=user
    )

    reservation = Reservation(user, place, "2025-07-01 to 2025-07-07")

    assert reservation in user.reservations, "Reservation should be in user's reservations list"
    assert reservation in place.reservations, "Reservation should be in place's reservations list"
    assert reservation in Reservation.list_all(), "Reservation should be in the global Reservation list"
    assert reservation in Reservation.reservations_by_user(user.id), "Reservation should be found by reservations_by_user"
    assert place in Reservation.places_reserved_by_user(user.id), "Place should be found by places_reserved_by_user"

if __name__ == "__main__":
    test_reservation_relationship_and_logic()
    print("All tests passed!")

