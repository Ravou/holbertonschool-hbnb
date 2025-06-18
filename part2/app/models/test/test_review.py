from app.models.review import Review
from app.models.user import User
from app.models.place import Place

def test_review_creation():
    user = User(first_name="Test", last_name="User", email="test.user@example.com")
    place = Place(title="Test Place", description="Just a test", price=50, latitude=0.0, longitude=0.0, owner=user)
    review = Review(text="Super expérience", rating=5, place=place, user=user)
    assert review.text == "Super expérience"
    assert review.rating == 5
    assert review.place == place
    assert review.user == user
    print("Review creation test passed!")

def test_review_rating_bounds():
    user = User(first_name="Test", last_name="User", email="test.user@example.com")
    place = Place(title="Test Place", description="Just a test", price=50, latitude=0.0, longitude=0.0, owner=user)
    review = Review(text="Pas terrible", rating=1, place=place, user=user)
    assert 1 <= review.rating <= 5
    print("Review rating bounds test passed!")
