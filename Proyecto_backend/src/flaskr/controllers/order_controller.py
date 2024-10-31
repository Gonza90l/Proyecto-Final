from flaskr.controllers.base_controller import BaseController
from flask_injector import inject

class OrderController(BaseController):
    def __init__(self, order_service):
        self._order_service = order_service
