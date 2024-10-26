from app.controllers.base_controller import BaseController
from app.services.register_service import RegisterService
from app.dtos.dtos import RegisterDTO
from injector import inject

class RegisterController(BaseController):
    @inject
    def __init__(self, register_service: RegisterService):
        self.register_service = register_service

    def register(self):
        register_dto = RegisterDTO(**self.get_json_data())
        user = self.register_service.register(register_dto)
        return self.respond_success(data=user)
