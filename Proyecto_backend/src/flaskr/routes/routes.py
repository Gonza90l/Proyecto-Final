from flask import Blueprint
from flaskr.controllers.users_controller import UsersController
from flaskr.controllers.menu_controller import MenuController
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

# Rutas para obtener menús

@main.route('/menus', methods=['GET'])
@inject
def get_menus(menu_controller: MenuController):
    return menu_controller.get_menus()

@main.route('/menus/<int:menu_id>', methods=['GET'])
@inject
def get_menu(menu_controller: MenuController, menu_id):
    return menu_controller.get_menu(menu_id)

@main.route('/menus', methods=['POST'])
@inject
def create_menu(menu_controller: MenuController):
    return menu_controller.create_menu()
    