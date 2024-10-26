from flask import Blueprint
from flaskr.controllers.controller import ExampleController, UserController
from injector import inject

main = Blueprint('main', __name__)

@main.route('/example', methods=['POST'])
@inject
def example_route(example_controller: ExampleController):
    return example_controller.handle_request()

@main.route('/user/<int:user_id>', methods=['GET'])
@inject
def get_user(user_id, user_controller: UserController):
    return user_controller.get_user(user_id)