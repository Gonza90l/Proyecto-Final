from flaskr.controllers.base_controller import BaseController
from flaskr.services.users_service import UsersService
from flaskr.dtos.login_request_dto import LoginRequestDTO
from flaskr.dtos.login_response_dto import LoginResponseDTO
from flaskr.dtos.register_request_dto import RegisterRequestDTO
from flaskr.dtos.user_dto import UserDTO
from flaskr.auth import token_required, role_required
from flaskr.exceptions.user_service_exceptions import UserAlreadyExistsException
from flask_injector import inject

class UsersController(BaseController):
    @inject
    def __init__(self, users_service: UsersService):
        """
        Constructor de la clase UsersController.
        
        :param users_service: Servicio de usuarios inyectado.
        """
        self.users_service = users_service

    @token_required
    @role_required('ADMIN')
    def get_users(self):
        """
        Obtiene todos los usuarios.

        :return: Respuesta JSON con la lista de usuarios.
        """
        users = self.users_service.get_users()
        users_dto = [user.to_dict_dto() for user in users]
        return self.respond_success(data=users_dto)

    @token_required
    def get_user(self, user_id):
        """
        Obtiene un usuario específico por su ID.

        :param user_id: ID del usuario.
        :return: Respuesta JSON con los datos del usuario.
        """
        user = self.users_service.get_user(user_id)
        if user:
            return self.respond_success(data=user.to_dict_dto())
        return self.respond_error(message="User not found", status_code=404)

    @token_required
    def create_user(self):
        """
        Crea un nuevo usuario.

        :return: Respuesta JSON con los datos del usuario creado.
        """
        data = self.get_json_data()
        user = self.users_service.create_user(data)
        user_dto = user.to_dict_dto()
        return self.respond_success(data=user_dto)

    @token_required
    def delete_user(self, user_id):
        """
        Elimina un usuario por su ID.

        :param user_id: ID del usuario.
        :return: Respuesta JSON con el resultado de la operación.
        """
        user = self.users_service.delete_user(user_id)
        return self.respond_success(data=user)

    def login(self):
        """
        Inicia sesión de un usuario.

        :return: Respuesta JSON con el token de autenticación.
        """
        data = self.get_json_data()
        login_request, errors = LoginRequestDTO.from_json(data)

        if errors:
            return self.respond_error(message="Validation errors", errors=errors, status_code=422)

        token = self.users_service.login(login_request)

        if not token:
            return self.respond_error(message="Invalid credentials", status_code=401)

        response = LoginResponseDTO(token=token)
        return self.respond_success(data=response.to_json())

    def register(self):
        """
        Registra un nuevo usuario.

        :return: Respuesta JSON con los datos del usuario registrado.
        """
        data = self.get_json_data()
        try:
            register_request, errors = RegisterRequestDTO.from_json(data)

            if errors:
                return self.respond_error(message="Validation errors", errors=errors, status_code=422)

            user = self.users_service.register(register_request)

            if not user:
                return self.respond_error(message="Registration failed", status_code=400)

            return self.respond_success(data=user.to_dict_dto())    

        except UserAlreadyExistsException as e:
            return self.respond_error(message="User already exists", status_code=400)

        except Exception as e:
            return self.respond_error(message="An unexpected error occurred", errors=str(e), status_code=500)

    @token_required
    def verify_token(self):
        """
        Verifica la validez del token de autenticación.

        :return: Respuesta JSON indicando que el token es válido.
        """
        return self.respond_success(data={'message': 'Token is valid'})