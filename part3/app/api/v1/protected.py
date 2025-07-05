from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

# Namespace sans préfixe interne, car on veut que l’URL finale soit /api/v1/protected
protected_ns = Namespace(
    'protected',
    description='Zone protégée',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    security='Bearer Auth'
)

@protected_ns.route('')
class ProtectedResource(Resource):
    @jwt_required()
    @protected_ns.doc(security='Bearer Auth')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user["id"]}, admin: {current_user["is_admin"]}'}, 200

