import time
import threading
from .cache_interface import CacheInterface

class MemoryCache(CacheInterface):
    def __init__(self, cleanup_interval=60):
        self.cache = {}
        self.cleanup_interval = cleanup_interval
        self._start_cleanup_thread()

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

    def _start_cleanup_thread(self):
        def run_cleanup():
            while True:
                time.sleep(self.cleanup_interval)
                self.cleanup()

        cleanup_thread = threading.Thread(target=run_cleanup, daemon=True)
        cleanup_thread.start()

cache: CacheInterface = MemoryCache() # Instancia de la cache
