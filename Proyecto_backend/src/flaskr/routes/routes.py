from flask import Blueprint
from flaskr.controllers.controller import ExampleController, UserController
from injector import inject

main = Blueprint('main', __name__)

@inject
def configure_routes(example_controller: ExampleController, user_controller: UserController):
    @main.route('/example', methods=['POST'])
    def example_route():
        return example_controller.handle_request()

    @main.route('/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        return user_controller.get_user(user_id)

configure_routes()