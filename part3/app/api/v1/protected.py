from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt

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
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        return {'message': f'Hello, user {current_user["id"]}, admin: {is_admin}'}, 200

