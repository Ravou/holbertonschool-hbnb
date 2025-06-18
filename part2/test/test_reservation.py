from app.models.reservation import Reservation
from app.models.user import User
from app.models.place import Place

def test_reservation_creation():
    user = User(first_name="Emma", last_name="Stone", email="emma.stone@example.com")
    place = Place(title="Charming Studio", description="Central location", price=80, latitude=45.7640, longitude=4.8357, owner=user)
    reservation = Reservation(user=user, place=place, start_date="2025-07-01", end_date="2025-07-10")
    assert reservation.user == user
    assert reservation.place == place
    assert reservation.start_date == "2025-07-01"
    assert reservation.end_date == "2025-07-10"
    print("Reservation creation test passed!")

def test_reservation_dates():
    user = User(first_name="Liam", last_name="Brown", email="liam.brown@example.com")
    place = Place(title="Lake House", description="Peaceful view", price=200, latitude=44.8378, longitude=-0.5792, owner=user)
    reservation = Reservation(user=user, place=place, start_date="2025-08-15", end_date="2025-08-20")
    # Vérifie que la date de début est avant la date de fin (à adapter selon ta logique)
    assert reservation.start_date < reservation.end_date
    print("Reservation date logic test passed!")
