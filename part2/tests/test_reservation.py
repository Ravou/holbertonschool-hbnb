from app.models.place import Place
from app.models.user import User
from app.models.reservation import Reservation

def test_reservation_relationships_and_review_logic():
    # Clean up before the test
    Reservation._reservations.clear()
    Place._places.clear()

    # Create a user
    user = User("John", "Doe", "john.doe@example.com", "StrongPass1", False)
    user.reservation_ids = []

    # Create a place
    place = Place(
        title="Charming Loft",
        description="A nice loft in the city center",
        price=200,
        latitude=40.7128,
        longitude=-74.0060,
        owner=user
    )
    place.reservation_ids = []

    # Create a reservation
    reservation = Reservation(user=user, place=place, date="2025-07-01")

    # Test entity-to-entity relationships
    assert reservation.user_id == user.id
    assert reservation.place_id == place.id
    assert reservation.id in user.reservation_ids
    assert reservation.id in place.reservation_ids

    # Test that reservation is registered in the class collection
    assert reservation in Reservation.get_all_reservation()
    assert reservation in Reservation.all()

    # Test retrieval of reservations by user
    reserved_places = Reservation.reservations_by(user.id)
    assert place in reserved_places

    # Test the review logic: user can only review if they have reserved the place
    def user_has_reserved_place(user_id, place_id):
        return any(
            r.user_id == user_id and r.place_id == place_id
            for r in Reservation._reservations
        )

    # Should be True: user has reserved the place
    assert user_has_reserved_place(user.id, place.id)

    # Negative test: another user or another place
    other_user = User("Jane", "Smith", "jane.smith@example.com", "SafePass2", False)
    other_place = Place(
        title="Country House",
        description="Peaceful house in the countryside",
        price=150,
        latitude=45.7640,
        longitude=4.8357,
        owner=user
    )
    other_user.reservation_ids = []
    other_place.reservation_ids = []

    # Should be False: other user has not reserved the place
    assert not user_has_reserved_place(other_user.id, place.id)
    # Should be False: user has not reserved the other place
    assert not user_has_reserved_place(user.id, other_place.id)

    print("Reservation relationship and review logic test passed.")

if __name__ == "__main__":
    test_reservation_relationships_and_review_logic()

