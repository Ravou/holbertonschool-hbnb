from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity

def test_amenity_relationship_and_logic():
    # Clean up before the test
    Amenity._amenities.clear()
    Place._places.clear()

    # Create an owner user
    owner = User("Alice", "Smith", "alice.smith@example.com", "StrongPass1", False)

    # Create a place
    place = Place(
        title="Cozy Apartment",
        description="Nice place",
        price=120,
        latitude=48.8566,
        longitude=2.3522,
        owner=owner
    )

    # Create an amenity linked to this place
    wifi = Amenity(place=place, name="WiFi", description="Wireless Internet")

    # Check that the amenity is linked to the correct place
    assert wifi.place_id == place.id

    # Check that the amenity is registered in the class collection
    assert wifi in Amenity.list_all()

    # Test retrieval by ID
    found = Amenity.get_by_id(wifi.id)
    assert found is wifi
    assert found.name == "WiFi"
    assert found.description == "Wireless Internet"

    # Create a secon amenity
    parking = Amenity(place=place, name="Parking", description="Private parking")
    assert parking.place_id == place.id

    # Check that both amenities are in the list
    all_amenities = Amenity.list_all()
    assert wifi in all_amenities
    assert parking in all_amenities

    # Test the string representation
    repr_str = repr(wifi)
    assert "WiFi" in repr_str
    assert str(place.id) in repr_str

    print("Amenity relationship and logic test passed.")

if __name__ == "__main__":
    test_amenity_relationship_and_logic()

