from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('reservations', description='Reservation operations')

# Define the reservation model for input validation and documentation
reservation_model = api.model('Reservation', {
    