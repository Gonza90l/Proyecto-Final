# run.py
from flaskr import FlaskApp
import os

# Crear la aplicación de Flask
flask_app_instance = FlaskApp() # Creamos una instancia de la clase FlaskApp
app = flask_app_instance.get_app() # Obtenemos la aplicación de la instancia 
context = flask_app_instance.get_ssl_context() # Obtenemos el contexto SSL de la instancia de FlaskApp

# Iniciar la aplicación de Flask
if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_HOST', '0.0.0.0'), port=int(os.getenv('FLASK_PORT', 5000)), ssl_context=context, debug=os.getenv('FLASK_ENV') == 'development')