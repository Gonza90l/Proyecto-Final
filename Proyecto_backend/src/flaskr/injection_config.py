# flaskr/injection_config.py
from injector import singleton, Binder
from flask_mysqldb import MySQL
from .services.users_service import UsersService
from .repositories.user_repository import UserRepository
from .controllers.controller import ExampleController
from .controllers.users_controller import UsersController

def configure(binder: Binder, mysql: MySQL):
    # Vincular UserRepository a su implementación
    user_repository = UserRepository(mysql)
    binder.bind(UserRepository, to=user_repository, scope=singleton)
    
    # Vincular UserService a su implementación
    user_service = UsersService(user_repository)
    binder.bind(UsersService, to=user_service, scope=singleton)
    
    # Vincular ExampleController a su implementación
    example_controller = ExampleController(mysql)
    binder.bind(ExampleController, to=example_controller, scope=singleton)
    