from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, NotFound

api = Namespace('reservations', description='Reservation operations')

# Define the reservation model for input validation and documentation
reservation_model = api.model('Reservation', {
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'start_date': fields.String(required=True, description='Start date of the reservation (YYYY-MM-DD)'),
    'end_date': fields.String(required=True, description='End date of the reservation (YYYY-MM-DD)'),
    'number_of_guests': fields.Integer(required=True, description='Number of guests')
    })

@api.route('/')
class ReservationList(Resource):
    @api.expect(reservation_model)
    @api.response(201, 'Reservation successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new reservation"""
        data = api.payload
        if not data:
            raise BadRequest("Missing JSON data")

        current_user_id = get_jwt_identity()

        try:
            reservation = facade.create_reservation(
                user_id=current_user_id,
                place_id=data['place_id'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                number_of_guests=data['number_of_guests']
            )
            return {
                "id": reservation.id,
                "user_id": reservation.user_id,
                "place_id": reservation.place_id,
                "start_date": reservation.start_date,
                "end_date": reservation.end_date,
                "number_of_guests": reservation.number_of_guests
            }, 201
        except ValueError as e:
            raise BadRequest(str(e))

    @api.response(200, 'List of reservations retrieved successfully')
    def get(self):
        """List all reservations"""
        reservations = facade.get_all_reservations()
        return [r.to_dict() for r in reservations], 200

@api.route('/<string:reservation_id>')
class ReservationResource(Resource):
    @api.response(200, 'Reservation details retrieved successfully')
    @api.response(404, 'Reservation not found')
    def get(self, reservation_id):
        """Get reservation by ID"""
        reservation = facade.get_reservation(reservation_id)
        if not reservation:
            raise NotFound('Reservation not found')
        return reservation.to_dict(), 200

    @api.expect(reservation_model)
    @api.response(200, 'Reservation updated successfully')
    @api.response(404, 'Reservation not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorization access')
    @jwt_required()
    def put(self, reservation_id):
        """Update a reservation"""
        data = api.payload
        if not data:
            raise BadRequest("Missing JSON data")
        
        reservation = facade.get_reservation(reservation_id)
        if not reservation:
            raise NotFound('Reservation not found')

        current_user_id = get_jwt_identity()
        if reservation.user_id != current_user_id:
            return {"message": "Unauthorization access"},403

        try:
            updated_reservation = facade.update_reservation(reservation_id, data)
            return {'message': 'Reservation updated successfully'}, 200
        except ValueError as e:
            raise BadRequest(str(e))
