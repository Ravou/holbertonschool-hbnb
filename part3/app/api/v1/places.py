from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

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
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities IDs")
})

@api.route('/')
class PlaceList(Resource):
    @api.doc(security='Bearer Auth')
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        data = api.payload
        current_user_id = get_jwt_identity()

        required_fields = ['title', 'description', 'price', 'latitude', 'longitude', 'amenities']
        for field in required_fields:
            if field not in data:
                return {'message': f"Missing field: {field}"}, 400

        owner = facade.get_user(current_user_id)
        if owner is None:
            return {'message': "Owner not found"}, 400

        try:
            new_place = facade.create_place(
                    title=data['title'],
                    description=data['description'],
                    price=data['price'],
                    latitude=data['latitude'],
                    longitude=data['longitude'],
                    owner=owner,
                    amenities=data['amenities']
            )
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        # Return minimal info for list
        result = [{
            'id': place.id,
            'title': place.title,
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

        try:
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'message': 'Place not found'}, 404

            return {'title': updated_place.title}, 200
        
        except ValueError as e:
            return {'message': str(e)}, 400

