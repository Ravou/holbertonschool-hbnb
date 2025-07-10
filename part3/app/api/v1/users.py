from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from flask import request
from config import Config
from flask_jwt_extended import jwt_required, get_jwt_identity
import jwt

SECRET_KEY = Config.SECRET_KEY

# Swagger Authorizations config
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Add "Bearer <your token>"'
    }
}

api = Namespace('users', description='User operations', authorizations=authorizations, security='Bearer Auth')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Define the user pour the update
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(
                user_data['first_name'], 
                user_data['last_name'], 
                user_data['email'],
                user_data['password']
        )

        return {
                'id': new_user.id, 
                'first_name': new_user.first_name, 
                'last_name': new_user.last_name, 
                'email': new_user.email
        }, 201

    @api.response(200, 'Users retrieved successfully')
    @api.response(500, 'Internal server error')
    def get(self):
        """Get list of all users"""
        try:
            users = facade.list_users()

            if not users:
                return [], 200

            result = [
                {
                    'id': u.id,
                    'first_name': u.first_name,
                    'last_name': u.last_name,
                    'email': u.email
                } for u in users
            ]
            return result, 200

        except Exception as e:
            return {'error': f'Internal server error: {str(e)}'}, 500


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

@api.route('/<string:user_id>')
class UserUpdate(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Email or password cannot be update here')
    @api.response(403, 'Unauthorized access')
    @api.response(401, 'Invalid or missing token')
    @api.response(404, 'User not found')
    def put(self, user_id):
       """Update a user's information (only first name and last name allowed"""
       current_user_id = get_jwt_identity()

       if str(current_user_id) != str(user_id):
           return {"error": "Unauthorized access"}, 403

       update_data = api.payload

       if 'email' in update_data or 'password' in update_data:
           return {"error": "Email or password cannot be updated here"}, 400

       allowed_fields = ['first_name', 'last_name']
       filtered_data = {k: v for k, v in update_data.items() if k in allowed_fields}

       if not filtered_data:
           return {"error": "No valid field to update"}, 400

       user = facade.update_user(user_id, filtered_data)
       if not user:
           return {"error": "User not found"}, 404
       return {"message": "User updated successfully"}, 200
