from flask_restx import Namespace, Resource, fields, abort
from flask import request
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=True, description='Description of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        data = api.payload
        new_amenity = facade.create_amenity(data)
        return new_amenity.to_dict(), 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'message': 'Amenity not found'}, 404
        return {
            "id": amenity.id,
            "name": amenity.name
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        data = api.payload
        amenity = facade.update_amenity(amenity_id, data)
        if not amenity:
            return {'message': 'Amenity not found'}, 404
        return {'message': 'Amenity updated successfully'}, 200
