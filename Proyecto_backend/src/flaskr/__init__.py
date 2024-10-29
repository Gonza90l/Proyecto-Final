#__init__.py
from flask import Flask
from flask_injector import FlaskInjector
from .database.database import FlaskMySQLDatabase, MySQLConnectorDatabase
import os
from .middlewares import log_request, log_response
from .injection_config import configure
import threading
import time
from .cache.cache_interface import CacheInterface
from .cache.memory_cache import MemoryCache

def create_app():

    # Crear la aplicación Flask
    app = Flask(__name__)
    # Configurar la conexión a la base de datos
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD','')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB','flaskapp')
    app.config['MYSQL_CURSORCLASS'] = os.getenv('MYSQL_CURSORCLASS','DictCursor')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','clavesecreta')

    # Inicializar la extensión MySQL como singleton
    # Seleccionar la implementación de la base de datos
    use_flask_mysqldb = os.getenv('USE_FLASK_MYSQLDB', 'True').lower() in ['true', '1', 't', 'y', 'yes']
    if use_flask_mysqldb:
        print("Using Flask-MySQLdb")
        db = FlaskMySQLDatabase()
    else:
        print("Using MySQL Connector")
        db = MySQLConnectorDatabase()
    
    db.init_app(app)

    # Registrando los middlewares entrantes
    app.before_request(log_request)
    # Registrando los middlewares salientes
    app.after_request(log_response)

    # Importaamos las rutas de la aplicación
    from .routes.routes import main
    app.register_blueprint(main)

    # Configurar la inyección de dependencias
    FlaskInjector(app=app, modules=[lambda binder: configure(binder, db)])


    return app