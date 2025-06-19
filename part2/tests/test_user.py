from app.models.user import User
from app.models.place import Place
from app.models.review import Review

def test_user_add_review_to_place():
    # Création d'un utilisateur et d'un lieu
    user = User("Alice", "Smith", "alice.smith@example.com", "StrongPass1", False)

    place = Place(title="Cozy Apartment", description="Nice", price=100, latitude=0.0, longitude=0.0, owner=user)

    # Simule une réservation pour permettre l'ajout d'un avis
    user.reservation_ids.append(place.id)
    place.reservation_ids.append(user.id)

    # Ajout d'un avis
    result = user.add_review("Super séjour", 5, place)

    # Vérifie que l'ajout a réussi
    assert result is True
    # Vérifie que l'identifiant de l'avis est bien dans les listes correspondantes
    assert len(user.review_ids) == 1
    assert user.review_ids[0] in place.review_ids

    print("Test relation User-Place-Review réussi !")

if __name__ == "__main__":
    test_user_add_review_to_place()
