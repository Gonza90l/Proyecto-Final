from app.controllers.base_controller import BaseController
from app.services.orders_service import OrdersService
from app.auth import token_required
from injector import inject

class OrdersController(BaseController):
    @inject
    def __init__(self, orders_service: OrdersService):
        self.orders_service = orders_service

    @token_required
    def get_orders(self, user_id):
        orders = self.orders_service.get_orders(user_id)
        return self.respond_success(data=orders)

    @token_required
    def create_order(self):
        data = self.get_json_data()
        order = self.orders_service.create_order(data)
        return self.respond_success(data=order)

    @token_required
    def delete_order(self, order_id):
        order = self.orders_service.delete_order(order_id)
        return self.respond_success(data=order)