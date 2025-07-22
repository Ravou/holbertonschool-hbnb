from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from app import bcrypt

api = Namespace('places', description='Place operations')

# Models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Place model for input validation and documentation
place_input_model = api.model('PlaceIn', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'address': fields.String(required=True, description='Street address of the place'),
    'city': fields.String(required=True, description='City of the place'),
    'state': fields.String(required=True, description='State of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities IDs")
})

place_output_model = api.model('PlaceOutModel', {
    'latitude': fields.Float(description='Auto-generated latitude'),
    'longitude': fields.Float(description='Auto-generated longitude'),
})

geocode_model = api.model('GeocodeInput', {
    'address': fields.String(required=True, description='Street address'),
    'city': fields.String(required=False, description='City'),
    'state': fields.String(required=False, description='State')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc(security='Bearer Auth')
    @api.expect(place_model)
    @api.marshal_with(place_output_model, code=201)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        data = api.payload
        current_user_id = get_jwt_identity()

        required_fields = ['title', 'description', 'price', 'address', 'city', 'state', 'amenities']
        for field in required_fields:
            if field not in data:
                return {'message': f"Missing field: {field}"}, 400

        owner = facade.get_user(current_user_id)
        if owner is None:
            return {'message': "Owner not found"}, 400

        try:
            new_place = facade.create_place(
                title=data['title'],
                address=data['address'],
                city=data['city'],
                state=data['state'],
                description=data['description'],
                price=data['price'],
                owner=owner,
                amenities=data['amenities']
            )
            return new_place, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    @api.marshal_with(place_list_model, as_list=True)
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        # Return minimal info for list
        result = [{
            'id': place.id,
            'title': place.title,
            'address': place.adress,
            'city': place.city,
            'state': place.city,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places]
        return result, 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        # Compose response including owner and amenities
        place_data = place.to_dict()
        place_data['owner'] = {
            'id': place.owner.id,
            'first_name': place.owner.first_name,
            'last_name': place.owner.last_name,
            'email': place.owner.email
        }
        place_data['amenities'] = []
        for amenity_id in place.amenities:
            amenity_obj = facade.get_amenity(amenity_id)
            if amenity_obj:
                place_data['amenities'].append({'id': amenity_obj.id, 'name': amenity_obj.name})
        return place_data, 200


    @api.doc(security='Bearer Auth')
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorizes action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        data = request.json
        current_user_id = get_jwt_identity()

        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        if place.owner.id != current_user_id:
            return {'message': 'Unauthorized action'}, 403

        allowed_fields = ['title', 'description', 'price', 'address', 'city', 'state', 'amenities']
        filtered_data = {k: v for k, v in data.items() if k in allowed_fields}

        if any(field in filtered_data for field in ['address', 'city', 'state']):
            full_address = f"{filtered_data.get('address', place.address)}",\
                           f"{filtered_data.get('city', place.city)}," \
                           f"{filtered_data.get('state', place.state)}"

        coords = facade.place_repo.geocode_address(full_address)
        if not coords:
            return {'message': 'Invalid address provided'}, 400
        filtered_data['latitude'] = coords['latitude']
        filtered_data['longitude'] = coords['longitude']

        try:
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'message': 'Place not found'}, 404

            return {'title': updated_place.title}, 200
        
        except ValueError as e:
            return {'message': str(e)}, 400

@api.route('/geocode')
class GeocodeAddress(Resource):
    @api.expect(geocode_model)
    @api.response(200, 'Coordinates retrieved successfully')
    @api.response(400, 'Invalid or missing address')
    @jwt_required()
    def post(self):
        """Get latitude and longitude from an address"""
        data = request.json
        address = data.get('address')

        if not address:
            return {'message': 'Address is required'}, 400

        place_repo = PlaceRepository()
        coords = place_repo.geocode_address(address)

        
        if coords:
            return coords, 200
        else:
            return {'message': 'Could not geocode address'}, 400

