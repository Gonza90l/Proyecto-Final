
# dtos/user_dto.py
from flaskr.dtos.base_dto import BaseDTO

class OrderDTO(BaseDTO):
    def __init__(self, id=None, user_id=None, created_at=None, status=None, total=None, order_items=None):
        self.id = id
        self.user_id = user_id
        self.created_at = created_at
        self.status = status
        self.total = total
        self.order_items = [] # por la relacion con order_has_menu se crea una lista de objetos de order_has_menu

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

    