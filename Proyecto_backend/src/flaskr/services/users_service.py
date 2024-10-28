from flaskr.models.user import User
from flaskr.dtos.register_dto import  RegisterDTO
from flaskr.dtos.update_user_dto import UpdateUserDTO
from flaskr.dtos.login_request_dto import LoginRequestDTO
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
import jwt
from datetime import datetime, timedelta

class UsersService:
    USER_ROL = 'USER'
    ADMIN_ROL = 'ADMIN'

    def __init__(self, mysql):
        self.mysql = mysql

    def register(self, register_dto: RegisterDTO):
        errors = register_dto.validate()
        if errors:
            raise Exception(f"Validation errors: {errors}")
        
        user = User(self.mysql)
        user.set(**register_dto.to_dict())
        user.password = generate_password_hash(user.password)
        user.role = self.USER_ROL

        if user.find_by_email(user.email):
            raise Exception("User with this email already exists")

        user.insert()
        return user

    def update_user(self, user_id, update_user_dto: UpdateUserDTO, current_user_id):
        errors = update_user_dto.validate()
        if errors:
            raise Exception(f"Validation errors: {errors}")

        if not self.has_permission(current_user_id, user_id):
            raise Exception("No permission to update this user")

        user = User(self.mysql)
        if not user.find_by_id(user_id):
            raise Exception("User does not exist")

        user.set(**update_user_dto.to_dict())
        user.update()
        return user

    def get_user(self, user_id):
        user = User(self.mysql)
        if user.find_by_id(user_id):
            return user
        return None

    def get_users(self):
        user = User(self.mysql)
        users = user.find_all()
        return [u.to_json_dto() for u in users]

    def delete_user(self, user_id, current_user_id):
        if not self.has_permission(current_user_id, user_id):
            raise Exception("No permission to delete this user")

        user = User(self.mysql)
        if user.find_by_id(user_id):
            user.deleted_flag = 1
            user.update()
            return True
        return False

    def login(self, login_request_dto: LoginRequestDTO):
        errors = login_request_dto.validate()
        if errors:
            raise Exception(f"Validation errors: {errors}")

        email = login_request_dto.email
        password = login_request_dto.password

        #encodeamos la contraseña
        #hacemos un print de la contraseña encriptada
        print(generate_password_hash(password))

        user = User(self.mysql)
        if user.find_by_email(email) and check_password_hash(user.password, password):
            secret_key = app.config.get('SECRET_KEY')
            if not secret_key or not isinstance(secret_key, str):
                raise Exception("SECRET_KEY is not set or is not a string")

            token = jwt.encode({
                'id': user.id,
                'rol': user.role,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, secret_key, algorithm='HS256')
            print("login",token)
            return token
        return None

    def get_user_by_token(self, token):
        data, _, _ = decode_and_cache_token()
        if data:
            return self.get_user(data['id'])
        return None

    def has_permission(self, current_user_id, target_user_id):
        user = User(self.mysql)
        current_user = user.find_by_id(current_user_id)
        return current_user and (current_user.role == self.ADMIN_ROL or current_user_id == target_user_id)
