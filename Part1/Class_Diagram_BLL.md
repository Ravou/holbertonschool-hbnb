```mermaid
classDiagram
direction TB

    %% 1. BaseModel
    class BaseModel {
	    - id : UUID
	    - created_at : DateTime
	    - updated_at : DateTime
	    #save() void
	    +to_dict() dict
    }
    
    %% 2. User
    class User {

        + email : str
        - password : str
        + owner : str
        + first_name : str
        + last_name : str
        + is_admin() bool
        + register() bool
        + authenticate() bool
        + add_place(name: str, price: float, ...) bool
        + has_reserved(place)  bool
        + add_review(text: str, rating: float) bool
        + add_amenity(name: str, description: str)  bool
    }
    
    %% 3. Place
    class Place {
        + name : str
        + title : str
        + description : str
        + price : float
        - latitude : float
        - longitude : float
        + owner: str
        + amenities: List[Amenity]
        + list_all() List[Place]
        - get_all_reservation() List
        + get_by_criteria(criteria: dict) List[Place]
    }
    
    %% 4. Amenity
    class Amenity {
	    + name : str
	    + description : str
	    + list_all() List[Amenity]
    }
    
    %% 5. Review
    class Review {
        + text : str
        + rating : float
        + list_by_place(place_id) List[Review]
    }

	<<abstract>> BaseModel

    BaseModel <|-- User : inheritence
    BaseModel <|--  Place : inheritence
    BaseModel <|--  Review : inheritence
    BaseModel <|--  Amenity : inheritence
    
    User "1" --> "0..*" Place : manage
    User "1" --> "0..*" Review : writes

    Place "0..*" --> "0..*" Amenity : offers
    
	Review "0..*" --> "1" Place : about
	

	style BaseModel :,stroke-width:1px,stroke-dasharray:none,stroke:#FF5978,fill:#FFDFE5,color:#8E2236
	style Review :,stroke-width:1px,stroke-dasharray:none,stroke:#999999,fill:#EEEEEE,color:#000000
	style Amenity :,stroke-width:1px,stroke-dasharray:none,stroke:#999999,fill:#EEEEEE,color:#000000
	style Place :,stroke-width:1px,stroke-dasharray:none,stroke:#999999,fill:#EEEEEE,color:#000000
	style User :,stroke-width:1px,stroke-dasharray:none,stroke:#999999,fill:#EEEEEE,color:#000000

	class BaseModel:::Rose
	class Review:::Ash
	class Amenity:::Ash
	class Place:::Ash
	class User:::Ash
```
