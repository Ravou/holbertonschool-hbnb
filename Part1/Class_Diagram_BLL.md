```mermaid
classDiagram
direction TB
    class BaseModel {
	    - id : UUID
	    - created_at : DateTime
	    - updated_at : DateTime
	    #save() void
	    +to_dict() dict
	    +__str__() str
	    +__init__() none
    }

    class Review {
	    + user_id : UUID
	    + place_id : UUID
	    + text : str
	    + rating : float
	    + add_review() : None
	    + update(): None
	    + delete() : None
	    + list_by_place(place_id) : List[Review]
		+ reserve_place(place)
    }

    class Amenity {
		- id : str
	    + name : str
	    + description : str
	    + __init__() None
	    + create() None
	    + update() None
	    + delete() None
	    + list_all() List[Amenity]
    }

    class Place {
	    + name : str
		+ title : str
	    + description : str
	    + price : float
	    - latitude : float
	    - longitude : float
	    - owner_id : UUID
	    + Amenity: List[Amenity]
	    + address : str
	    + __init__() None
	    + add_place() None
	    + update() None
	    + delete() None
	    + list_all() List[Place]
		+ get_all_reservation() List
		+ getter_address() str
		+ setter_address() None
    }

    class User {
	    + email : str
	    - password : str
	    + first_name : str
	    + last_name : str
	    + __init__() None
	    + register() None
	    + update_profile() None
	    + delete_user() None
	    + authenticate() bool
		+ reserve_place(place) None
		}

	<<abstract>> BaseModel

    BaseModel --|> User : inheritence
    BaseModel --|> Place : inheritence
    BaseModel --|> Review : inheritence
    BaseModel --|> Amenity : inheritence
    Review --> User
    Review --> Place
    Place "1" --> "*" Review : receives
    Place "*" --> "*" Amenity : offers
    User "1" --> "*" Place : creates
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
```mermaid
