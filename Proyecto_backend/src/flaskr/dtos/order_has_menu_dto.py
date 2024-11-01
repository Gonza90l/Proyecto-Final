
from flaskr.dtos.base_dto import BaseDTO

class OrderHasMenuDTO(BaseDTO):
    def __init__(self, item=None, quantity=None):
        self.quantity = quantity
        #por la relacion con menu se crea un objeto de item de menu desde la clase OrderDTO
