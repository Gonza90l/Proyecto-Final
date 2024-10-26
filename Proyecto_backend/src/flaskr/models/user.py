from .base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    def create_user(self, username, email, password):
        password_hash = generate_password_hash(password)
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        self.execute_query(query, (username, email, password_hash))

    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        return self.fetch_one(query, (username,))

    def check_password(self, stored_password_hash, provided_password):
        return check_password_hash(stored_password_hash, provided_password)