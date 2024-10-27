from app.controllers.base_controller import BaseController
from app.services.login_service import LoginService
from app.services.user_service import UserService
from app.dtos.dtos import LoginDTO, RegisterDTO
from app.auth import token_required
from injector import inject

class LoginController(BaseController):
    @inject
    def __init__(self, login_service: LoginService, user_service: UserService):
        self.login_service = login_service
        self.user_service = user_service

    def login(self):
        login_dto = LoginDTO(**self.get_json_data())
        login_response = self.login_service.login(login_dto)
        return self.respond_success(data=login_response)

    def register(self):
        register_dto = RegisterDTO(**self.get_json_data())
        user = self.user_service.register(register_dto)
        return self.respond_success(data=user)

    #verify-token
    @token_required
    def verify_token(self):
        return self.respond_success(data={})

        