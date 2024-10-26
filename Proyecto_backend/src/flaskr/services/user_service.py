from flaskr.repositories.user_repository import UserRepository
from flaskr.dtos.dtos import RegisterDTO, UpdateUserDTO


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, register_dto: RegisterDTO):
        user = self.user_repository.create_user(register_dto)
        return user

    def get_user_by_email(self, email: str):
        user = self.user_repository.get_user_by_email(email)
        return user

    def get_user_by_id(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        return user

    def update_user(self, user_id: int, update_dto: UpdateUserDTO):
        user = self.user_repository.update_user(user_id, update_dto)
        return user

    def delete_user(self, user_id: int):
        user = self.user_repository.delete_user(user_id)
        return user