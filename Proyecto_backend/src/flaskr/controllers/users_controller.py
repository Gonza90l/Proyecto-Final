from flaskr.controllers.base_controller import BaseController
from flaskr.services.users_service import UsersService
from flaskr.dtos.login_request_dto import LoginRequestDTO
from flaskr.dtos.login_response_dto import LoginResponseDTO
from flaskr.auth import token_required, role_required
from injector import inject

class UsersController(BaseController):
    @inject
    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    @token_required
    @role_required('ADMIN')
    def get_users(self):
        users = self.users_service.get_users()
        #armamos el dto de respuesta
        users_dto = [user.to_json_dto() for user in users]
        return self.respond_success(data=users_dto)


    @token_required
    def get_user(self, user_id):
        user = self.users_service.get_user(user_id)
        if user:
            return self.respond_success(data=user.to_json_dto())
        return self.respond_error(message="User not found", status_code=404)


    @token_required
    def create_user(self):
        data = self.get_json_data()
        user = self.users_service.create_user(data)
        #retornamos el dto de respuesta
        user_dto = user.to_json_dto()
        return self.respond_success(data=user_dto)
        

    @token_required
    def delete_user(self, user_id):
        user = self.users_service.delete_user(user_id)
        #respondemos con 200 OK
        return self.respond_success(data=user)

    # login
    def login(self):
        try:
            data = self.get_json_data()
            login_request, errors = LoginRequestDTO.from_json(data)

            if errors:
                return self.respond_error(message="Validation errors", errors=errors, status_code=422)

            token = self.users_service.login(login_request)

            if not token:
                return self.respond_error(message="Invalid credentials", status_code=401)

            response = LoginResponseDTO(token=token)
            return self.respond_success(data=response.to_json())

        except Exception as e:
            return self.respond_error(message="An unexpected error occurred", errors=str(e), status_code=500)
        # verify-token
        @token_required
        def verify_token(self):
            return self.respond_success(data={'message': 'Token is valid'})
