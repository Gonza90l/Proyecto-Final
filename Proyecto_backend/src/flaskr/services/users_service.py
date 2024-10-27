from flaskr.dtos.dtos import RegisterDTO, UpdateUserDTO
from flaskr.dtos.user_dto import UserDTO
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app, jsonify
import jwt
from datetime import datetime, timedelta
from flaskr.auth import decode_and_cache_token  # Importar la función decode_and_cache_token

class UsersService:
    # Definimos las constantes
    USER_ROL = 'USER'
    ADMIN_ROL = 'ADMIN'

    def __init__(self, mysql):
        self.mysql = mysql

    def register(self, register_dto: RegisterDTO):
        # Validamos el DTO
        errors = register_dto.validate()
        if errors:
            raise Exception(f"Validation errors: {errors}")

        # Intentamos convertir el DTO a un objeto de la base de datos
        user_data = register_dto.to_dict()
        user_data['password'] = generate_password_hash(user_data['password'])
        user_data['role'] = self.USER_ROL

        # Buscamos si no existe un usuario con el mismo email usando MySQL
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND deleted_flag = 0", (user_data['email'],))
        user_exists = cur.fetchone()
        cur.close()

        if user_exists:
            raise Exception("User with this email already exists")

        # Intentamos guardar el objeto en la base de datos
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("INSERT INTO users (name, email, lastname, role, password) VALUES (%s, %s, %s, %s, %s)", 
                        (user_data['name'], user_data['email'], user_data['lastname'], user_data['role'], user_data['password']))
            self.mysql.connection.commit()
            user_data['id'] = cur.lastrowid
            cur.close()
        except Exception as e:
            raise Exception(f"Error saving user to database: {e}")
        
        return UserDTO(**user_data)

    def update_user(self, user_id, update_user_dto: UpdateUserDTO, current_user_id):
        # Validamos el DTO
        errors = update_user_dto.validate()
        if errors:
            raise Exception(f"Validation errors: {errors}")

        # Verificamos permisos
        if not self.has_permission(current_user_id, user_id):
            raise Exception("You do not have permission to update this user")

        # Intentamos convertir el DTO a un objeto de la base de datos
        user_data = update_user_dto.to_dict()

        # Comprobamos de que el usuario exista
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s AND deleted_flag = 0", (user_id,))
        user_exists = cur.fetchone()
        cur.close()

        if not user_exists:
            raise Exception("User does not exist")

        # Intentamos guardar el objeto en la base de datos
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("UPDATE users SET name = %s, lastname = %s WHERE id = %s", 
                        (user_data['name'], user_data['lastname'], user_id))
            self.mysql.connection.commit()
            cur.close()
        except Exception as e:
            raise Exception(f"Error saving user to database: {e}")
        
        user_data['id'] = user_id
        return UserDTO(**user_data)

    def get_user(self, user_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s AND deleted_flag = 0", (user_id,))
        user = cur.fetchone()
        cur.close()

        if user:
            return UserDTO(**user)
        return None

    def get_users(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE deleted_flag = 0")
        users = cur.fetchall()
        cur.close()

        return [UserDTO(**user) for user in users]

    def delete_user(self, user_id, current_user_id):
        # Verificamos permisos
        if not self.has_permission(current_user_id, user_id):
            raise Exception("You do not have permission to delete this user")

        # Hacemos un soft delete
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("UPDATE users SET deleted_flag = 1 WHERE id = %s", (user_id,))
            self.mysql.connection.commit()
            cur.close()
        except Exception as e:
            raise Exception(f"Error deleting user: {e}")

        return True

    def get_user_by_email(self, email):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND deleted_flag = 0", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            return UserDTO(**user)
        return None

    def login(self, email, password):
        # Buscamos si existe un usuario con el mismo email usando MySQL
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND deleted_flag = 0", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['password'], password):
            # Generar el token JWT incluyendo el campo 'rol'
            token = jwt.encode({
                'id': user['id'],
                'rol': user['role'],  # Agregar el campo 'rol' al token
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['SECRET_KEY'])
            return token
        else:
            return None

    def get_user_by_token(self, token):
        # Utilizar decode_and_cache_token para verificar el token
        data, error_response, status_code = decode_and_cache_token()
        if error_response:
            return None
        user = self.get_user(data['id'])
        return user

    def get_user_role(self, user_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT role FROM users WHERE id = %s AND deleted_flag = 0", (user_id,))
        role = cur.fetchone()
        cur.close()

        return role['role'] if role else None

    def has_permission(self, current_user_id, target_user_id):
        # Verificar si el usuario actual tiene permisos para modificar el usuario objetivo
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT role FROM users WHERE id = %s AND deleted_flag = 0", (current_user_id,))
        current_user = cur.fetchone()
        cur.close()

        if not current_user:
            return False

        # Si el usuario actual es un administrador, tiene permiso
        if current_user['role'] == self.ADMIN_ROL:
            return True

        # Si el usuario actual es el mismo que el usuario objetivo, tiene permiso
        if current_user_id == target_user_id:
            return True

        return False