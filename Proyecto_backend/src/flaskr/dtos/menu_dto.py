# dtos/user_dto.py
from flaskr.dtos.base_dto import BaseDTO

class MenuDTO(BaseDTO):
    def __init__(self, id=None, name=None, description=None, price=None, photo=None, category_id=None):
        self.name = name
        self.description = description
        self.price = price
        self.photo = photo
        self.category_id = category_id
        self.id = id


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
                
        }