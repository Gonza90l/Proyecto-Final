from flask_injector import inject
from flaskr.services.orders_service import OrderService
from flaskr.controllers.base_controller import BaseController

class ipnController(BaseController):
    @inject
    def __init__(self, order_service: OrderService):
        """
        Constructor de la clase ipnController.
        
        :param order_service: Servicio de órdenes inyectado.
        """
        self._order_service = order_service

    def post(self):
        """
        Maneja la recepción de notificaciones IPN (Instant Payment Notification).

        :return: Respuesta JSON con el resultado de la operación.
        """
        try:
            # Obtenemos el post desde la solicitud
            post = self.get_json_data()

            # Verificamos si el post contiene el order_id
            order_id = post.get('orderId')
            if not order_id:
                return self.respond_error(message="order_id no proporcionado")

            # Determinamos si hay una orden con el id proporcionado
            order = self._order_service.get_order(order_id)

            if order:
                # Llamamos al servicio de órdenes para hacer un update
                self._order_service.processPayment(order.id)
                return self.respond_success(data="IPN received.")
            else:
                return self.respond_error(message="Orden no encontrada", status_code=404)
        except ValueError as e:
            return self.respond_error(message=str(e), status_code=400)
        except Exception as e:
            return self.respond_error(message="Error interno del servidor", status_code=500)