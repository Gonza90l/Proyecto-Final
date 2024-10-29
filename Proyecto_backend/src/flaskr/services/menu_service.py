from flaskr.models.menu import Menu
from flaskr.exceptions.menu_service_exceptions import MenuNotFoundException
from flaskr.dtos.create_menu_request_dto import CreateMenuRequestDTO

class MenuService:

    def __init__(self, mysql):
        self._mysql = mysql

    def get_menus(self):
        menu = Menu(self._mysql)
        menus = menu.find_all()
        return menus

    def get_menu(self, id):
        menu = Menu(self._mysql)
        if not menu.find_by_id(id):
            raise MenuNotFoundException(f"Menu with id {id} not found")
        return menu

    def create_menu(self, create_menu_request_dto: CreateMenuRequestDTO):
        
        menu = Menu(self._mysql)
        #mapeamos el dto a los campos del modelo
        menu.from_dto(create_menu_request_dto)
        cosnsole.log("menu", menu)
        menu.insert()
        return menu

    def update_menu(self, id, data):
        menu = Menu(self._mysql)
        if not menu.find_by_id(id):
            raise MenuNotFoundException(f"Menu with id {id} not found")
        menu.update(data)
        return menu

    def delete_menu(self, id):
        menu = Menu(self._mysql)
        if not menu.find_by_id(id):
            raise MenuNotFoundException(f"Menu with id {id} not found")
        menu.delete()
        return menu