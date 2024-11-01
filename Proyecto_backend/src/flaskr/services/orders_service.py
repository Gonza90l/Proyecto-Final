from flask_injector import inject
from flaskr.database.database_interface import IDatabase
from flaskr.models.order import Order
from flaskr.exceptions.order_service_exceptions import OrderNotFoundException

class OrderService:

    @inject
    def __init__(self, mysql: IDatabase):
        self._mysql = mysql

    def get_orders(self):
        orders = Order.find_all(self._mysql)
        for order in orders:
            print(order)
            order.load_related_data()
            for order_item in order.order_items:
                order_item.load_related_data()
                print(order_item)
        return orders

    def get_order(self, order_id):
        order = Order.find_by_id(self._mysql, order_id)
        if not order:
            raise OrderNotFoundException("Order not found")
        order.load_related_data()
        for order_item in order.order_items:
            order_item.load_related_data()
        return order

    def create_order(self, create_order_request_dto):
        order = Order()
        order.from_dto(create_order_request_dto)
        order.insert(self._mysql)
        return order

    def update_order(self, order_id, update_order_request_dto):
        order = Order.find_by_id(self._mysql, order_id)
        if not order:
            raise OrderNotFoundException("Order not found")
        order.set(**update_order_request_dto.to_dict())
        order.update(self._mysql)
        return order

    def delete_order(self, order_id):
        raise Exception("Not implemented, orders cannot be deleted, only updated and created")