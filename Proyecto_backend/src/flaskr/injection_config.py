# flaskr/injection_config.py
from flask_injector import singleton, Binder
from flaskr.database.database_interface import IDatabase
from flaskr.services.users_service import UsersService
from flaskr.services.menu_service import MenuService
from flaskr.services.orders_service import OrderService
from flaskr.services.image_service import ImageService

def configure(binder: Binder, db):
    # Bind de la base de datos mediante la interfaz IDatabase
    binder.bind(IDatabase, to=db, scope=singleton)

    # Bind de UsersService a su implementación
    binder.bind(UsersService, to=UsersService, scope=singleton)

    # Bind de MenuService a su implementación
    binder.bind(MenuService, to=MenuService, scope=singleton)

    # Bind de OrderService a su implementación
    binder.bind(OrderService, to=OrderService, scope=singleton)

    # Bind de ImageService a su implementación
    binder.bind(ImageService, to=ImageService, scope=singleton)