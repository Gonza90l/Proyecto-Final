#update_user_dto.py
from flaskr.dtos.base_dto import BaseDTO

class UpdateUserDTO(BaseDTO):
    def __init__(self, name=None, lastname=None, email=None, role=None):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.role = role

    def get_required_fields(self):
        return {
            'name': str,
            'lastname': str,
            'email': str,
            'role': str
        }

    def get_field_constraints(self):
        return {
            'role': {
                'min': 1,
                'max': 50
            }
        }