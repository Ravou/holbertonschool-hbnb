from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity

def test_place_relationships_and_logic():
    # Clean up before the test
    Place._places.clear()
    Amenity._amenities = []

    # Create an owner user
    owner = User("Alice", "Smith", "alice.smith@example.com", "StrongPass1", False)

    # Create the place first

    place = Place(title="Cozy Apartment", description="Nice place", price=100, latitude=48.85, longitude=2.35, owner=owner)

    # Create amenities

    wifi = Amenity(name="WiFi", description="Wireless Internet", place=place)
    parking = Amenity(name="Parking", description="Private parking", place=place)

    place.amenity_ids.extend([wifi.id, parking.id])

    # Check owner-place relationship
    assert place.owner_id == owner.id
    assert place in Place.list_all()
    
    # Check place-amenity relationship
    amenity_names = [Amenity.get_by_id(aid).name for aid in place.amenity_ids]
    assert "WiFi" in amenity_names
    assert "Parking" in amenity_names

    # Test logic for amenity-based search
    result = Place.get_by_criteria(["WiFi"])
    assert place in result
    result = Place.get_by_criteria(["WiFi", "Parking"])
    assert place in result
    result = Place.get_by_criteria(["Pool"])
    assert place not in result

    print("Place relationship and logic test passed.")

if __name__ == "__main__":
    test_place_relationships_and_logic()

