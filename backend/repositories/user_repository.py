from .base_repository import BaseRepository

class UserRepository(BaseRepository):
    def get_by_email(self, email):
        result = self.execute_query("SELECT * FROM users WHERE email = %s", (email,))
        return result[0] if result else None

    def create(self, name, email, hashed_password):
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        return self.execute_query(query, (name, email, hashed_password), commit=True)

    def get_by_id(self, user_id):
        result = self.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))
        return result[0] if result else None
