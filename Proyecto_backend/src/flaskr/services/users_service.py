from flaskr.models.user import User
from flaskr.dtos.register_request_dto import RegisterRequestDTO
from flaskr.dtos.update_user_dto import UpdateUserDTO
from flaskr.dtos.login_request_dto import LoginRequestDTO
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.exceptions.user_service_exceptions import UserAlreadyExistsException

from flask import current_app as app
import jwt
from datetime import datetime, timedelta
from flask_injector import inject
from flaskr.database.database_interface import IDatabase



class UsersService:
    USER_ROL = 'USER'
    ADMIN_ROL = 'ADMIN'

    @inject
    def __init__(self, mysql: IDatabase):
        self._mysql = mysql

    def register(self, register_dto: RegisterRequestDTO):
        # Convertimos el dto a modelo
        user = User(self._mysql)
        # Mapeamos el dto a los campos del modelo
        user.from_dto(register_dto)

        # Verificamos si el usuario ya existe
        if User.find_by_email(self._mysql, user.email):
            raise UserAlreadyExistsException("User already exists")

        # Encriptamos la contraseña
        user.password = generate_password_hash(user.password)
        # Guardamos el usuario
        user.insert()

        print("ROL", user.role)

        return user

    def update_user(self, user_id, update_user_dto: UpdateUserDTO, current_user_id):
        errors = update_user_dto.validate()
        if errors:
            raise Exception(f"Validation errors: {errors}")

        if not self.has_permission(current_user_id, user_id):
            raise Exception("No permission to update this user")

        user = User.find_by_id(self._mysql, user_id)
        if not user:
            raise Exception("User does not exist")

        #verificamos que el nuevo email no este en uso
        if update_user_dto.email != user.email and User.find_by_email(self._mysql, update_user_dto.email):
            raise Exception("Email already in use")

        # Encriptamos la contraseña
        user.password = generate_password_hash(user.password)

        # Actualizamos los campos del usuario
        user.set(**update_user_dto.to_dict())
        # Guardamos los cambios
        user.update()
        return user

    def get_user(self, user_id):
        return User.find_by_id(self._mysql, user_id)

    def get_users(self):
        users = User.find_all(self._mysql)
        return [u.to_dict_dto() for u in users]

    def delete_user(self, user_id, current_user_id):
        if not self.has_permission(current_user_id, user_id):
            raise Exception("No permission to delete this user")

        user = User.find_by_id(self._mysql, user_id)
        if user:
            user.deleted_flag = 1
            user.update()
            return True
        return False

    def login(self, login_request_dto: LoginRequestDTO):
        email = login_request_dto.email
        password = login_request_dto.password

        # Encodeamos la contraseña
        print(generate_password_hash(password))

        user = User.find_by_email(self._mysql, email)
        if user and check_password_hash(user.password, password):
            secret_key = app.config.get('SECRET_KEY')
            if not secret_key or not isinstance(secret_key, str):
                raise Exception("SECRET_KEY is not set or is not a string")

            token = jwt.encode({
                'id': user.id,
                'role': user.role,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, secret_key, algorithm='HS256')
            print("login", token)
            return token
        return None

    def get_user_by_token(self, token):
        data, _, _ = decode_and_cache_token()
        if data:
            return self.get_user(data['id'])
        return None

    def has_permission(self, current_user_id, target_user_id):
        current_user = User.find_by_id(self._mysql, current_user_id)
        return current_user and (current_user.role == self.ADMIN_ROL or current_user_id == target_user_id)