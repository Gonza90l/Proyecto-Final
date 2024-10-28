#login_response_dto.py
from flaskr.dtos.base_dto import BaseDTO

class LoginResponseDTO(BaseDTO):
    def __init__(self, token = None):
        self.token = token

    def to_json(self):
        return {
            'token': self.token
        }

        