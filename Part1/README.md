# HBNB UML Diagrams - Technical Documentation

![HBNB](Part1/diagramme/hbnb.png)

This repository contains the technical documentation and UML diagrams for the **HBNB project** — part of the Holberton School AirBnB clone. It compiles all architectural and design diagrams into a cohesive reference blueprint for the project’s implementation.

---

## Table of Contents

- [Introduction](#introduction)
- [High-Level Package Diagram](#high-level-package-diagram)
- [Class Diagram for Business Logic Layer](#class-diagram-for-business-logic-layer)
- [Sequence Diagrams for API Calls](#sequence-diagrams-for-api-calls)
- [Explanatory Notes](#explanatory-notes)
- [Status](#status)
- [How to Use](#how-to-use)
- [Author](#author)
- [License](#license)

---

## Introduction

This document serves as a **comprehensive technical reference** for the HBNB system — the backend foundation of the Holberton School AirBnB clone project. It consolidates all key UML diagrams into a single, structured blueprint, offering a clear overview of the system’s architecture and internal workflows.

### Purpose

- Provide **visual and written representations** of the system’s layered architecture and object relationships.
- Clarify **design choices** and their underlying rationale, making the codebase easier to understand, maintain, and extend.
- Serve as a **reliable reference** for developers during all phases of the project, including planning, implementation, testing, and review.

---

## High-Level Package Diagram

**Diagram:** `package_diagram.png`

### Description

- **Layered Structure:**
  - **Presentation Layer:** Handles user interaction and routing.
  - **Business Logic Layer:** Contains core application logic.
  - **Data Layer:** Manages storage and persistence.

- **Facade Pattern:** Used to simplify interactions between layers and reduce coupling.

---

## Class Diagram for Business Logic Layer

**Diagram:** `class_diagram_business.png`

### Description

- Main entities:
  - `User`
  - `Place`
  - `Amenity`
  - `Review`

- Relationships:
  - `User` → `Place` : owns (1 → *)
  - `Place` → `Amenity` : offers (* → *)
  - `Place` → `Review` : receives (* → *)
  - `User` → `Review` : writes (1 → *)

- Each class is described with:
  - Attributes (e.g., `name`, `description`, `created_at`, etc.)
  - Responsibilities
  - Relationship roles

### Diagram Legend (Related to Class Diagram)

To interpret the UML class diagrams, here’s a quick legend for the **relationship arrows**:

- `1` → `*` : One-to-Many relationship (e.g., one `User` owns many `Places`)
- `*` → `*` : Many-to-Many relationship (e.g., `Place` offers multiple `Amenities`, and vice versa)
- `1` → `1` : One-to-One relationship
- `0` → `1` : Optional relationship (zero or one)
- `0` → `*` : Optional one-to-many (e.g., an entity may have zero or more related items)
- Solid Arrow: Association (basic relationship)
- Filled Diamond: Composition (strong ownership, e.g., if A is deleted, B is deleted too)
- Empty Diamond: Aggregation (shared ownership)
- Triangle: Inheritance (generalization)

## Sequence Diagram for API CAlls

Below are Mermaid.js-based sequence diagrams representing core API workflows.

User Registration :

``mermaid
sequenceDiagram
    %% Layers:
    %% Presentation: User, API
    %% Business Logic: Facade, BusinessLogic, Repository
    %% Persistence: Persistence

    actor User
    participant API as API (Presentation Layer)
    participant Facade as "Facade pattern"
    participant BusinessLogic as Business Logic
    participant Repository as "Repository (Interface)"
    participant Persistence as Persistence Layer

    User ->> API: POST /users with data
    API ->> Facade: create_user(data)

    alt "Missing required fields"
        Facade -->> API: 400 Bad Request - Missing fields
        API -->> User: Please fill all required fields
    else "Invalid email format"
        Facade -->> API: 400 Bad Request - Invalid email
        API -->> User: Invalid email address
    else "Password too short"
        Facade -->> API: 400 Bad Request - Weak password
        API -->> User: Password must be at least 8 characters
    else "Email already exists"
        Facade -->> API: 409 Conflict - Email already registered
        API -->> User: Email already in use
    else "Valid data"
        Facade ->> BusinessLogic: create_user_instance(data)
        BusinessLogic ->> Repository: save(user)
        Repository ->> Persistence: insert_user(user)
        Persistence -->> Repository: OK
        Repository -->> BusinessLogic: User saved
        BusinessLogic -->> Facade: return user
        Facade -->> API: 201 Created + user object
        API -->> User: Success + user_id
    end

```

Place Creation :

``mermaid
sequenceDiagram
    %% Layers:
    %% Presentation: User, API
    %% Business Logic: Facade, PlaceLogic, PlaceRepository
    %% Persistence: Database

    actor User
    participant API as API (Presentation Layer)
    participant Facade as Facade
    participant PlaceLogic as Business Logic
    participant PlaceRepository as Repository (Interface)
    participant Database as Persistence

    loop For each place
        User ->> API: POST /places with place data
        API ->> Facade: create_place(data)

        alt Missing required fields
            Facade -->> API: 400 - Missing required fields
            API -->> User: Fill all required fields
        else Invalid price or location
            Facade -->> API: 400 - Invalid price/location
            API -->> User: Check your data
        else Invalid amenities
            Facade -->> API: 400 - Invalid amenities
            API -->> User: Provide valid amenities
        else Valid data
            Facade ->> PlaceLogic: validate and build place
            PlaceLogic ->> PlaceRepository: save(place_object)
            PlaceRepository ->> Database: INSERT place_object
            Database -->> PlaceRepository: OK
            PlaceRepository -->> PlaceLogic: Place saved
            PlaceLogic -->> Facade: Return place_id
            Facade -->> API: 201 Created + place info
            API -->> User: Place successfully created
        end
    end
```

Review Submission :

``mermaid
sequenceDiagram
    actor User
    participant API as API (Presentation)
    participant Facade
    participant Logic as Business Logic
    participant Repo as Repository (interface)
    participant DB as Persistence

    User ->> API: POST /reviews with data
    API ->> Facade: create_review(data)

    alt Invalid input (missing or bad rating)
        Facade -->> API: 400 Bad Request
        API -->> User: Review data invalid
    else No reservation
        Facade ->> Logic: validate_reservation(user_id, place_id)
        Logic ->> Repo: check_reservation(user_id, place_id)
        Repo ->> DB: query_reservation()
        DB -->> Repo: No match
        Repo -->> Logic: Forbidden
        Logic -->> Facade: 403 Forbidden
        Facade -->> API: Review not allowed
        API -->> User: Must reserve place first
    else Valid input + reserved
        Facade ->> Logic: create_review_instance(data)
        Logic ->> Repo: save(review)
        Repo ->> DB: insert_review()
        DB -->> Repo: OK
        Repo -->> Logic: Done
        Logic -->> Facade: review object
        Facade -->> API: 201 Created
        API -->> User: Review submitted
    end
```


---

##  Status

-  Diagrams created and reviewed
-  Organized and documented in Markdown
-  Ready to be included in the main AirBnB clone documentation or wiki

---

##  How to Use

1. Clone the repository: https://github.com/Ravou/holbertonschool-hbnb.git

2. Open the diagram files using your prefered UML viewer or any web browser.

3. Use the diagrams for documentation, development guidance, or team onboarding.

##  Author

- Olivia Letchy - @Ravou

##  License

```
This project is licensed under the MIT License. 

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, provided that the original license notice is included in all copies or substantial portions of the Software.

> Copyright (c) 2025 Ravou  
>  
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

