from abc import ABC, abstractmethod

class CacheInterface(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value, ttl):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def cleanup(self):
        pass