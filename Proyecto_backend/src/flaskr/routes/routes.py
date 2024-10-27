from flask import Blueprint
from flaskr.controllers.controller import ExampleController
from flaskr.controllers.users_controller import UsersController
from injector import inject

main = Blueprint('main', __name__)

@main.route('/example', methods=['GET'])
@inject
def example_route(example_controller: ExampleController):
    return example_controller.handle_request()

@main.route('/user/<int:user_id>', methods=['GET'])
@inject
def get_user(user_id, user_controller: UsersController):
    return user_controller.get_user(user_id)