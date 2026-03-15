from flask import Blueprint, request, jsonify, make_response
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
import logging

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)
user_repo = UserRepository()
auth_service = AuthService(user_repo)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    logger.info(f"Registration attempt for email: {email}")
    result, status = auth_service.register(data)
    
    if status == 201:
        logger.info(f"User registered successfully: {email}")
        response = make_response(jsonify({
            "message": result["message"],
            "user": result["user"]
        }), 201)
        response.headers["X-Session-Id"] = result["session_id"]
        return response
    
    logger.warning(f"Registration failed for {email}: {result.get('error')}")
    return jsonify(result), status

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    logger.info(f"Login attempt for email: {email}")
    result, status = auth_service.login(data)
    
    if status == 200:
        logger.info(f"Login successful for user: {email}")
        response = make_response(jsonify({
            "message": result["message"],
            "user": result["user"]
        }), 200)
        response.headers["X-Session-Id"] = result["session_id"]
        return response
        
    logger.warning(f"Login failed for {email}: {result.get('error')}")
    return jsonify(result), status
