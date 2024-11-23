
from flaskr.dtos.base_dto import BaseDTO

class NotificationDTO(BaseDTO):
    def __init__(self, id=None, subject=None, body=None, created_at=None, read_at=None, user_id=None):
        self.id = id,
        self.subject = subject,
        self.body = body,
        self.created_at = created_at,
        self.read_at = read_at,
        self.user_id = user_id