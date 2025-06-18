from app.models.amenity import Amenity

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")

def test_amenity_name_update():
    amenity = Amenity(name="Parking")
    amenity.name = "Free Parking"
    assert amenity.name == "Free Parking"
    print("Amenity name update test passed!")

