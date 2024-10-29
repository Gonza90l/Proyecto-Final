from flaskr.models.menu import Menu
from flaskr.exceptions.menu_service_exceptions import MenuNotFoundException
from flaskr.dtos.create_menu_request_dto import CreateMenuRequestDTO
from flaskr.dtos.update_menu_request_dto import UpdateMenuRequestDTO
from flaskr.models.category import Category


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
        menu.from_dto(create_menu_request_dto)

        #verificamos que exista la categoria
        category = Category(self._mysql)
        if not category.find_by_id(menu.category_id):
            raise CategoryNotFoundException(f"Category with id {menu.category_id} not found")

        menu.insert()
        return menu


    def update_menu(self, id, update_menu_request_dto: UpdateMenuRequestDTO):
        # Obtener el menú por su ID
        menu = Menu(self._mysql) #creamos un objeto menu y le pasamos la conexion
        menu.find_by_id(id) #buscamos el obnjeto y cargamos en el objeto menu
        if not menu: #si no existe el menu
            raise MenuNotFoundException(f"Menu with id {id} not found") #lanzamos una excepcion

        # Actualizar los campos del menú con los datos proporcionados en dto
        menu.from_dto(update_menu_request_dto)

        # Guardar los cambios en la base de datos
        menu.update()

        return menu


    def delete_menu(self, id):
        menu = Menu(self._mysql)
        if not menu.find_by_id(id):
            raise MenuNotFoundException(f"Menu with id {id} not found")
        menu.delete()
        return True