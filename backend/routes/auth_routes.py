from flask import Blueprint, request, jsonify, make_response
from core.container import auth_service
import logging

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.

    Request body (JSON): ``{ name, email, password }``

    Returns:
        201 with user info, or 400/500 on failure.
        Session token is delivered via the ``X-Session-Id`` response header.
    """
    data = request.get_json()
    email = data.get("email")
    logger.info(f"Registration attempt for: {email}")

    result, status = auth_service.register(data)

    if status == 201:
        logger.info(f"User registered: {email}")
        response = make_response(
            jsonify({"message": result["message"], "user": result["user"]}), 201
        )
        response.headers["X-Session-Id"] = result["session_id"]
        return response

    logger.warning(f"Registration failed for {email}: {result.get('error')}")
    return jsonify(result), status


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate an existing user.

    Request body (JSON): ``{ email, password }``

    Returns:
        200 with user info, or 400/401 on failure.
        Session token is delivered via the ``X-Session-Id`` response header.
    """
    data = request.get_json()
    email = data.get("email")
    logger.info(f"Login attempt for: {email}")

    result, status = auth_service.login(data)

    if status == 200:
        logger.info(f"Login successful: {email}")
        response = make_response(
            jsonify({"message": result["message"], "user": result["user"]}), 200
        )
        response.headers["X-Session-Id"] = result["session_id"]
        return response

    logger.warning(f"Login failed for {email}: {result.get('error')}")
    return jsonify(result), status
