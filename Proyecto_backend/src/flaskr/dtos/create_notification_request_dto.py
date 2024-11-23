
from flaskr.dtos.base_dto import BaseDTO

class CreateNotificationRequestDTO(BaseDTO):
    def __init__(self, id=None, subject=None, body=None, created_at=None, read_at=None, user_id=None):
        self.subject = subject,
        self.body = body,
        self.user_id = user_id