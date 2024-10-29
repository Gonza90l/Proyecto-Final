from flaskr.dtos.base_dto import BaseDTO

class LoginRequestDTO(BaseDTO):
    def get_required_fields(self):
        return {
            'email': str,
            'password': str
        }

    def get_field_constraints(self):
        return {
            'email': {
                'email': True
            },
        }