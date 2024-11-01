# __init__.py
from flask import Flask
from flask_injector import FlaskInjector
from flask_cors import CORS
from .database.database import FlaskMySQLDatabase, MySQLConnectorDatabase
import os
from .middlewares import log_request, log_response
from .injection_config import configure
import ssl

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.configure_app()
        self.configure_database()
        self.configure_middlewares()
        self.configure_routes()
        self.configure_injection()
        self.configure_cors()
        self.configure_ssl()

    def configure_app(self):
        # Configurar la conexión a la base de datos
        self.app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
        self.app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
        self.app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
        self.app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
        self.app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'flaskapp')
        self.app.config['MYSQL_CURSORCLASS'] = os.getenv('MYSQL_CURSORCLASS', 'DictCursor')
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clavesecreta')

    def configure_database(self):
        # Inicializar la extensión MySQL como singleton
        # Seleccionar la implementación de la base de datos
        use_flask_mysqldb = os.getenv('USE_FLASK_MYSQLDB', 'True').lower() in ['true', '1', 't', 'y', 'yes']
        if use_flask_mysqldb:
            print("Using Flask-MySQLdb")
            self.db = FlaskMySQLDatabase()
        else:
            print("Using MySQL Connector")
            self.db = MySQLConnectorDatabase()
        
        self.db.init_app(self.app)

    def configure_middlewares(self):
        # Registrando los middlewares entrantes
        self.app.before_request(log_request)
        # Registrando los middlewares salientes
        self.app.after_request(log_response)

    def configure_routes(self):
        # Importaamos las rutas de la aplicación
        from .routes.routes import main
        self.app.register_blueprint(main)

    def configure_injection(self):
        # Configurar la inyección de dependencias
        FlaskInjector(app=self.app, modules=[lambda binder: configure(binder, self.db)])

    def configure_cors(self):
        # Configurar CORS
        cors_config = {
            "origins": os.getenv('CORS_ORIGINS').split(','),  # Orígenes permitidos
            "methods": os.getenv('CORS_METHODS').split(','),  # Métodos HTTP permitidos
            "allow_headers": os.getenv('CORS_ALLOW_HEADERS').split(','),  # Cabeceras permitidas
        }
        CORS(self.app, resources={r"/*": cors_config})

    def configure_ssl(self):
        # Crear un contexto SSL
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # Cargar el certificado y la clave
        self.context.load_cert_chain(certfile=os.getenv('SSL_CERTFILE'), keyfile=os.getenv('SSL_KEYFILE'))

    def get_app(self):
        return self.app

    def get_ssl_context(self):
        return self.context