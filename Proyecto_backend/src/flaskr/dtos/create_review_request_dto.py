from flaskr.dtos.base_dto import BaseDTO

class CreateReviewRequestDTO(BaseDTO):
    def get_required_fields(self):
        return {
            'order_id': int,
            'id': int,
            'rating': int,
            'review': str
        }

    def get_field_constraints(self):
        return {
            'order_id': {'min_value': 1},
            'id': {'min_value': 1},
            'rating': {'min_value': 1, 'max_value': 5},
            'review': {'max_length': 255}
        }