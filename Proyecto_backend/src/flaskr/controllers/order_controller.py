from flaskr.controllers.base_controller import BaseController
from flask_injector import inject
from flaskr.services.orders_service import OrderService
from flaskr.auth import token_required

from flaskr.exceptions.order_service_exceptions import OrderNotFoundException

class OrderController(BaseController):

    @inject
    def __init__(self, order_service: OrderService):
        self._order_service = order_service

    @token_required
    def get_orders(self):
        #try:
        orders = self._order_service.get_orders()
        # orders es una lista así que lo recorremos convirtiendo en json_dto
        json_orders = [order.to_dict_dto() for order in orders]
        # serializamos la lista de json
        return self.respond_success(data=json_orders)
        #except Exception as e:
        #    return self.respond_error(message=str(e))

    @token_required
    def get_order(self, id):
        #try:
            order = self._order_service.get_order(id)
            print(">>>>>>",order)
            return self.respond_success(data=order.to_dict_dto())
        #except OrderNotFoundException as e:
        #    return self.respond_error(message=str(e), status_code=404)
        #except Exception as e:
        #   return self.respond_error(message=str(e))

    @token_required
    def create_order(self):
        data = self.get_json_data()

        create_order_request_dto, errors = CreateOrderRequestDTO.from_json(data)
        if errors:
            return self.respond_error(message="Validation errors", errors=errors, status_code=422)
        try:
            order = self._order_service.create_order(create_order_request_dto)
            return self.respond_success(data=order.to_dict_dto())
        except ValueError as e:
            return self.respond_error(message=f"Invalid DTO format: {str(e)}", status_code=400)
        except Exception as e:
            return self.respond_error(message=str(e))

    @token_required
    def update_order(self, id):
        data = self.get_json_data()
        update_order_request_dto, errors = UpdateOrderRequestDTO.from_json(data)
        if errors:
            return self.respond_error(message="Validation errors", errors=errors, status_code=422)
        
        try:
            order = self._order_service.update_order(id, update_order_request_dto)
            return self.respond_success(data=order.to_dict_dto())
        except OrderNotFoundException as e:
            return self.respond_error(message=str(e), status_code=404)
        except Exception as e:
            return self.respond_error(message=str(e))

    @token_required
    def delete_order(self, id):
        #notificamos que no se pueden eliminar ordenes
        return self.respond_error(message="Orders cannot be deleted, only updated and created", status_code=400)
