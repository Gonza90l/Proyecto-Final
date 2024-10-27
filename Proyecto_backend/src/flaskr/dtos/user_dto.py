# dtos/user_dto.py
class UserDTO:
    def __init__(self, id=None, name=None, lastname=None, email=None, role=None):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.email = email
        self.role = role
