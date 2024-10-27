from flask import Blueprint
from flaskr.controllers.controller import ExampleController
from flaskr.controllers.users_controller import UsersController
from injector import inject

main = Blueprint('main', __name__)

@main.route('/example', methods=['GET'])
@inject
def example_route(example_controller: ExampleController):
    return example_controller.handle_request()

#rutas de registro y login
@main.route('/users', methods=['POST'])
@inject
def register_route(users_controller: UsersController):
    return users_controller.register()

@main.route('/login', methods=['POST'])
@inject
def login_route(users_controller: UsersController):
    return users_controller.login()

#rutas de usuarios
@main.route('/users', methods=['GET'])
@inject
def get_users_route(users_controller: UsersController):
    return users_controller.get_users()
    