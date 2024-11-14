from flaskr.controllers.base_controller import BaseController
from flaskr.services.menu_service import MenuService, MenuNotFoundException
from flaskr.auth import token_required, role_required
from flaskr.dtos.create_menu_request_dto import CreateMenuRequestDTO
from flaskr.dtos.update_menu_request_dto import UpdateMenuRequestDTO
from flask_injector import inject

class MenuController(BaseController):
    @inject
    def __init__(self, menu_service: MenuService):
        """
        Constructor de la clase MenuController.
        
        :param menu_service: Servicio de menú inyectado.
        """
        self._menu_service = menu_service

    @token_required
    def get_menus(self):
        """
        Obtiene todos los menús.

        :return: Respuesta JSON con la lista de menús.
        """
        try:
            menus = self._menu_service.get_menus()
            json_menus = [menu.to_dict_dto() for menu in menus]
            return self.respond_success(data=json_menus)
        except Exception as e:
            return self.respond_error(message=str(e))

    @token_required
    def get_menu(self, id):
        """
        Obtiene un menú específico por su ID.

        :param id: ID del menú.
        :return: Respuesta JSON con los datos del menú.
        """
        try:
            menu = self._menu_service.get_menu(id)
            return self.respond_success(data=menu.to_dict_dto())
        except MenuNotFoundException as e:
            return self.respond_error(message=str(e), status_code=404)
        except Exception as e:
            return self.respond_error(message=str(e))

    @role_required('ADMIN')
    def create_menu(self):
        """
        Crea un nuevo menú.

        :return: Respuesta JSON con los datos del menú creado.
        """
        data = self.get_json_data()

        create_menu_request_dto, errors = CreateMenuRequestDTO.from_json(data)
        if errors:
            return self.respond_error(message="Validation errors", errors=errors, status_code=422)
        try:
            menu = self._menu_service.create_menu(create_menu_request_dto)
            return self.respond_success(data=menu.to_dict_dto())
        except ValueError as e:
            return self.respond_error(message=f"Invalid DTO format: {str(e)}", status_code=400)
        except Exception as e:
            return self.respond_error(message=str(e))

    @role_required('ADMIN')
    def update_menu(self, id):
        """
        Actualiza un menú existente.

        :param id: ID del menú a actualizar.
        :return: Respuesta JSON con los datos del menú actualizado.
        """
        data = self.get_json_data()
        update_menu_request_dto, errors = UpdateMenuRequestDTO.from_json(data)
        if errors:
            return self.respond_error(message="Validation errors", errors=errors, status_code=422)
        
        try:
            menu = self._menu_service.update_menu(id, update_menu_request_dto)
            return self.respond_success(data=menu.to_dict_dto())
        except MenuNotFoundException as e:
            return self.respond_error(message=str(e), status_code=404)
        except Exception as e:
            return self.respond_error(message=str(e))

    @role_required('ADMIN')
    def delete_menu(self, id):
        """
        Elimina un menú.

        :param id: ID del menú a eliminar.
        :return: Respuesta JSON con el resultado de la operación.
        """
        try:
            self._menu_service.delete_menu(id)
            return self.respond_success(data="none")
        except MenuNotFoundException as e:
            return self.respond_error(message=str(e), status_code=404)
        except Exception as e:
            return self.respond_error(message=str(e))