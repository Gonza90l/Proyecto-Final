
class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, register_dto: RegisterDTO):
        user = User(
            email=register_dto.email,
            password=register_dto.password,
            first_name=register_dto.first_name,
            last_name=register_dto.last_name,
            is_active=True,
            is_admin=False,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        return user

    def get_user_by_id(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        return user

    def update_user(self, user_id: int, update_dto: UpdateUserDTO):
        user = self.get_user_by_id(user_id)
        if user is None:
            return None
        user.email = update_dto.email
        user.first_name = update_dto.first_name
        user.last_name = update_dto.last_name
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user is None:
            return None
        self.db.delete(user)
        self.db.commit()
        return user