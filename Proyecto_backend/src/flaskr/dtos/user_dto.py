# dtos/user_dto.py
from flaskr.dtos.base_dto import BaseDTO

class UserDTO(BaseDTO):
    def __init__(self, id=None, name=None, lastname=None, email=None, role=None):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.email = email
        self.role = role

    def get_required_fields(self):
        return {
            'id': int,
            'name': str,
            'lastname': str,
            'email': str,
            'role': str
        }

    def get_field_constraints(self):
        return {
                
        }
