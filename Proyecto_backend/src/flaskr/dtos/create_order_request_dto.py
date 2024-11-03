from flaskr.dtos.base_dto import BaseDTO

class CreateOrderRequestDTO(BaseDTO):
    def get_required_fields(self):
        return {
            'user_id': int,
            'total': float,
            'status': str,
            'order_items': list  # This will be a list of OrderHasMenuDTO
        }

    def get_field_constraints(self):
        return {
            'status': {'min_length': 1, 'max_length': 20},
            'total': {'min_value': 0},
        }