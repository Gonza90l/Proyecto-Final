from flaskr.models.menu import Menu
from flaskr.exceptions.menu_service_exceptions import MenuNotFoundException
from flaskr.exceptions.menu_service_exceptions import CategoryNotFoundException
from flaskr.dtos.create_menu_request_dto import CreateMenuRequestDTO
from flaskr.dtos.update_menu_request_dto import UpdateMenuRequestDTO
from flaskr.dtos.create_category_request_dto import CreateCategoryRequestDTO
from flaskr.dtos.update_category_request_dto import UpdateCategoryRequestDTO

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
        if not menu.find_by_id(id):
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

    def create_category(self, create_category_request_dto: CreateCategoryRequestDTO):
        category = Category(self._mysql)
        category.from_dto(create_category_request_dto)
        category.insert()
        return category

    def update_category(self, id, update_category_request_dto: UpdateCategoryRequestDTO):
        category = Category(self._mysql)
        if not category.find_by_id(id):
            raise CategoryNotFoundException(f"Category with id {id} not found")
        category.from_dto(update_category_request_dto)
        category.update()
        return category

    def delete_category(self, id):
        print("delete_category")
        category = Category(self._mysql)
        if not category.find_by_id(id):
            raise CategoryNotFoundException(f"Category with id {id} not found")

        
        connection = self._mysql.get_connection()
        cursor = connection.cursor()
        try:
            # Iniciamos una transaccion
            connection.begin()
            
            # Quitamos la categoria de los items menus
            cursor.execute(
                "UPDATE menu SET category_id = NULL WHERE category_id = %s",
                (id,)
            )

            # Eliminamos la categoria
            cursor.execute(
                "DELETE FROM category WHERE id = %s",
                (id,)
            )
            
            # Commit a la transaccion
            connection.commit()
        except Exception as e:
            # Rollback en caso de error
            connection.rollback()
            print(e)
            return False
        finally:
            # cerramos el cursor
            cursor.close()
        return True

        

    def get_categories(self):
        category = Category(self._mysql)
        categories = category.find_all()
        return categories

    def get_category(self, id):
        category = Category(self._mysql)
        if not category.find_by_id(id):
            raise CategoryNotFoundException(f"Category with id {id} not found")
        return category