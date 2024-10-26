# flaskr/injection_config.py
from injector import singleton


def configure(binder):
    from app.services.user_service import UserService
    from app.repositories.user_repository import UserRepository

    # Vincular UserRepository a su implementación
    binder.bind(UserRepository, to=UserRepository, scope=singleton)
    
    # Vincular UserService a su implementación
    binder.bind(UserService, to=UserService, scope=singleton)