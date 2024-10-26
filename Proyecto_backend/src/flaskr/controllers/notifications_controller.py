from app.controllers.base_controller import BaseController
from app.services.notifications_service import NotificationsService
from app.auth import token_required
from injector import inject

class NotificationsController(BaseController):
    @inject
    def __init__(self, notifications_service: NotificationsService):
        self.notifications_service = notifications_service

    @token_required
    def get_notifications(self, user_id):
        notifications = self.notifications_service.get_notifications(user_id)
        return self.respond_success(data=notifications)

    @token_required
    def create_notification(self):
        data = self.get_json_data()
        notification = self.notifications_service.create_notification(data)
        return self.respond_success(data=notification)

    @token_required
    def delete_notification(self, notification_id):
        notification = self.notifications_service.delete_notification(notification_id)
        return self.respond_success(data=notification)