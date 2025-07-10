from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from flask import request
from config import Config
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from jwt


api = Namespace('admin', description='Admin operations')

user_input = api.model('UserInput', {
    'email': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean
})

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.response(201, 'User successfully created', user_model)
    @api.response(400, 'Email already registered or missing required fields')
    @api.reponse(403, 'Admin privileges required')
    @api.response(500, 'Internal server error')
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Logic to create a new user
        new_user = facade.create_user(
                user_data['first_name'],
                user_data['last_name'],
                email,
                user_data['password'],
                user_data.get('is_admin', False)
        )

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
        }, 201

@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    @api.response(200, 'User updated successfully', user_model)
    @api.response(400, 'Email is already in use')
    @api.response(403, 'Admin, privileges required')
    @api.response(404, 'User not found') 
    def put(self, user_id):
        current_user = get_jwt_identity()

        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            # Check if email is already in use
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        # Logic to update user details, including email and password
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.hash_password(data['password'])
        if 'is_admin' in data:
            user.is_admin = data['is_admin']

        return {'message': 'User updated successfully'}, 200


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity created successfully')
    @api.response(400, 'Amenity already exists')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    def post(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        name = data.get('name')

        # (Optionnel) Vérifie si l'amenity existe déjà
        existing = facade.get_amenity_by_name(name)
        if existing:
            return {'error': 'Amenity already exists'}, 400

        # Création
        new_amenity = facade.create_amenity(name=name)

        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.get_amenity_by_id(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        data = api.payload
        new_name = data.get('name')

        
        existing = facade.get_amenity_by_name(new_name)
        if existing and existing.id != amenity.id:
            return {'error': 'Another amenity with this name already exists'}, 400

        
        amenity.name = new_name
        facade.save_amenity(amenity)

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.response(201, 'Amenity created successfully')
    @api.response(400, 'Missing or invalid amenity data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        name = data.get('name')

        if not name:
            return {'error': 'Amenity name is required'}, 400

        
        if facade.get_amenity_by_name(name):
            return {'error': 'Amenity already exists'}, 400

        new_amenity = facade.create_amenity(name)

        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services.facade import facade

api = Namespace('admin', description='Admin operations')

# Define model for response (optional, for Swagger)
amenity_model = api.model('Amenity', {
    'id': fields.String,
    'name': fields.String,
})

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    @api.response(200, 'Amenity updated successfully', amenity_model)
    @api.response(400, 'Invalid input or missing data')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        name = data.get('name')

        if not name:
            return {'error': 'Amenity name is required'}, 400

        amenity = facade.get_amenity_by_id(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        # Update logic
        amenity.name = name
        facade.save(amenity)

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

