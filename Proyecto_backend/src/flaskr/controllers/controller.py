# app/controllers/controller.py
from flaskr.controllers.base_controller import BaseController
from flaskr.services.users_service import UsersService
from flaskr.auth import token_required 
from injector import inject
from flaskr.models.user import User

class ExampleController(BaseController):
    @inject
    def __init__(self, mysql):
        self.mysql = mysql

    def handle_request(self):
        #data = self.get_json_data()  # Acceder a los datos JSON de la solicitud
        #query_params = self.get_query_params()  # Acceder a los parámetros de la URL
        #headers = self.get_headers()  # Acceder a los encabezados de la solicitud
        #cookies = self.get_cookies()  # Acceder a las cookies de la solicitud

        #retornamos un json con los datos de la solicitud
        #creamos un usuario en la base de datos

        user = User(self.mysql)
        user.name = "Juan"
        user.email = "juan@example.com"
        user.password = "1234"
        user.role = "admin"
        user.lastname = "Perez"
        user.insert()

        return self.respond_success(data=user.to_json_dto())


