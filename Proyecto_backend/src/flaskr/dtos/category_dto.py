from flaskr.dtos.base_dto import BaseDTO

class CategoryDTO(BaseDTO):
    def __init__(self, name=None, description=None, photo=None, id=None):
        self.name = name
        self.description = description
        self.photo = photo
        self.id = id
    
    def get_required_fields(self):
        return {
            'name': str,
            'description': str,
            'photo': str,
            'id': int
        }

    def get_field_constraints(self):
        return {

        }