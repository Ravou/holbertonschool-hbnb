import pytest
from .user_service import UserService
from app.models.user import User

# python

@pytest.fixture(autouse=True)
def patch_user_methods(monkeypatch):
    monkeypatch.setattr(User, "is_valid_email", staticmethod(lambda email: "@" in email and "." in email))
    monkeypatch.setattr(User, "is_strong_password", staticmethod(lambda pwd: len(pwd) >= 8 and any(c.isupper() for c in pwd) and any(c.isdigit() for c in pwd)))

def test_register_user_success():
    service = UserService()
    result = service.register_user(
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@example.com",
        password="StrongPass1",
        is_admin=False
    )
    assert result is True

def test_register_user_empty_first_name():
    service = UserService()
    result = service.register_user(
        first_name="",
        last_name="Smith",
        email="alice.smith@example.com",
        password="StrongPass1",
        is_admin=False
    )
    assert result is False

def test_register_user_empty_last_name():
    service = UserService()
    result = service.register_user(
        first_name="Alice",
        last_name="",
        email="alice.smith@example.com",
        password="StrongPass1",
        is_admin=False
    )
    assert result is False

def test_register_user_invalid_email(monkeypatch):
    service = UserService()
    monkeypatch.setattr(User, "is_valid_email", staticmethod(lambda email: False))
    result = service.register_user(
        first_name="Alice",
        last_name="Smith",
        email="bademail",
        password="StrongPass1",
        is_admin=False
    )
    assert result is False

def test_register_user_weak_password(monkeypatch):
    service = UserService()
    monkeypatch.setattr(User, "is_strong_password", staticmethod(lambda pwd: False))
    result = service.register_user(
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@example.com",
        password="weak",
        is_admin=False
    )
    assert result is False