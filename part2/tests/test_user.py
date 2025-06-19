import pytest
from app.services.facade import HBnBFacade

def test_user_can_add_review_to_reserved_place():
    from app.services.facade import HBnBFacade

    # Initialisation de la façade
    facade = HBnBFacade()

    # Création d'un utilisateur via la façade
    user = facade.register_user(
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@example.com",
        password="StrongPass1"
    )

    # Création d'un lieu via la façade
    place = facade.create_place(
        title="Cozy Apartment",
        description="Nice",
        price=100,
        latitude=0.0,
        longitude=0.0,
        owner_id=user.id
    )

    # Création d'une réservation pour l'utilisateur et ce lieu
    reservation = facade.create_reservation(
        user_id=user.id,
        place_id=place.id,
        date="2025-07-01"
    )

    # Ajout d'un avis via la façade
    review = facade.add_review(
        user_id=user.id,
        place_id=place.id,
        text="Super séjour",
        rating=5
    )

    # Vérifications des relations et de la logique métier
    assert review.user_id == user.id
    assert review.place_id == place.id
    assert review.rating == 5
    assert review.text == "Super séjour"

    # Vérifie que l'avis est bien listé pour ce lieu
    reviews_for_place = facade.get_reviews_for_place(place.id)
    assert any(r.id == review.id for r in reviews_for_place)

