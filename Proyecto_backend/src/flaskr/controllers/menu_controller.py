from app.controllers.base_controller import BaseController
from app.services.menu_service import MenuService
from app.auth import token_required
from injector import inject

class MenuController(BaseController):
    @inject
    def __init__(self, menu_service: MenuService):
        self.menu_service = menu_service

    @token_required
    def get_menu(self):
        menu = self.menu_service.get_menu()
        return self.respond_success(data=menu)

    @token_required
    def get_item(self, item_id):
        item = self.menu_service.get_item(item_id)
        return self.respond_success(data=item)

    @token_required
    def get_items_by_category(self, category_id):
        items = self.menu_service.get_items_by_category(category_id)
        return self.respond_success(data=items)

    @token_required
    def get_categories(self):
        categories = self.menu_service.get_categories()
        return self.respond_success(data=categories)

