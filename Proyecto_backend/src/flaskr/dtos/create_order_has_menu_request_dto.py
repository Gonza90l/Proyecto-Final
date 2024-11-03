from flaskr.dtos.base_dto import BaseDTO

class CreateOrderHasMenuRequestDTO(BaseDTO):
    def get_required_fields(self):
        return {
            'menu_id': int,
            'quantity': int
        }

    def get_field_constraints(self):
        return {
            'quantity': {'min_value': 1}
        }