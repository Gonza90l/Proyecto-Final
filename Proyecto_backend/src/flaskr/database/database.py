from flask_mysqldb import MySQL
import mysql.connector
import os
from .database_interface import IDatabase
from mysql.connector import cursor

class FlaskMySQLDatabase(IDatabase):
    """
    Implementación de la interfaz IDatabase utilizando Flask-MySQLdb.
    """
    def __init__(self):
        self.mysql = MySQL()

    def init_app(self, app):
        """
        Inicializa la aplicación Flask con la configuración de la base de datos.

        :param app: La aplicación Flask.
        """
        self.mysql.init_app(app)

    @property
    def connection(self):
        """
        Obtiene la conexión a la base de datos.

        :return: Conexión a la base de datos.
        """
        return self.mysql.connection

    def get_connection(self):
        """
        Obtiene la conexión a la base de datos.

        :return: Conexión a la base de datos.
        """
        return self.connection

    def get_cursor(self):
        """
        Obtiene un cursor para ejecutar consultas en la base de datos.

        :return: Cursor de la base de datos.
        """
        return self.connection.cursor()

class MySQLConnectorDatabase(IDatabase):
    """
    Implementación de la interfaz IDatabase utilizando mysql-connector-python.
    """
    def __init__(self):
        self._connection = None

    def init_app(self, app):
        """
        Inicializa la aplicación Flask con la configuración de la base de datos.

        :param app: La aplicación Flask.
        """
        self._connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port=3306,
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')
        )

    @property
    def connection(self):
        """
        Obtiene la conexión a la base de datos.

        :return: Conexión a la base de datos.
        """
        return self._connection

    def get_connection(self):
        """
        Obtiene la conexión a la base de datos.

        :return: Conexión a la base de datos.
        """
        return self.connection

    def get_cursor(self):
        """
        Obtiene un cursor para ejecutar consultas en la base de datos.

        :return: Cursor de la base de datos.
        """
        return self.connection.cursor(cursor_class=MySQLCursorDict)

class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):
    """
    Cursor personalizado para devolver resultados como diccionarios.
    """
    def _row_to_python(self, rowdata, desc=None):
        """
        Convierte una fila de datos en un diccionario.

        :param rowdata: Datos de la fila.
        :param desc: Descripción de la fila.
        :return: Fila convertida en diccionario.
        """
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None