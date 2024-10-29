from flaskr.dtos.base_dto import BaseDTO

class CreateMenuRequestDTO(BaseDTO):

    def get_required_fields(self):
        return {
            'name': str,
            'description': str,
            'price': float,
            'image': str,
            'category_id': str
        }

    def get_field_constraints(self):
        return {
            'name': {
                'min_length': 3,
                'max_length': 50
            },
            'description': {
                'min_length': 3,
                'max_length': 255
            },
            'price': {
                'min_value': 0.01,
                'max_value': 10000.00
            },
            'image': {
                'min_length': 0,
                'max_length': 255
            },
            'category_id': {
                'min_length': 1,
                'max_length': 10
            }
        }