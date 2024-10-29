from flaskr.dtos.base_dto import BaseDTO

class UpdateCategoryRequestDTO(BaseDTO):

    def get_required_fields(self):
        return {
            'name': str,
            'description': str,
            'photo': str,
        }

    def get_field_constraints(self):
        return {
            'name': {
                'min_length': 3,
                'max_length': 50
            },
            'description': {
                'min_length': 3,
                'max_length': 255
            },
            'photo': {
                'min_length': 0,
                'max_length': 255
            }
        }

