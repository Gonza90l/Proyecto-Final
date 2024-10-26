# flaskr/__init__.py
from flask import Flask
from flask_injector import FlaskInjector
from .middlewares import log_request, log_response

def create_app():
    app = Flask(__name__)

    # Registrar el middleware entrante
    app.before_request(log_request)
    # Registrar el middleware saliente
    app.after_request(log_response)

    # Importar y registrar las rutas
    from .routes.routes import main
    app.register_blueprint(main)

    # Configurar Flask-Injector
    from .injection_config import configure
    FlaskInjector(app=app, modules=[configure])

    return app