# run.py
from flaskr import create_app
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_ENV') == 'development')