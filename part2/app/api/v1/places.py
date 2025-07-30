from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade

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
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities IDs")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        data = api.payload

        required_fields = ['title', 'description', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in data:
                return {'message': f"Missing field: {field}"}, 400
            owner = facade.get_user(data['owner_id'])
            if owner is None:
                return {'message': "Owner not found"}, 400

            try:
                new_place = facade.create_place(
                        title=data['title'],
                        description=data['description'],
                        price=data['price'],
                        latitude=data['latitude'],
                        longitude=data['longitude'],
                        owner=owner
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
        place_data['amenities'] = [{'id': a.id, 'name': a.name} for a in place.amenities]
        return place_data, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = request.json
        try:
            updated = facade.update_place(place_id, data)
            if not updated:
                return {'message': 'Place not found'}, 404
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 400

