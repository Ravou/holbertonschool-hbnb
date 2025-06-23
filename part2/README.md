# User Model - Python OOP

This module defines a `User` class for managing users in an object-oriented system.  
It includes user attributes, relations to other models, and utility methods for management and retrieval.

## 🧩 Features

- Inherits from a base model (`BaseModel`)
- Stores user information: first name, last name, email, admin status
- Tracks associated places, reviews, and reservations
- Supports searching users by email or ID
- Includes an internal registry of all created users

## 🔧 Class: `User`

### Attributes

- `first_name` (str): User's first name
- `last_name` (str): User's last name
- `email` (str): User's email
- `is_admin` (bool): Admin status (default `False`)
- `reservations` (List[Reservation]): List of reservations made by the user
- `places` (List[Place]): List of places owned by the user
- `reviews` (List[Review]): Reviews written by the user

### Class Attributes

- `_users`: List of all instantiated users
- `allowed_update_fields`: Fields that can be updated dynamically

### Methods

- `add_place(place)`: Adds a place to the user's list and sets ownership
- `add_review(review)`: Adds a review to the user's list
- `add_reservation(reservation)`: Adds a reservation to the user's list
- `get_by_email(email)`: Returns a user instance matching the email
- `get_by_id(id)`: Returns a user instance matching the ID
- `list_all()`: Returns all created users
- `is_admin` (property): Getter and setter for admin status
- `__repr__()`: Returns a readable string representation of the user

## 📦 Dependencies

- Python 3.10+
- `BaseModel` class from `app.models.base_model`

## ✅ Example

```python
from app.models.user import User

u1 = User("Alice", "Doe", "alice@example.com")
u2 = User("Bob", "Smith", "bob@example.com", is_admin=True)

print(User.get_by_email("bob@example.com"))  # → User(id='...', email='bob@example.com')
print(u1.is_admin)  # → False
u1.is_admin = True

