# dtos/user_dto.py
from flaskr.dtos.base_dto import BaseDTO

class UpdateMenuRequestDTO(BaseDTO):
    def __init__(self, id=None, name=None, description=None, price=None, photo=None, category_id=None):
        self.name = name
        self.description = description
        self.price = price
        self.photo = photo
        self.category_id = category_id


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
            'name': {'min_length': 3, 'max_length': 50},
            'description': {'min_length': 10, 'max_length': 200},
            'price': {'min_value': 0.01},
            'photo': {'max_length': 255},
        }