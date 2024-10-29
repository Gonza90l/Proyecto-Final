from flask_injector import inject
from flaskr.controllers.base_controller import BaseController
from flaskr.services.menu_service import MenuService
from flaskr.auth import token_required, role_required

from flaskr.dtos.create_category_request_dto import CreateCategoryRequestDTO
from flaskr.dtos.update_category_request_dto import UpdateCategoryRequestDTO
from flaskr.exceptions.menu_service_exceptions import CategoryNotFoundException


class MenuCategoryController(BaseController):
    @inject
    def __init__(self, menu_service: MenuService):
        self._menu_service = menu_service

    @token_required
    def get_categories(self):
        try:
            categories = self._menu_service.get_categories()
            json_categories = [category.to_dict_dto() for category in categories]
            return self.respond_success(data=json_categories)
        except Exception as e:
            return self.respond_error(message=str(e))

    @token_required
    def get_category(self, id):
        try:
            category = self._menu_service.get_category(id)
            return self.respond_success(data=category.to_dict_dto())
        except CategoryNotFoundException as e:
            return self.respond_error(message=str(e), status_code=404)
        except Exception as e:
            return self.respond_error(message=str(e))

    @role_required('ADMIN')
    def create_category(self):
        data = self.get_json_data()

        create_category_request_dto, errors = CreateCategoryRequestDTO.from_json(data)
        if errors:
            return self.respond_error(message="Validation errors", errors=errors, status_code=422)
        try:
            category = self._menu_service.create_category(create_category_request_dto)
            return self.respond_success(data=category.to_dict_dto())
        except ValueError as e:
            return self.respond_error(message=f"Invalid DTO format: {str(e)}", status_code=400)
        except Exception as e:
            return self.respond_error(message=str(e))


    @role_required('ADMIN')
    def update_category(self, id):
        data = self.get_json_data()
        update_category_request_dto, errors = UpdateCategoryRequestDTO.from_json(data)
        if errors:
            return self.respond_error(message="Validation errors", errors=errors, status_code=422)
        
        try:
            category = self._menu_service.update_category(id, update_category_request_dto)
            return self.respond_success(data=category.to_dict_dto())
        except CategoryNotFoundException as e:
            return self.respond_error(message=str(e), status_code=404)
        except Exception as e:
            return self.respond_error(message=str(e))

    @role_required('ADMIN')
    def delete_category(self, id):
        try:
            respond = self._menu_service.delete_category(id)
            return self.respond_success(data = respond)
        except CategoryNotFoundException as e:
            return self.respond_error(message=str(e), status_code=404)
        except Exception as e:
            return self.respond_error(message=str(e))