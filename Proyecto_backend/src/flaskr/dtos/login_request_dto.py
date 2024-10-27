#login_rquest.py
from flaskr.dtos.base_dto import BaseDTO

class LoginRequestDTO(BaseDTO):
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def validate(self):
        errors = []
        if not self.email:
            errors.append("Email is required")
        if not self.password:
            errors.append("Password is required")
        return errors