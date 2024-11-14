from abc import ABC, abstractmethod

class IDatabase(ABC):
    """
    Interfaz para la base de datos, define los métodos que deben ser implementados por cualquier clase que la herede.
    """

    @abstractmethod
    def init_app(self, app):
        """
        Inicializa la aplicación con la configuración de la base de datos.

        :param app: La aplicación Flask.
        """
        pass

    @abstractmethod
    def get_connection(self):
        """
        Obtiene una conexión a la base de datos.

        :return: Conexión a la base de datos.
        """
        pass

    @abstractmethod
    def get_cursor(self):
        """
        Obtiene un cursor para ejecutar consultas en la base de datos.

        :return: Cursor de la base de datos.
        """
        pass