from flaskr.models.notification import Notification
from flaskr.exceptions.notification_service_exceptions import NotificationNotFoundException
from flask_injector import inject
from flaskr.database.database_interface import IDatabase

class NotificationService:
    
    @inject
    def __init__(self, mysql: IDatabase):
        self._mysql = mysql

    def get_notifications(self, user_id):
        notifications = Notification.find_by_user_id(self._mysql, user_id)
        return notifications

    def get_notification(self, notification_id):
        notification = Notification.find_by_id(self._mysql, notification_id)
        if not notification:
            raise NotificationNotFoundException("Notification not found")
        return notification

    def create_notification(self, create_notification_request_dto):
        notification = Notification(self._mysql)
        notification.from_dto(create_notification_request_dto)
        notification.insert()
        return notification.id

    def update_notification(self, notification_id, update_notification_request_dto):
        notification = Notification.find_by_id(self._mysql, notification_id)
        if not notification:
            raise NotificationNotFoundException("Notification not found")
        notification.from_dto(update_notification_request_dto)
        notification.update()

    def delete_notification(self, notification_id):
        notification = Notification.find_by_id(self._mysql, notification_id)
        if not notification:
            raise NotificationNotFoundException("Notification not found")
        notification.delete()
        return notification_id