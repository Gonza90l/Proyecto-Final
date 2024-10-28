# database.py
from flask_mysqldb import MySQL
import mysql.connector
import os
from .database_interface import IDatabase

class FlaskMySQLDatabase(IDatabase):
    def __init__(self):
        self.mysql = MySQL()

    def init_app(self, app):
        self.mysql.init_app(app)

    @property
    def connection(self):
        return self.mysql.connection

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.connection.cursor()

class MySQLConnectorDatabase(IDatabase):
    def __init__(self):
        self._connection = None

    def init_app(self, app):
        self._connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port=3306,
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')
        )

    @property
    def connection(self):
        return self._connection

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.connection.cursor()