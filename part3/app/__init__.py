from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.reservations import api as reservations_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import protected_ns
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)

    authorizations = {
            'Bearer Auth': {
                'type': 'apikey', 
                'in': 'header', 
                'name': 'Authorization', 
                'description': "Type 'Bearer <JWT token>' to authorize."
                } 
            }
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/', authorizations=authorizations, security='Bearer Auth')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(reservations_ns, path='/api/v1/reservations')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected')

    return app
