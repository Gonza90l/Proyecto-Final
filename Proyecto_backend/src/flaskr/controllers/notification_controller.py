
from flask_injector import inject
from flaskr.controllers.base_controller import BaseController
from flaskr.services.notification_service import NotificationService
from flaskr.auth import get_user_id, get_user_role, token_required, role_required


class NotificationController(BaseController):
    @inject
    def __init__(self, notification_service: NotificationService):
        self._notification_service = notification_service

    @token_required
    def get_notifications(self):
        # OBTENEMOS EL ID DEL USUARIO
        user_id = get_user_id()

        # OBTENEMOS LAS NOTIFICACIONES DEL USUARIO
        notifications = self._notification_service.get_notifications(user_id)
        notifications_dto = [notification.to_dict_dto() for notification in notifications]
        return self.respond_success(data=notifications_dto)

    def get_notification(self, notification_id):
        #OBTENEMOS LA NOTIFICACION
        notification = self._notification_service.get_notification(notification_id)
        #convertimos la notificacion a diccionario
        return self.respond_success(data=notification.to_dict_dto())

    @role_required('ADMIN')
    def create_notification(self):
        #OBTENEMOS EL ID DEL USUARIO
        user_id = get_user_id()

        #CREAMOS LA NOTIFICACION
        notification_id = self._notification_service.create_notification(user_id)
        return self.send_response(notification_id)
