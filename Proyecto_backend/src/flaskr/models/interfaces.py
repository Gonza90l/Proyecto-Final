from abc import ABC, abstractmethod

class IModel(ABC):
    '''La interfaz IModel define un contrato genérico para cualquier clase que implemente un modelo en la aplicación.
    Utiliza la biblioteca abc (Abstract Base Classes) de Python para asegurar que las clases que implementen esta interfaz
    proporcionen implementaciones concretas de los métodos definidos.'''

    @abstractmethod
    def execute_query(self, query, params=None):
        pass

    @abstractmethod
    def fetch_one(self, query, params=None):
        pass

    @abstractmethod
    def fetch_all(self, query, params=None):
        pass

    @abstractmethod
    def insert(self, table, data):
        pass

    @abstractmethod
    def update(self, table, data, where_clause, where_params):
        pass

    @abstractmethod
    def delete(self, table, where_clause, where_params):
        pass

    @abstractmethod
    def find_by_id(self, table, id):
        pass

    @abstractmethod
    def find_all(self, table):
        pass