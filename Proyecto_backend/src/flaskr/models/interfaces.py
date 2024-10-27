from abc import ABC, abstractmethod

class IModel(ABC):
    '''La interfaz IModel define un contrato genérico para cualquier clase que implemente un modelo en la aplicación.
    Utiliza la biblioteca abc (Abstract Base Classes) de Python para asegurar que las clases que implementen esta interfaz
    proporcionen implementaciones concretas de los métodos definidos.'''

    @abstractmethod
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL y realiza un commit en la base de datos."""
        pass

    @abstractmethod
    def fetch_one(self, query, params=None):
        """Recupera una única fila de la base de datos."""
        pass

    @abstractmethod
    def fetch_all(self, query, params=None):
        """Recupera todas las filas de una consulta SQL."""
        pass

    @abstractmethod
    def insert(self, table, data):
        """Inserta un nuevo registro en una tabla específica."""
        pass

    @abstractmethod
    def update(self, table, data, where_clause, where_params):
        """Actualiza un registro existente en una tabla específica."""
        pass

    @abstractmethod
    def delete(self, table, where_clause, where_params):
        """Elimina un registro en una tabla específica."""
        pass

    @abstractmethod
    def find_by_id(self, table, id):
        """Encuentra un registro en una tabla usando su ID."""
        pass

    @abstractmethod
    def find_all(self, table):
        """Recupera todos los registros de una tabla."""
        pass