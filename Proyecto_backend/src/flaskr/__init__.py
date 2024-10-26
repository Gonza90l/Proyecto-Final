from flask import Flask
from flask_injector import FlaskInjector
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from .middlewares import log_request, log_response
from .injection_config import configure

# Initialize MySQL
mysql = MySQL()

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['MYSQL_CURSORCLASS'] = os.getenv('MYSQL_CURSORCLASS')

    mysql.init_app(app)

    # Create users table if it doesn't exist
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(80) NOT NULL UNIQUE,
                email VARCHAR(120) NOT NULL UNIQUE,
                password_hash VARCHAR(128) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        mysql.connection.commit()
        cursor.close()

    # Register the incoming middleware
    app.before_request(log_request)
    # Register the outgoing middleware
    app.after_request(log_response)

    # Import and register routes
    from .routes.routes import main
    app.register_blueprint(main)

    # Configure Flask-Injector
    FlaskInjector(app=app, modules=[lambda binder: configure(binder, mysql)])

    return app