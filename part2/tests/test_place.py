import pytest

from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.reservation import Reservation

def test_place_relationships_and_business_logic():
    # Création d'un utilisateur
    user = User(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        is_admin=False
    )

    # Création d'un lieu
    place = Place(
        title="Beach House",
        description="Nice house by the beach",
        price=200,
        latitude=36.7783,
        longitude=-119.4179,
        owner=user
    )

    # Vérifier que le lieu est bien enregistré
    assert place in Place.list_all()
    assert place.owner == user

    # Création et ajout d'amenities
    wifi = Amenity(name="WiFi", description="Wireless internet access")
    pool = Amenity(name="Pool", description="Swimming pool")
    place.add_amenity(wifi)
    place.add_amenity(pool)
    assert wifi in place.amenities
    assert pool in place.amenities

    # Création et ajout de reviews
    review1 = Review(user=user, place=place, text="Great stay!", rating=5)
    place.add_review(review1)
    assert review1 in place.reviews

    # Création et ajout de réservations
    reservation1 = Reservation(user=user, place=place, date="2025-07-01 to 2025-07-07")
    place.add_reservation(reservation1)
    assert reservation1 in place.reservations

    # Tester get_by_criteria avec une amenity existante
    criteria_result = Place.get_by_criteria(["WiFi"])
    assert place in criteria_result

    # Tester get_by_criteria avec une amenity inexistante
    criteria_result_empty = Place.get_by_criteria(["Jacuzzi"])
    assert place not in criteria_result_empty

    # Tester la représentation string (__repr__)
    repr_str = repr(place)
    assert "Beach House" in repr_str
    assert "WiFi" in repr_str and "Pool" in repr_str

if __name__ == "__main__":
    pytest.main()

