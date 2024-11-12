from flask_injector import inject
from flaskr.services.orders_service import OrderService
from flaskr.controllers.base_controller import BaseController

class ipnController(BaseController):
    @inject
    def __init__(self, order_service: OrderService):
        self._order_service = order_service

    def post(self):
        #obtenemos el post desde la solicitud
        post = self.get_json_data()

        # Verificamos si el post contiene el order_id
        order_id = post.get('orderId')
        if not order_id:
            return self.respond_error(message="order_id no proporcionado")

        #determinamos si hay una orden con el id proporcionado
        order = self._order_service.get_order(order_id)

        if order:
            #llamamo sal servicio de ordenes para hacer un update
            self._order_service.processPayment(order.id)

        return self.respond_success(data="IPN received.")


        
        
