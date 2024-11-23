
from flaskr.dtos.base_dto import BaseDTO

class UpdateNotificationDTO(BaseDTO):
    def __init__(self, read_at=None):
        self.read_at = read_at,

    def get_required_fields(self):
        return {
            'read_at': str
        }