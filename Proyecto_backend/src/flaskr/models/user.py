from .base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from abc import ABC, abstractmethod
from .interfaces import IModel

class IUserModel(IModel):
    '''La interfaz IUserModel define un contrato específico para cualquier clase que implemente un modelo de usuario en la aplicación.
    Hereda de IModel para incluir métodos genéricos y añade métodos específicos del modelo de usuario.'''

    @abstractmethod
    def create_user(self, username, email, password):
        pass

    @abstractmethod
    def get_user_by_username(self, username):
        pass

    @abstractmethod
    def check_password(self, stored_password_hash, provided_password):
        pass

class User(BaseModel, IUserModel):
    def create_user(self, username, email, password):
        password_hash = generate_password_hash(password)
        data = {
            'username': username,
            'email': email,
            'password_hash': password_hash
        }
        self.create(data)

    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        return self.fetch_one(query, (username,))

    def check_password(self, stored_password_hash, provided_password):
        return check_password_hash(stored_password_hash, provided_password)

    def create(self, data):
        self.insert('users', data)

    def get_by_id(self, id):
        return self.find_by_id('users', id)

    def update(self, id, data):
        self.update('users', data, 'id = %s', (id,))

    def delete(self, id):
        self.delete('users', 'id = %s', (id,))

    def get_all(self):
        return self.find_all('users')