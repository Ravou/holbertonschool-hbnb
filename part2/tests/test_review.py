from app.models.user import User
from app.models.place import Place
from app.models.reservation import Reservation
from app.models.review import Review

def test_review_relationships_and_business_logic():
    # Nettoyage avant le test
    Review._reviews.clear()
    Reservation._reservations.clear()
    Place._places.clear()

    # Création d'un utilisateur
    user = User("Alice", "Smith", "alice.smith@example.com", "StrongPass1", False)
    user.reservation_ids = []

    # Création d'un lieu
    place = Place(
        title="Cozy Cottage",
        description="A quiet place in the countryside",
        price=150,
        latitude=48.8566,
        longitude=2.3522,
        owner=user
    )
    place.reservation_ids = []

    # Création d'une réservation liant user et place
    reservation = Reservation(user=user, place=place, date="2025-07-10")

    # Fonction métier : vérifier si l'utilisateur a réservé la place
    def user_can_review(user_id, place_id):
        return any(
            r.user_id == user_id and r.place_id == place_id
            for r in Reservation._reservations
        )

    # Vérification que l'utilisateur peut laisser un avis
    assert user_can_review(user.id, place.id) is True

    # Création d'un avis
    review_text = "Great place, very cozy and quiet."
    review_rating = 5
    review = Review(user_id=user.id, place_id=place.id, text=review_text, rating=review_rating)

    # Vérification des relations dans l'avis
    assert review.user_id == user.id
    assert review.place_id == place.id
    assert review.text == review_text
    assert review.rating == review_rating

    # Vérification que l'avis est bien enregistré dans la liste des avis
    assert review in Review._reviews

    # Vérification que l'avis est listé par place
    reviews_for_place = Review.list_by_place(place.id)
    assert review in reviews_for_place

    # Test négatif : un autre utilisateur sans réservation ne peut pas laisser d'avis
    other_user = User("Bob", "Jones", "bob.jones@example.com", "SafePass2", False)
    assert user_can_review(other_user.id, place.id) is False

    print("Review relationships and business logic test passed.")

if __name__ == "__main__":
    test_review_relationships_and_business_logic()

