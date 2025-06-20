import unittest
from app.models.user import User

class DummyPlace:
    def __init__(self, id):
        self.id = id

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            password="StrongPass1",
            is_admin=False
        )

    def test_user_creation(self):
        self.assertEqual(self.user.first_name, "Alice")
        self.assertEqual(self.user.last_name, "Smith")
        self.assertEqual(self.user.email, "alice.smith@example.com")
        print(self.user.is_admin)
        self.assertFalse(self.user.is_admin)
        self.assertIsInstance(self.user.reservation_ids, list)

    def test_is_valid_email(self):
        self.assertTrue(User.is_valid_email("test@example.com"))
        self.assertFalse(User.is_valid_email("invalid-email"))

    def test_is_strong_password(self):
        self.assertTrue(User.is_strong_password("Password1"))
        self.assertFalse(User.is_strong_password("weak"))

    def test_authenticate(self):
        self.assertTrue(self.user.authenticate("StrongPass1"))
        self.assertFalse(self.user.authenticate("WrongPass"))

    def test_has_reserved(self):
        place = DummyPlace(id="abc123")
        self.user.reservation_ids.append("abc123")
        self.assertTrue(self.user.has_reserved(place))
        other_place = DummyPlace(id="def456")
        self.assertFalse(self.user.has_reserved(other_place))

if __name__ == '__main__':
    unittest.main()


