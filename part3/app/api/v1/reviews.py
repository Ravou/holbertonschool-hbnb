from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

# Review model for input validation and Swagger docs
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'reservation_id': fields.String(required=True, description='ID of the reservation')
})

@api.route('/')
class ReviewList(Resource):
    @api.doc(security= 'Bearer Auth')
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data or no reservation found')
    @jwt_required()
    def post(self):
        review_data = request.json
        if not review_data:
            raise BadRequest("Missing JSON data")

        try:
            review = facade.create_review(review_data)
        except ValueError as e:
            raise BadRequest(str(e))

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id,
            "reservation_id": review.reservation_id,
            "created_at": review.created_at.isoformat() if hasattr(review, 'created_at') else None,
            "updated_at": review.updated_at.isoformat() if hasattr(review, 'updated_at') else None,
        }, 201
        

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_all_review(review_id)
        if not review:
            raise NotFound('Review not found')
        return review.__dict__, 200

    @api.doc(security= 'Bearer Auth')
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        data = request.json
        if not data: 
            return {'message': 'No data provided'}, 400
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        if review.user_id != current_user_id:
            return {'message': 'Unauthorized access'}, 403

        try:
            updated_review = facade.update_review(review_id, data)
            if not updated_review:
                return {'message': 'Review not found'}, 404

            return {'message': 'Review updated successfully'}, 200
        
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.doc(security= 'Bearer Auth')
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized access')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""

        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            raise NotFound('Review not found')

        if review.user_id != current_user_id:
            return {'message': 'Unauthorized access'}, 403

        deleted = facade.delete_review(review_id)
        if not deleted:
            raise NotFound('Review not found')
        
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.place_repo.get(place_id)
        if not place:
            raise NotFound('Place not found')
        reviews = facade.get_reviews_by_place(place_id)
        return [review.__dict__ for review in reviews], 200
