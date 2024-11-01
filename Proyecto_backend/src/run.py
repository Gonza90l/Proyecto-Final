# run.py
from flaskr import FlaskApp
from dotenv import load_dotenv
import os
import logging

# Configurar el registro basado en el .env
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Crear la aplicación de Flask
flask_app_instance = FlaskApp()
app = flask_app_instance.get_app()
context = flask_app_instance.get_ssl_context()

# Iniciar la aplicación de Flask
if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_HOST', '0.0.0.0'), port=int(os.getenv('FLASK_PORT', 5000)), ssl_context=context, debug=os.getenv('FLASK_ENV') == 'development')