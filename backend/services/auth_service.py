from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from services.config_service import config_service

class AuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo
        self.secret = config_service.get("JWT_SECRET", "temporary-dev-secret-key")

    def _generate_token(self, user_id):
        payload = {
            "userId": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def register(self, data):
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return {"error": "All fields are required"}, 400

        if self.user_repo.get_by_email(email):
            return {"error": "User already exists"}, 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user_id = self.user_repo.create(name, email, hashed_password)

        if not user_id:
            return {"error": "Registration failed"}, 500

        token = self._generate_token(user_id)
        return {
            "message": "User registered successfully",
            "session_id": token,
            "user": {
                "id": user_id,
                "name": name,
                "email": email
            }
        }, 201

    def login(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"error": "Email and password required"}, 400

        user = self.user_repo.get_by_email(email)
        if user and check_password_hash(user["password"], password):
            token = self._generate_token(user["id"])
            return {
                "message": "Login successful",
                "session_id": token,
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"]
                }
            }, 200

        return {"error": "Invalid credentials"}, 401

    def get_user_id_by_session(self, token):
        if not token:
            return None
        try:
            decoded = jwt.decode(token, self.secret, algorithms=["HS256"])
            return decoded["userId"]
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
