from flaskr.dtos.base_dto import BaseDTO

class CreateMenuRequestDTO(BaseDTO):

    def get_required_fields(self):
        return {
            'name': str,
            'description': str,
            'price': float,
            'photo': str,
            'category_id': int
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
            'photo': {
                'min_length': 0,
                'max_length': 255
            }
        }