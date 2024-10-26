# app/controllers/controller.py
from flaskr.controllers.base_controller import BaseController
from flaskr.services.user_service import UserService
from app.auth import token_required
from injector import inject

class ExampleController(BaseController):
    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @token_required
    def handle_request(self):
        data = self.get_json_data()  # Acceder a los datos JSON de la solicitud
        query_params = self.get_query_params()  # Acceder a los parámetros de la URL
        headers = self.get_headers()  # Acceder a los encabezados de la solicitud
        cookies = self.get_cookies()  # Acceder a las cookies de la solicitud

        return self.respond_success(data={
            "message": "This is an example controller",
            "received_data": data,
            "query_params": query_params,
            "headers": headers,
            "cookies": cookies
        })

class UserController(BaseController):
    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @token_required
    def get_user(self, user_id):
        user = self.user_service.get_user(user_id)
        return self.respond_success(data=user)