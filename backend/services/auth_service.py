from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class AuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo
        self.sessions = {}

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

        session_id = str(uuid.uuid4())
        self.sessions[session_id] = user_id
        return {"message": "User registered successfully", "session_id": session_id, "user_id": user_id}, 201

    def login(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"error": "Email and password required"}, 400

        user = self.user_repo.get_by_email(email)
        if user and check_password_hash(user["password"], password):
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = user["id"]
            return {
                "message": "Login successful",
                "session_id": session_id,
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"]
                }
            }, 200

        return {"error": "Invalid credentials"}, 401
