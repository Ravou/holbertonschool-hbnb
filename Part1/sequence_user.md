```mermaid
sequenceDiagram
    %% Layers:
    %% Presentation: User, API
    %% Business Logic: Facade, BusinessLogic, Repository
    %% Persistence: Persistence

    actor User
    participant API as API (Presentation Layer)
    participant Facade as Facade pattern
    participant BusinessLogic as Business Logic
    participant Repository as Repository (Interface)
    participant Persistence as Persistence Layer

    User ->> API: POST /users with data
    API ->> Facade: create_user(data)

    alt Missing required fields
        Facade -->> API: 400 Bad Request - Missing fields
        API -->> User: Please fill all required fields
    else Invalid email format
        Facade -->> API: 400 Bad Request - Invalid email
        API -->> User: Invalid email address
    else Password too short
        Facade -->> API: 400 Bad Request - Weak password
        API -->> User: Password must be at least 8 characters
    else Email already exists
        Facade -->> API: 409 Conflict - Email already registered
        API -->> User: Email already in use
    else Valid data
        Facade ->> BusinessLogic: create_user_instance(data)
        BusinessLogic ->> Repository: save(user)
        Repository ->> Persistence: insert_user(user)
        Persistence -->> Repository: OK
        Repository -->> BusinessLogic: User saved
        BusinessLogic -->> Facade: return user
        Facade -->> API: 201 Created + user object
        API -->> User: Success + user_id
    end
```mermaid
