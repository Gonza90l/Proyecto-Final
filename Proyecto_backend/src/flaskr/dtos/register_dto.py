#register_dto.py
from flaskr.dtos.base_dto import BaseDTO

class RegisterDTO(BaseDTO):
    def __init__(self, name=None, lastname=None, email=None, password=None):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password

    def get_required_fields(self):
        return {
            'name': str,
            'lastname': str,
            'email': str,
            'password': str
        }

    def get_field_constraints(self):
        return {
            'password': {
                'min_length': 6,
                'max_length': 50,
                'must_contain_special': True
            }
        }
