from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services.facade import facade
import jwt

SECRET_KEY = Config.SECRET_KEY

api = Namespace(
    'admin',
    description='Admin operations',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Add "Bearer <your token>"'
        }
    },
    security='Bearer Auth'
)

# --- Swagger models ---

user_model = api.model('User', {
    'id': fields.String(readonly=True, description='User identifier'),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'is_admin': fields.Boolean(description='Admin flag')
})

user_input = api.model('UserInput', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean(default=False)
})

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity identifier'),
    'name': fields.String(required=True, description='Name of the amenity')
})

# --- Admin: Create User ---
@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_input, validate=True)
    @api.response(201, 'User successfully created', user_model)
    @api.response(400, 'Email already registered or missing required fields')
    @api.response(403, 'Admin privileges required')
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.get_json()
        email = user_data.get('email')

        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(
            data['first_name'],
            data['last_name'],
            data['email'],
            data['password'],
            data.get('is_admin', False)
        )
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
        }, 201

# --- Admin: Modify User ---
@api.route('/users/<string:user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    @api.expect(user_input, validate=True)
    @api.response(200, 'User updated successfully', user_model)
    @api.response(400, 'Email is already in use or invalid data')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    def put(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        email = data.get('email')

        if email:
            existing = facade.get_user_by_email(email)
            if existing and existing.id != user_id:
                return {'error': 'Email is already in use'}, 400

        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.hash_password(data['password'])
        if 'is_admin' in data:
            user.is_admin = data['is_admin']

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

# --- Admin: Create Amenity ---
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.doc(security='Bearer Auth')
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity created successfully', amenity_model)
    @api.response(400, 'Amenity already exists or missing name')
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

        new_amenity = facade.create_amenity({'name': name})
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

# --- Admin: Modify Amenity ---
@api.route('/amenities/<string:amenity_id>')
class AdminAmenityModify(Resource):
    @api.doc(security='Bearer Auth')
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully', amenity_model)
    @api.response(400, 'Another amenity with this name already exists or missing name')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        name = data.get('name')
        if not name:
            return {'error': 'Amenity name is required'}, 400

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        existing = facade.get_amenity_by_name(name)
        if existing and existing.id != amenity_id:
            return {'error': 'Another amenity with this name already exists'}, 400

        amenity.name = name
        facade.update_amenity(amenity_id, {'name': name})
        return {'id': amenity.id, 'name': amenity.name}, 200

