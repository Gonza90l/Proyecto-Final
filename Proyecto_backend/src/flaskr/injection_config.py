# flaskr/injection_config.py
from injector import singleton, Binder
from flask_mysqldb import MySQL
from .services.users_service import UsersService
from .services.menu_service import MenuService

def configure(binder: Binder, mysql):
    # Vincular UserService a su implementación
    user_service = UsersService(mysql)
    binder.bind(UsersService, to=user_service, scope=singleton)

    # Vincular MenuService a su implementación
    menu_service = MenuService(mysql)
    binder.bind(MenuService, to=menu_service, scope=singleton)

    # Vincular ExampleController a su implementación
    #example_controller = ExampleController(mysql)
    #binder.bind(ExampleController, to=example_controller, scope=singleton)
    