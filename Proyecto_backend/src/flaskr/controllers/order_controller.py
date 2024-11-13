from flaskr.controllers.base_controller import BaseController
from flask_injector import inject
from flaskr.services.orders_service import OrderService
from flaskr.auth import token_required
from flaskr.dtos.create_order_request_dto import CreateOrderRequestDTO
from flaskr.auth import get_user_id, get_user_role

from flaskr.exceptions.order_service_exceptions import OrderNotFoundException

class OrderController(BaseController):

    @inject
    def __init__(self, order_service: OrderService):
        self._order_service = order_service

    @token_required
    def get_orders(self):
        try:
            orders = self._order_service.get_orders()

            # Filtramos las ordenes por el usuario que hizo la petición, si es admin mostramos todo
            user_role = get_user_role()
            if user_role == "USER":
                user_id = get_user_id()
                orders = [order for order in orders if order.user_id == user_id]

            # orders es una lista así que lo recorremos convirtiendo en json_dto
            json_orders = [order.to_dict_dto() for order in orders]
            # serializamos la lista de json
            return self.respond_success(data=json_orders)
        except Exception as e:
            return self.respond_error(message=str(e))


    @token_required
    def get_order(self, id):
        try:
            user_role = get_user_role()
            if user_role == "user":
                user_id = get_user_id()
                order = self._order_service.get_order(id)
                if order.user_id != user_id:
                    return self.respond_error(message="You do not have permission to access this resource", status_code=403)
            
            order = self._order_service.get_order(id)
            return self.respond_success(data=order.to_dict_dto())
        except OrderNotFoundException as e:
            return self.respond_error(message=str(e), status_code=404)
        except Exception as e:
           return self.respond_error(message=str(e))

    @token_required
    def create_order(self):
        data = self.get_json_data()

        create_order_request_dto, errors = CreateOrderRequestDTO.from_json(data)
        if errors:
            return self.respond_error(message="Validation errors", errors=errors, status_code=422)
        try:
            order_id = self._order_service.create_order(create_order_request_dto)
            return self.respond_success(data=order_id)
        except ValueError as e:
            return self.respond_error(message=f"Invalid DTO format: {str(e)}", status_code=400)
        except Exception as e:
           return self.respond_error(message=str(e))

    @token_required
    def update_order(self, id):

        #si es admin puede editar todo, si es user solo si le pertenece
        user_role = get_user_role()
        if user_role == "user":
            user_id = get_user_id()
            order = self._order_service.get_order(id)
            if order.user_id != user_id:
                return self.respond_error(message="You do not have permission to access this resource", status_code=403)

        data = self.get_json_data()
        create_order_request_dto, errors = CreateOrderRequestDTO.from_json(data)
        if errors:
            return self.respond_error(message="Validation errors", errors=errors, status_code=422)
        try:
            order = self._order_service.update_order(id, create_order_request_dto)
            return self.respond_success()
        except OrderNotFoundException as e:
            return self.respond_error(message=str(e), status_code=404)
        except Exception as e:
            return self.respond_error(message=str(e))

    @token_required
    def delete_order(self, id):
        #notificamos que no se pueden eliminar ordenes
        return self.respond_error(message="Orders cannot be deleted, only updated and created", status_code=400)
