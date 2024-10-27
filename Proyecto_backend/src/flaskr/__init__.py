from flask import Flask
from flask_injector import FlaskInjector
from flask_mysqldb import MySQL
import os
from .middlewares import log_request, log_response
from .injection_config import configure
import threading
from .cache.memory_cache import MemoryCache
import time

# Inicializar la extensión MySQL
mysql = MySQL()
# Crear una instancia de la cache
cache = MemoryCache()

def cleanup_cache():
    """Función para limpiar la cache"""
    while True:
        time.sleep(600)  # Intervalo de limpieza en segundos
        cache.cleanup()

def create_app():

    # Crear la aplicación Flask
    app = Flask(__name__)
    # Configurar la conexión a la base de datos
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['MYSQL_CURSORCLASS'] = os.getenv('MYSQL_CURSORCLASS')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Ensure this line is present


    # Inicializar la extensión MySQL como singleton
    mysql.init_app(app)
    # Crear la tabla de usuarios si no existe
    #campos = ['id', 'name', 'lastname', 'email', 'password', 'role']
    with app.app_context():
        cursor = mysql.connection.cursor()
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
        mysql.connection.commit()
        cursor.close()

    # Registrando los middlewares entrantes
    app.before_request(log_request)
    # Registrando los middlewares salientes
    app.after_request(log_response)

    # Importaamos las rutas de la aplicación
    from .routes.routes import main
    app.register_blueprint(main)

    # Configurar la inyección de dependencias
    FlaskInjector(app=app, modules=[lambda binder: configure(binder, mysql)])

     # Iniciar el hilo de limpieza de la cache
    cleanup_thread = threading.Thread(target=cleanup_cache, daemon=True)
    cleanup_thread.start()

    return app