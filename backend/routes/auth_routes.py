from flask import Blueprint, request, jsonify, make_response
from services.auth_service import AuthService
from repositories.user_repository import UserRepository

auth_bp = Blueprint('auth', __name__)
user_repo = UserRepository()
auth_service = AuthService(user_repo)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    result, status = auth_service.register(data)
    
    if status == 201:
        response = make_response(jsonify({"message": result["message"]}), 201)
        response.headers["X-Session-Id"] = result["session_id"]
        return response
    
    return jsonify(result), status

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    result, status = auth_service.login(data)
    
    if status == 200:
        response = make_response(jsonify({
            "message": result["message"],
            "user": result["user"]
        }), 200)
        response.headers["X-Session-Id"] = result["session_id"]
        return response
        
    return jsonify(result), status
