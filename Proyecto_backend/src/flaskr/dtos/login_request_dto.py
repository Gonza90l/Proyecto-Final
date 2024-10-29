from flaskr.dtos.base_dto import BaseDTO

class LoginRequestDTO(BaseDTO):
    def get_required_fields(self):
        return {
            'email': str,
            'password': str
        }

    def get_field_constraints(self):
        return {
             'password': {
                'min_length': 6,
                'max_length': 50,
                'must_contain_special': True
            },
            'email': {
                'email': True
            },
        }