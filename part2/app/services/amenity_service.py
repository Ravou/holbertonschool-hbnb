from app.models.amenity import Amenity

class AmenityService:
    @staticmethod
    def get_by_id(id):
        for amenity in Amenity.list_all():
            if amenity.id == id:
                return amenity
        return None
