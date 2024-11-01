from .base_model import BaseModel


class Order(BaseModel):
    _table = '`order`'
    _fields = ['id', 'created_at', 'updated_at', 'user_id', 'total', 'status']
    _relationships = {'order_items': {'class': 'OrderHasMenu', 'foreign_key': 'order_id'}}