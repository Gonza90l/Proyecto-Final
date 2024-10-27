import time
from .cache_interface import CacheInterface

class MemoryCache(CacheInterface):
    def __init__(self):
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            value, exp = self.cache[key]
            if exp > time.time():
                return value
            else:
                self.delete(key)
        return None

    def set(self, key, value, ttl):
        exp = time.time() + ttl
        self.cache[key] = (value, exp)

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def cleanup(self):
        current_time = time.time()
        keys_to_delete = [key for key, (_, exp) in self.cache.items() if exp <= current_time]
        for key in keys_to_delete:
            self.delete(key)

