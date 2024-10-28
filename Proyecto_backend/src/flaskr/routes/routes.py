from flask import Blueprint
from flaskr.controllers.controller import ExampleController
from flaskr.controllers.users_controller import UsersController
from injector import inject

main = Blueprint('main', __name__)

############################################################################################################
# Rutas para el login, registro y verificación de token

@main.route('/login', methods=['POST'])
@inject
def login(users_controller: UsersController):
    return users_controller.login()

@main.route('/register', methods=['POST'])
@inject
def register(users_controller: UsersController):
    return users_controller.register()

# verificación de token
@main.route('/verify_token', methods=['POST'])
@inject
def verify_token(users_controller: UsersController):
    return users_controller.verify_token()

############################################################################################################

# Rutas para obtener usuarios

@main.route('/users', methods=['GET'])
@inject
def get_users(users_controller: UsersController):
    return users_controller.get_users()

@main.route('/users/<int:user_id>', methods=['GET'])
@inject
def get_user(users_controller: UsersController, user_id):
    return users_controller.get_user(user_id)


############################################################################################################
