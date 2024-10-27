# flaskr/injection_config.py
from injector import singleton, Binder
from flask_mysqldb import MySQL
from .services.users_service import UsersService
from .controllers.controller import ExampleController
from .controllers.users_controller import UsersController

def configure(binder: Binder, mysql):
    # Vincular UserService a su implementación
    user_service = UsersService(mysql)
    binder.bind(UsersService, to=user_service, scope=singleton)
    
    # Vincular ExampleController a su implementación
    example_controller = ExampleController(mysql)
    binder.bind(ExampleController, to=example_controller, scope=singleton)
    