from flask import Blueprint, request, jsonify
import os
import json
from repositories.subject_repository import SubjectRepository, TopicRepository
from routes.auth_routes import auth_service
import logging

config_bp = Blueprint('config', __name__)
logger = logging.getLogger(__name__)

subject_repo = SubjectRepository()
topic_repo = TopicRepository()

RESOURCE_FOLDER = "resources"
MAPPING_FILE = "mapping.json"

@config_bp.route("/api/admin/subjects", methods=["GET"])
def get_subjects():
    session_id = request.headers.get("X-Session-Id")
    user_id = auth_service.get_user_id_by_session(session_id)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    subjects = subject_repo.get_all()
    for sub in subjects:
        sub['topics'] = topic_repo.get_by_subject(sub['id'])
    
    return jsonify(subjects), 200

@config_bp.route("/api/admin/subjects", methods=["POST"])
def add_subject():
    session_id = request.headers.get("X-Session-Id")
    user_id = auth_service.get_user_id_by_session(session_id)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get("name")
    topics = data.get("topics", [])

    if not name:
        return jsonify({"error": "Name is required"}), 400

    subject_id = subject_repo.create(name)
    for topic_name in topics:
        topic_repo.create(subject_id, topic_name)

    return jsonify({"message": "Subject added successfully", "id": subject_id}), 201

@config_bp.route("/api/admin/subjects/<int:subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    session_id = request.headers.get("X-Session-Id")
    user_id = auth_service.get_user_id_by_session(session_id)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    subject_repo.delete(subject_id)
    return jsonify({"message": "Subject deleted successfully"}), 200

@config_bp.route("/api/admin/files", methods=["GET"])
def list_files():
    session_id = request.headers.get("X-Session-Id")
    user_id = auth_service.get_user_id_by_session(session_id)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if not os.path.exists(RESOURCE_FOLDER):
        return jsonify([]), 200

    files = os.listdir(RESOURCE_FOLDER)
    
    mapping = {}
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r") as f:
            mapping = json.load(f)

    file_list = []
    for f in files:
        file_list.append({
            "name": f,
            "subject": mapping.get(f, "Unassigned")
        })

    return jsonify(file_list), 200

@config_bp.route("/api/admin/files/<filename>", methods=["DELETE"])
def delete_file(filename):
    session_id = request.headers.get("X-Session-Id")
    user_id = auth_service.get_user_id_by_session(session_id)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    file_path = os.path.join(RESOURCE_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"File deleted: {filename}")
        
        # Update mapping
        if os.path.exists(MAPPING_FILE):
            with open(MAPPING_FILE, "r") as f:
                mapping = json.load(f)
            if filename in mapping:
                del mapping[filename]
                with open(MAPPING_FILE, "w") as f:
                    json.dump(mapping, f, indent=4)
        
        return jsonify({"message": "File deleted successfully"}), 200
    
    return jsonify({"error": "File not found"}), 404
