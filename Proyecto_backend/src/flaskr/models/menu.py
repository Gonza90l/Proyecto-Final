from .base_model import BaseModel

class Menu(BaseModel):
    _table = 'menu'
    _fields = ['id', 'name', 'description', 'price', 'photo', 'deleted_flag', 'category_id']
    _deleted_flag = 'deleted_flag'  # Campo de bandera de eliminación