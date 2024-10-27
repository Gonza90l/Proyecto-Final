from flaskr.controllers.base_controller import BaseController
from flaskr.services.users_service import UsersService
from flaskr.auth import token_required
from injector import inject

class UsersController(BaseController):
    @inject
    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    @token_required
    def get_users(self):
        users = self.users_service.get_users()
        return self.respond_success(data=users)

    @token_required
    def get_user(self, user_id):
        user = self.users_service.get_user(user_id)
        return self.respond_success(data=user)

    @token_required
    def create_user(self):
        data = self.get_json_data()
        user = self.users_service.create_user(data)
        return self.respond_success(data=user)

    @token_required
    def delete_user(self, user_id):
        user = self.users_service.delete_user(user_id)
        return self.respond_success(data=user)