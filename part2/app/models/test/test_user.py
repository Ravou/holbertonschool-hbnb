from app.models.user import User

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    print("User creation test passed!")

def test_user_admin_flag():
    admin = User(first_name="Admin", last_name="User", email="admin@example.com", is_admin=True)
    assert admin.is_admin is True
    print("User admin flag test passed!")

