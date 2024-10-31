from .base_model import BaseModel

class User(BaseModel):
    _table = 'user'
    _fields = ['id', 'name', 'lastname', 'email', 'password', 'role', 'created_at', 'deleted_flag']
    _deleted_flag = 'deleted_flag'  # Campo de bandera de eliminación

    @classmethod
    def find_by_email(cls, mysql, email):
        """Busca un usuario por su email"""
        query = f"SELECT * FROM {cls._table} WHERE email = %s AND {cls._deleted_flag} = 0"
        result = cls.fetch_one(mysql, query, (email,))
        if result:
            return cls(mysql, **result)
        return None