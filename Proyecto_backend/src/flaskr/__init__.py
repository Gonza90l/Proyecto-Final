from flask import Flask
from flask_injector import FlaskInjector
from flask_cors import CORS
from .database.database import FlaskMySQLDatabase, MySQLConnectorDatabase
import os
from .middlewares import log_request, log_response
from .injection_config import configure
import ssl
from dotenv import load_dotenv
import logging
from flaskr.database.database_interface import IDatabase

class FlaskApp:
    def __init__(self):
        load_dotenv()
        logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
        self._app = Flask(__name__)
        self.configure_app()
        self.configure_database()
        self.configure_middlewares()
        self.configure_routes()
        self.configure_injection()
        self.configure_cors()
        self.configure_ssl()


    def configure_app(self):
        # Configurar la conexión a la base de datos
        self._app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
        self._app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
        self._app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
        self._app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
        self._app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'flaskapp')
        self._app.config['MYSQL_CURSORCLASS'] = os.getenv('MYSQL_CURSORCLASS', 'DictCursor')
        self._app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clavesecreta')

    def configure_database(self):
        # Inicializar la extensión MySQL como singleton
        # Seleccionar la implementación de la base de datos
        use_flask_mysqldb = os.getenv('USE_FLASK_MYSQLDB', 'True').lower() in ['true', '1', 't', 'y', 'yes']
        if use_flask_mysqldb:
            print("Using Flask-MySQLdb")
            self._db: IDatabase = FlaskMySQLDatabase()
        else:
            print("Using MySQL Connector")
            self._db: IDatabase = MySQLConnectorDatabase()
        
        self._db.init_app(self._app)

    def configure_middlewares(self):
        # Registrando los middlewares entrantes
        self._app.before_request(log_request)
        # Registrando los middlewares salientes
        self._app.after_request(log_response)

    def configure_routes(self):
        # Importaamos las rutas de la aplicación
        from .routes.routes import main
        self._app.register_blueprint(main)

    def configure_injection(self):
        # Configurar la inyección de dependencias
        FlaskInjector(app=self._app, modules=[lambda binder: configure(binder, self._db)])

    def configure_cors(self):
        # Configurar CORS
        cors_config = {
            "origins": os.getenv('CORS_ORIGINS').split(','),  # Orígenes permitidos
            "methods": os.getenv('CORS_METHODS').split(','),  # Métodos HTTP permitidos
            "allow_headers": os.getenv('CORS_ALLOW_HEADERS').split(','),  # Cabeceras permitidas
        }
        CORS(self._app, resources={r"/*": cors_config})

    def configure_ssl(self):
        # Crear un contexto SSL
        self._context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # Cargar el certificado y la clave
        self._context.load_cert_chain(certfile=os.getenv('SSL_CERTFILE'), keyfile=os.getenv('SSL_KEYFILE'))

    def get_app(self):
        return self._app

    def get_ssl_context(self):
        return self._context