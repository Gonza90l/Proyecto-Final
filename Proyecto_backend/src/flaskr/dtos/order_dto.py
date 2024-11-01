
# dtos/user_dto.py
from flaskr.dtos.base_dto import BaseDTO

class OrderDTO(BaseDTO):
    def __init__(self, id=None, user_id=None, created_at=None, status=None, total=None):
        self.id = id
        self.user_id = user_id
        self.created_at = created_at
        self.status = status
        self.total = total

    def get_required_fields(self):
        return {
            'id': int,
            'user_id': int,
            'created_at': str,
            'status': str,
            'total': float
        }

    def get_field_constraints(self):
        return {}

    