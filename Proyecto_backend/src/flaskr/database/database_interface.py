from abc import ABC, abstractmethod

class IDatabase(ABC):
    @abstractmethod
    def init_app(self, app):
        pass

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def get_cursor(self):
        pass