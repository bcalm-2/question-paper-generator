import jwt
from flask import request

SECRET = "question-generator-secret-key"

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
