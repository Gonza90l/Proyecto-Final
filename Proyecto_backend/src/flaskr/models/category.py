from .base_model import BaseModel

class Category(BaseModel):
    _table = 'category'
    _fields = ['id', 'name', 'description', 'photo']