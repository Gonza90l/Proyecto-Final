from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, mysql):
        # Definimos la tabla y los campos específicos para el modelo User
        fields = ['id', 'name', 'lastname', 'email', 'password', 'role']
        table = 'users'
        super().__init__(mysql, table, fields)