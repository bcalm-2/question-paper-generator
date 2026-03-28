from __future__ import annotations

from flask import Blueprint, request, jsonify
from core.container import auth_service, app_config_service, subject_service, file_service
import logging

config_bp = Blueprint("config", __name__)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helper — auth guard
# ---------------------------------------------------------------------------

def _get_user_id() -> int | None:
    """Extracts and validates the session token from the request header."""
    return auth_service.get_user_id_by_session(request.headers.get("X-Session-Id"))


# ---------------------------------------------------------------------------
# Application config
# ---------------------------------------------------------------------------

@config_bp.route("/api/config", methods=["GET"])
def get_app_config():
    """
    Return application configuration (subjects, topics, Bloom's levels).
    Served from cache after the first request.
    """
    if not _get_user_id():
        return jsonify({"error": "Unauthorized"}), 401

    config = app_config_service.get_app_config()
    return jsonify(config), 200


# ---------------------------------------------------------------------------
# Subject management (admin)
# ---------------------------------------------------------------------------

@config_bp.route("/api/admin/subjects", methods=["GET"])
def get_subjects():
    """Return full subject list with topics for the admin panel."""
    if not _get_user_id():
        return jsonify({"error": "Unauthorized"}), 401

    subjects = app_config_service.get_admin_subjects()
    return jsonify(subjects), 200


@config_bp.route("/api/admin/subjects", methods=["POST"])
def add_subject():
    """
    Create a new subject with optional topics.

    Request body (JSON): ``{ name: str, topics: [str, ...] }``
    """
    user_id = _get_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    result, status = subject_service.add_subject(
        name=data.get("name"),
        topics=data.get("topics", []),
    )
    if status == 201:
        logger.info(f"Subject '{data.get('name')}' added by user {user_id}")
    return jsonify(result), status


@config_bp.route("/api/admin/subjects/<int:subject_id>", methods=["DELETE"])
def delete_subject(subject_id: int):
    """Delete a subject and clear the configuration cache."""
    user_id = _get_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    result, status = subject_service.delete_subject(subject_id)
    logger.info(f"Subject {subject_id} deleted by user {user_id}")
    return jsonify(result), status


# ---------------------------------------------------------------------------
# File management (admin)
# ---------------------------------------------------------------------------

@config_bp.route("/api/admin/files", methods=["GET"])
def list_files():
    """List all uploaded reference files with their subject mappings."""
    if not _get_user_id():
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(file_service.list_files()), 200


@config_bp.route("/api/admin/files/<filename>", methods=["DELETE"])
def delete_file(filename: str):
    """Permanently delete a reference file from the server."""
    if not _get_user_id():
        return jsonify({"error": "Unauthorized"}), 401

    if file_service.delete_entry(filename):
        return jsonify({"message": "File deleted successfully"}), 200

    return jsonify({"error": "File not found"}), 404
