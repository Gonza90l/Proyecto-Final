from flaskr.dtos.base_dto import BaseDTO

class ReviewDTO(BaseDTO):
    def __init__(self, comment=None, created_at=None, menu_id=None, rating=None, user_id=None):
        self.comment = comment
        self.created_at = created_at
        self.menu_id = menu_id
        self.rating = rating
        self.user_id = user_id

    def get_required_fields(self):
        return {
            'comment': str,
            'created_at': str,
            'menu_id': int,
            'rating': int,
            'user_id': int
        }

    def get_field_constraints(self):
        return {
            'rating': {'min': 1, 'max': 5}
        }

class ReviewSummaryDTO(BaseDTO):
    def __init__(self, average=None, count=None, reviews=None):
        self.average = average
        self.count = count
        self.reviews = [ReviewDTO(**review) for review in reviews] if reviews else []

    def get_required_fields(self):
        return {
            'average': float,
            'count': int,
            'reviews': list
        }

    def get_field_constraints(self):
        return {}