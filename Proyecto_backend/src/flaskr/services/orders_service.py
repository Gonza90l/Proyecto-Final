from flask_injector import inject
from flaskr.database.database_interface import IDatabase
from flaskr.models.order import Order
from flaskr.exceptions.order_service_exceptions import OrderNotFoundException
from flaskr.models.order_has_menu import OrderHasMenu
from flaskr.dtos.create_order_request_dto import CreateOrderRequestDTO
from flaskr.dtos.create_order_has_menu_request_dto import CreateOrderHasMenuRequestDTO
from datetime import datetime
from flaskr.auth import get_user_id, get_user_role

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

    def update_order(self, order_id, create_order_request_dto):
        order = Order.find_by_id(self._mysql, order_id)
        if not order:
            raise OrderNotFoundException("Order not found")

        # Obtener el rol del usuario y el ID del usuario
        user_role = get_user_role()  # Asume que esta función obtiene el rol del usuario
        user_id = get_user_id()  # Asume que esta función obtiene el ID del usuario

        # Verificar permisos
        if user_role != 'admin':
            if order.user_id != user_id:
                raise PermissionError("You do not have permission to modify this order")
            
            # Verificar si el usuario puede cancelar el pedido
            if create_order_request_dto.status == 'CANCELED':
                if order.status in ['DELIVERED', 'CANCELED']:
                    raise PermissionError("You cannot cancel an order that is already delivered or canceled")
            
            # Verificar si el usuario puede editar el contenido del pedido
            elif order.status != 'CREATED':
                raise PermissionError("You can only modify orders that are in 'CREATED' status")

            # Verificar que el usuario no esté intentando modificar el contenido del pedido si el estado no es 'CREATED'
            if order.status == 'CREATED' and create_order_request_dto.status != 'CANCELED':
                if create_order_request_dto.order_items != order.order_items:
                    raise PermissionError("You can only modify the content of orders that are in 'CREATED' status")

        # Actualizamos los datos del pedido
        order.from_dto(create_order_request_dto)
        order.status = self._validate_status(create_order_request_dto.status)
        order.update()

        # Obtenemos una conexión y un cursor
        connection = self._mysql.get_connection()
        cursor = self._mysql.get_cursor()

        try:
            # Eliminamos los items existentes del pedido
            delete_query = "DELETE FROM order_has_menu WHERE order_id = %s"
            cursor.execute(delete_query, (order_id,))
            connection.commit()

            # Añadimos los nuevos items del pedido
            insert_query = "INSERT INTO order_has_menu (order_id, menu_id, quantity) VALUES (%s, %s, %s)"
            order_items = create_order_request_dto.order_items
            for item_dto in order_items:
                try:
                    order_item_dto = CreateOrderHasMenuRequestDTO(**item_dto)
                    cursor.execute(insert_query, (order.id, order_item_dto.menu_id, order_item_dto.quantity))
                except ValueError as e:
                    raise ValueError(f"Invalid DTO format for order item: {item_dto}") from e

            connection.commit()
        finally:
            cursor.close()

        return True

    def delete_order(self, order_id):
        raise Exception("Not implemented, orders cannot be deleted, only updated and created")