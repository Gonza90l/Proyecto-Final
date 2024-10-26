# flaskr/injection_config.py
from injector import singleton, Binder
from flask_mysqldb import MySQL
from .services.user_service import UserService
from .repositories.user_repository import UserRepository
from .controllers.controller import ExampleController, UserController

def configure(binder: Binder, mysql: MySQL):
    # Vincular UserRepository a su implementación
    user_repository = UserRepository(mysql)
    binder.bind(UserRepository, to=user_repository, scope=singleton)
    
    # Vincular UserService a su implementación
    user_service = UserService(user_repository)
    binder.bind(UserService, to=user_service, scope=singleton)
    
    # Vincular ExampleController a su implementación
    example_controller = ExampleController(user_service)
    binder.bind(ExampleController, to=example_controller, scope=singleton)
    
    # Vincular UserController a su implementación
    user_controller = UserController(user_service)
    binder.bind(UserController, to=user_controller, scope=singleton)