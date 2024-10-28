from flask import Flask
from flask_injector import FlaskInjector
from .database.database import FlaskMySQLDatabase, MySQLConnectorDatabase
import os
from .middlewares import log_request, log_response
from .injection_config import configure
import threading
import time

def cleanup_cache():
    """Función para limpiar la cache"""
    while True:
        time.sleep(600)  # Intervalo de limpieza en segundos
        cache.cleanup()

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
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','clavesecreta')  # Ensure this line is present

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

    # Crear la tabla de usuarios si no existe
    # Crear la tabla de usuarios si no existe
    with app.app_context():
        cursor = db.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                lastname VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL,
                role VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.connection.commit()
        cursor.close()

    # Registrando los middlewares entrantes
    app.before_request(log_request)
    # Registrando los middlewares salientes
    app.after_request(log_response)

    # Importaamos las rutas de la aplicación
    from .routes.routes import main
    app.register_blueprint(main)

    # Configurar la inyección de dependencias
    FlaskInjector(app=app, modules=[lambda binder: configure(binder, db)])

     # Iniciar el hilo de limpieza de la cache
    cleanup_thread = threading.Thread(target=cleanup_cache, daemon=True)
    cleanup_thread.start()

    return app