from flask_injector import inject
from flaskr.database.database_interface import IDatabase
from flaskr.models.order import Order
from flaskr.exceptions.order_service_exceptions import OrderNotFoundException
from flaskr.models.order_has_menu import OrderHasMenu
from flaskr.dtos.create_order_request_dto import CreateOrderRequestDTO
from flaskr.dtos.create_order_has_menu_request_dto import CreateOrderHasMenuRequestDTO
from datetime import datetime


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

    def _validate_status(self, status):
        valid_statuses = ['CREATED','PAID','IN PROGRESS','SEND','DELIVERED','CANCELED'] 
        status = status.upper()  # Convertir a mayúsculas
        if status not in valid_statuses:
            raise ValueError(f"Invalid status value: {status}")
        return status

    def create_order(self, create_order_request_dto):
        # Create the Order instance
        order = Order(self._mysql)
        order.from_dto(create_order_request_dto)
        order.created_at = datetime.now()
        order.status = self._validate_status(create_order_request_dto.status)  # Ajusta el valor de status

        order.insert()

        # Create OrderHasMenu instances for each item in order_items
        order_items = create_order_request_dto.order_items
        for item_dto in order_items:
            try:
                order_item_dto = CreateOrderHasMenuRequestDTO(**item_dto)
                order_item = OrderHasMenu(self._mysql)
                order_item.from_dto(order_item_dto)
                order_item.order_id = order.id  # Set the order_id to the newly created order's id
                order_item.insert()
            except ValueError as e:
                raise ValueError(f"Invalid DTO format for order item: {item_dto}") from e

        return order.id

    def processPayment(self, order_id):
        order = Order.find_by_id(self._mysql, order_id)
        if not order:
            raise OrderNotFoundException("Order not found")
        order.status = "PAID"
        order.update()
        return order

    '''def update_order(self, order_id, update_order_request_dto):
        order = Order.find_by_id(self._mysql, order_id)
        if not order:
            raise OrderNotFoundException("Order not found")
        order.set(**update_order_request_dto.to_dict())
        order.update()
        return order'''

    def delete_order(self, order_id):
        raise Exception("Not implemented, orders cannot be deleted, only updated and created")