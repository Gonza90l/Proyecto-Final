from flask_injector import inject
from flaskr.services.order_service import OrderService

class ipnController(BaseController):
    @inject
    def __init__(self, order_service: OrderService):
        self._order_service = order_service

    def post(self):
        #obtenemos el post desde la solicitud
        post = self.get_json_data()

        #determinamos si hay una orden con el id proporcionado
        order_id = post.get('order_id')
        order = self._order_service.get_order(order_id)

        if order:
            #llamamo sal servicio de ordenes para hacer un update
            self._order_service.processPayment(order.id)

        return self.respond_success(data="IPN received.")


        
        
