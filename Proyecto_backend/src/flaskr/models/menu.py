from .base_model import BaseModel

class Menu(BaseModel):
    def __init__(self, mysql):
        table = 'menu'
        fields = ['id', 'name', 'description', 'price', 'photo', 'deleted_flag', 'category_id']
        deleted_flag = 'deleted_flag' # Campo de bandera de eliminación
        super().__init__(mysql, table, fields, deleted_flag)
