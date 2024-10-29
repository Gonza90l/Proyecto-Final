from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, mysql):
        fields = ['id', 'name', 'lastname', 'email', 'password', 'role', 'created_at', 'deleted_flag']
        table = 'user'
        deleted_flag = 'deleted_flag' # Campo de bandera de eliminación
        super().__init__(mysql, table, fields, deleted_flag)

    def find_by_email(self, email):
        """Busca un usuario por su email"""
        query = f"SELECT * FROM {self._table} WHERE email = %s AND deleted_flag = 0"
        result = self.fetch_one(query, (email,))
        if result:
            self.set(**result)
        return result
