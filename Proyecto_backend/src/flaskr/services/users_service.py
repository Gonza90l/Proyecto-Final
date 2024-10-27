from flaskr.dtos.dtos import RegisterDTO, UpdateUserDTO
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app, jsonify
import jwt
from datetime import datetime, timedelta
from flaskr.auth import decode_and_cache_token  # Importar la función decode_and_cache_token

class UsersService:
    def __init__(self, mysql):
        self.mysql = mysql

    def register(self, register_dto: RegisterDTO):
        # validamos el DTO
        errors = register_dto.validate()
        if errors:
            raise Exception(f"Validation errors: {errors}")

        # intentamos convertir el DTO a un objeto de la base de datos
        user = User()
        try:
            user.from_json_dto(register_dto)
        except Exception as e:
            raise Exception(f"Error converting DTO to database object: {e}")

        # buscamos si no existe un usuario con el mismo email usando mysql
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (user.email,))
        user_exists = cur.fetchone()  # traemos un solo resultado
        cur.close()

        # si el usuario ya existe, lanzamos una excepcion
        if user_exists:
            raise Exception("User with this email already exists")

        # el password lo debemos hashear ya que no se debe guardar en texto plano
        user.password = generate_password_hash(user.password)

        # intentamos guardar el objeto en la base de datos
        try:
            # podemos usar la funcion save implementada en el modelo
            # user.save()
            # pero usamos mysql raw para no ser pythonico y usar el SQL directamente
            cur = self.mysql.connection.cursor()
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (user.name, user.email, user.password))
            self.mysql.connection.commit()
            cur.close()
        except Exception as e:
            raise Exception(f"Error saving user to database: {e}")
        
        return user

    def update_user(self, user_id, update_user_dto: UpdateUserDTO):
        # validamos el DTO
        errors = update_user_dto.validate()
        if errors:
            raise Exception(f"Validation errors: {errors}")

        # intentamos convertir el DTO a un objeto de la base de datos
        user = User()
        try:
            user.from_json_dto(update_user_dto)
        except Exception as e:
            raise Exception(f"Error converting DTO to database object: {e}")

        # intentamos guardar el objeto en la base de datos
        try:
            # podemos usar la funcion save implementada en el modelo
            # user.save()
            # pero usamos mysql raw para no ser pythonico y usar el SQL directamente
            cur = self.mysql.connection.cursor()
            cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (user.name, user.email, user_id))
            self.mysql.connection.commit()
            cur.close()
        except Exception as e:
            raise Exception(f"Error saving user to database: {e}")
        
        return user

    def get_user(self, user_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        return user

    def get_users(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()

        return users

    def delete_user(self, user_id):
        cur = self.mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        self.mysql.connection.commit()
        cur.close()

        return True

    def get_user_by_email(self, email):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        return user

    def login(self, email, password):
        # Buscamos si existe un usuario con el mismo email usando MySQL
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['password'], password):
            # Generar el token JWT incluyendo el campo 'rol'
            token = jwt.encode({
                'id': user['id'],
                'rol': user['rol'],  # Agregar el campo 'rol' al token
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
        cur.execute("SELECT role FROM users WHERE id = %s", (user_id,))
        role = cur.fetchone()
        cur.close()

        return role