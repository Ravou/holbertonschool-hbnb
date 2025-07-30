import pytest
from app.models.amenity import Amenity

def test_amenity_creation_and_methods():
    # Création de quelques amenities
    amenity1 = Amenity(name="WiFi", description="Wireless internet access")
    amenity2 = Amenity(name="Pool", description="Outdoor swimming pool")
    
    # Vérifie que les attributs sont correctement assignés
    assert amenity1.name == "WiFi"
    assert amenity1.description == "Wireless internet access"
    assert amenity2.name == "Pool"
    
    # Vérifie que les amenities sont dans la liste de classe
    all_amenities = Amenity.list_all()
    assert amenity1 in all_amenities
    assert amenity2 in all_amenities
    
    # Vérifie la recherche par ID
    found = Amenity.get_by_id(amenity1.id)
    assert found == amenity1
    
    # Recherche d'un ID inexistant retourne None
    not_found = Amenity.get_by_id("nonexistent_id")
    assert not_found is None
    
    # Vérifie la représentation string
    repr_str = repr(amenity1)
    assert "WiFi" in repr_str
    assert "Wireless internet access" in repr_str
    assert amenity1.id in repr_str

if __name__ == "__main__":
    pytest.main()

