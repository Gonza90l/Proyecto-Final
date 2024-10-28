# run.py
from flaskr import create_app
from dotenv import load_dotenv
from flask_cors import CORS
import os
import ssl
import logging

# Configurar el registro
logging.basicConfig(level=logging.INFO)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = create_app()

cors_config = {
    "origins": ["https://proyecto_frontend.test"],  # Orígenes permitidos
    "methods": ["GET", "POST", "PUT", "DELETE"],  # Métodos HTTP permitidos
    "allow_headers": ["Content-Type", "Authorization"],  # Cabeceras permitidas
}
CORS(app, resources={r"/*": cors_config})

if __name__ == '__main__':
    # Crear un contexto SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="./flaskr/ssl/cert.pem", keyfile="./flaskr/ssl/key.pem")
    
    app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=os.getenv('FLASK_ENV') == 'development')