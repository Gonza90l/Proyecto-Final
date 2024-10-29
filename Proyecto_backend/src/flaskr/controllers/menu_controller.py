from flask_injector import inject
from flaskr.controllers.base_controller import BaseController
from flaskr.services.menu_service import MenuService

class MenuController(BaseController):
    @inject
    def __init__(self, menu_service: MenuService):
        self._menu_service = menu_service

    def get_menus(self):
        menus = self._menu_service.get_menus()
        #menus es una lsita asique lo recorremos conviertiendo en json_dto
        json_menus = [menu.to_dict_dto() for menu in menus]
        #serializamos la lista de json
        return self.respond_success(data=json_menus)
