from app.models.user import User
from app.models.place import Place
from app.models.reservation import Reservation
from app.models.review import Review


def test_review_relationship_and_logic():
    # Create a user and a place
    user = User(first_name="Alice", last_name="Dupont", email="alice@example.com")
    place = Place(
        title="Mountain Cabin",
        description="A cozy cabin in the mountains",
        price=200,
        latitude=46.0,
        longitude=-70.0,
        owner=user
    )

    # Test: Trying to review without reservation should fail
    try:
        Review.create_review(user, place, "Great stay!", 5)
        assert False, "Review should not be allowed without a reservation"
    except ValueError as e:
        assert str(e) == "User must have a reservation for this place to leave a review"

    # Create a reservation
    reservation = Reservation(user, place, "2025-08-01 to 2025-08-05")

    # Test: Creating a review should now succeed
    review = Review.create_review(user, place, "Amazing place!", 5)
    assert review in Review._reviews, "Review should be in the global review list"
    assert review in user.reviews, "Review should be in the user's review list"
    assert review in place.reviews, "Review should be in the place's review list"
    assert review.is_valid_rating(), "Rating should be considered valid"
    assert review in Review.list_by_user(user.id), "Review should be found by user ID"
    assert review in Review.list_by_place(place.id), "Review should be found by place ID"

    print("All Review relationship and logic tests passed.")


if __name__ == "__main__":
    test_review_relationship_and_logic()

