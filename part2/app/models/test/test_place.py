from app.models.place import Place
from app.models.user import User
from app.models.review import Review

def test_place_creation_and_review():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)
    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    assert place.reviews[0].rating == 5
    assert place.reviews[0].user == owner
    print("Place creation and review relationship test passed!")

def test_place_multiple_reviews():
    owner = User(first_name="Bob", last_name="Marley", email="bob@example.com")
    place = Place(title="Sunny Loft", description="Bright and spacious", price=150, latitude=48.8566, longitude=2.3522, owner=owner)
    review1 = Review(text="Loved it!", rating=5, place=place, user=owner)
    review2 = Review(text="Very clean.", rating=4, place=place, user=owner)
    place.add_review(review1)
    place.add_review(review2)
    assert len(place.reviews) == 2
    assert place.reviews[1].text == "Very clean."
    print("Place multiple reviews test passed!")
