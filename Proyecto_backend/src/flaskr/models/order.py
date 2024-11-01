from .base_model import BaseModel

class Order(BaseModel):
    _table = '`order`'
    _fields = ['id','created_at','updated_at','user_id','total','status']
