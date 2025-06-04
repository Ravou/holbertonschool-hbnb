```mermaid
classDiagram
direction TB
    class BaseModel {
	    - id : UUID
	    - created_at : DateTime
	    - updated_at : DateTime
	    #save() void
	    +to_dict() dict
		+delete()
    }

    class Review {
	    + text : str
	    + rating : float
	    + add_review() : None
	    + update(): None
	    + list_by_place(place_id) : List[Review]
		+ reserve_place(place)
    }

    class Amenity {
	    + name : str
	    + description : str
	    + list_all() List[Amenity]
    }

    class Place {
	    + name : str
		+ title : str
	    + description : str
	    + price : float
	    - latitude : float
	    - longitude : float
	    - owner: str
	    + Amenity: List[Amenity]
	    + add_place() None
	    + list_all() List[Place]
		+ get_all_reservation() List
    }

    class User {
	    + email : str
	    - password : str
		+ owner : str
	    + first_name : str
	    + last_name : str
	    + register() None
	    + authenticate() bool
		}

	<<abstract>> BaseModel

    BaseModel <|-- User : inheritance
    BaseModel <|--  Place : inheritance
    BaseModel <|--  Review : inheritance
    BaseModel <|--  Amenity : inheritance
    
	Review "*" --> "1" Place : about
	Review "*" --> "1" User : by

    Place "1" --> "*" Review : receives
    Place "1" --> "*" Amenity : offers
	

    Amenity "*" --> "1" Place : available_in
	
    User "1" <-- "0..*" Place : réservation
    User "1" --> "*" Review : writes

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
