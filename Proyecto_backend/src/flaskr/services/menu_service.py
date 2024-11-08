from flaskr.models.menu import Menu
from flaskr.exceptions.menu_service_exceptions import MenuNotFoundException
from flaskr.exceptions.menu_service_exceptions import CategoryNotFoundException
from flaskr.dtos.create_menu_request_dto import CreateMenuRequestDTO
from flaskr.dtos.update_menu_request_dto import UpdateMenuRequestDTO
from flaskr.dtos.create_category_request_dto import CreateCategoryRequestDTO
from flaskr.dtos.update_category_request_dto import UpdateCategoryRequestDTO
from flask_injector import inject
from flaskr.database.database_interface import IDatabase
from flaskr.models.category import Category


class MenuService:

    @inject
    def __init__(self, mysql: IDatabase):
        self._mysql = mysql

    def get_menus(self):
        menus = Menu.find_all(self._mysql)
        return menus

    def get_menu(self, id):
        menu = Menu.find_by_id(self._mysql, id)
        if not menu:
            raise MenuNotFoundException(f"Menu with id {id} not found")
        return menu

    def create_menu(self, create_menu_request_dto: CreateMenuRequestDTO):
        menu = Menu(self._mysql)
        menu.from_dto(create_menu_request_dto)

        #si la categoria es cero entonces no buscamos la categoria
        if menu.category_id == 0:
            menu.category_id = None
        else:
            # Verificamos que exista la categoría
            category = Category.find_by_id(self._mysql, menu.category_id)
            if not category:
                raise CategoryNotFoundException(f"Category with id {menu.category_id} not found")

        menu.insert()
        return menu

    def update_menu(self, id, update_menu_request_dto: UpdateMenuRequestDTO):
        # Obtener el menú por su ID
        menu = Menu.find_by_id(self._mysql, id)
        if not menu:
            raise MenuNotFoundException(f"Menu with id {id} not found")

        if update_menu_request_dto.category_id == 0:
            update_menu_request_dto.category_id = None
        
        # Actualizar los campos del menú con los datos proporcionados en dto
        menu.from_dto(update_menu_request_dto)

        # Guardar los cambios en la base de datos
        menu.update()

        return menu

    def delete_menu(self, id):
        menu = Menu.find_by_id(self._mysql, id)
        if not menu:
            raise MenuNotFoundException(f"Menu with id {id} not found")
        menu.delete()
        return True

    def create_category(self, create_category_request_dto: CreateCategoryRequestDTO):
        category = Category()
        category.from_dto(create_category_request_dto)
        category.insert()
        return category

    def update_category(self, id, update_category_request_dto: UpdateCategoryRequestDTO):
        category = Category.find_by_id(self._mysql, id)
        if not category:
            raise CategoryNotFoundException(f"Category with id {id} not found")
        category.from_dto(update_category_request_dto)
        category.update()
        return category

    def delete_category(self, id):
        print("delete_category")
        category = Category.find_by_id(self._mysql, id)
        if not category:
            raise CategoryNotFoundException(f"Category with id {id} not found")

        connection = self._mysql.connection
        cursor = connection.cursor()
        try:
            # Iniciamos una transacción
            connection.begin()

            # Quitamos la categoría de los ítems del menú
            cursor.execute(
                "UPDATE menu SET category_id = NULL WHERE category_id = %s",
                (id,)
            )

            # Eliminamos la categoría
            cursor.execute(
                "DELETE FROM category WHERE id = %s",
                (id,)
            )

            # Commit a la transacción
            connection.commit()
        except Exception as e:
            # Rollback en caso de error
            connection.rollback()
            print(e)
            return False
        finally:
            # Cerramos el cursor
            cursor.close()
        return True

    def get_categories(self):
        categories = Category.find_all(self._mysql)
        return categories

    def get_category(self, id):
        category = Category.find_by_id(self._mysql, id)
        if not category:
            raise CategoryNotFoundException(f"Category with id {id} not found")
        return category