from .base_model import BaseModel

class Notification(BaseModel):
    _table = 'notification'
    _fields = ['id', 'created_at', 'read_at', 'subject', 'user_id', 'body']

    @classmethod
    def find_by_user_id(cls, mysql, id):
        """Busca las notificaciones de un usuario"""
        query = f"SELECT * FROM {cls._table} WHERE user_id = %s"
        results = cls.fetch_all(mysql, query, (id,))
        return [cls(mysql, **result) for result in results]