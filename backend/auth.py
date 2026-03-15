import jwt
from flask import request
from services.config_service import config_service

SECRET = config_service.get("JWT_SECRET")

if not SECRET:
    # During development, we can warn, but in production this should be a hard error
    if config_service.get("FLASK_ENV") != "development":
        raise RuntimeError("JWT_SECRET environment variable is missing!")
    SECRET = "temporary-dev-secret-key" # Fallback ONLY for dev if absolutely necessary

def get_user_id():
    auth = request.headers.get("Authorization")

    if not auth:
        return None

    try:
        token = auth.split(" ")[1]

        decoded = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"]
        )

        return decoded["userId"]

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None
