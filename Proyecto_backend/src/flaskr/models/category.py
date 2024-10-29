from .base_model import BaseModel

class Category(BaseModel):
    def __init__(self, mysql):
        table = 'category'
        fields = ['id', 'name', 'description', 'photo']
        super().__init__(mysql, table, fields)
