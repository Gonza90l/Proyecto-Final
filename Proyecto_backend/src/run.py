# run.py
from flaskr import FlaskApp
import os

# Crear la aplicación de Flask
flask_app_instance = FlaskApp()  # Creamos una instancia de la clase FlaskApp
app = flask_app_instance.get_app()  # Obtenemos la aplicación de la instancia
context = flask_app_instance.get_ssl_context()  # Obtenemos el contexto SSL de la instancia de FlaskApp

# Iniciar la aplicación de Flask
if __name__ == '__main__':
    if os.getenv('FLASK_ENV') == 'development':
        #si es desarrollo se usa el servidor de desarrollo de Flask
        app.run(host=os.getenv('FLASK_HOST', '0.0.0.0'), port=int(os.getenv('FLASK_PORT', 5000)), ssl_context=context, debug=True)
    else:
        #si es producción se usa gunicorn
        from gunicorn.app.base import BaseApplication

        class GunicornApp(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                config = {key: value for key, value in self.options.items()
                          if key in self.cfg.settings and value is not None}
                for key, value in config.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        options = {
            'bind': f"{os.getenv('FLASK_HOST', '0.0.0.0')}:{os.getenv('FLASK_PORT', '5000')}",
            'workers': 4,
            'certfile': os.getenv('SSL_CERTFILE'),
            'keyfile': os.getenv('SSL_KEYFILE'),
        }
        GunicornApp(app, options).run()