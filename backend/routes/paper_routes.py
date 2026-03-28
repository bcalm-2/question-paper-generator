from __future__ import annotations

from flask import Blueprint, request, jsonify, send_file
from core.container import auth_service, paper_service, file_service, subject_repo
import logging

paper_bp = Blueprint("paper", __name__)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helper — auth guard
# ---------------------------------------------------------------------------

def _get_user_id() -> int | None:
    """Extracts and validates the session token from the request header."""
    return auth_service.get_user_id_by_session(request.headers.get("X-Session-Id"))


# ---------------------------------------------------------------------------
# File upload
# ---------------------------------------------------------------------------

@paper_bp.route("/api/upload", methods=["POST"])
def upload_file():
    """
    Upload a reference material file (PDF or TXT) for a given subject.

    Form data:
        - ``file``: the uploaded file
        - ``subject_id``: ID of the associated subject

    Returns 200 on success, 400/401/500 on failure.
    """
    user_id = _get_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]
    subject_id = request.form.get("subject_id")

    if not subject_id or file.filename == "":
        return jsonify({"message": "Subject ID and a valid file are required"}), 400

    if not (file.filename.endswith(".pdf") or file.filename.endswith(".txt")):
        return jsonify({"message": "Only PDF or TXT files are allowed"}), 400

    subject_data = subject_repo.get_by_id(subject_id)
    subject_name = subject_data["name"] if subject_data else "Unknown"

    try:
        file_service.save_file(file, subject_name)
        return jsonify({"message": "Uploaded successfully"}), 200
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return jsonify({"error": "Failed to save file"}), 500


# ---------------------------------------------------------------------------
# Paper CRUD
# ---------------------------------------------------------------------------

@paper_bp.route("/api/papers", methods=["GET"])
def get_papers():
    """Return all papers belonging to the authenticated user."""
    user_id = _get_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    result, status = paper_service.get_papers(user_id)
    return jsonify(result), status


@paper_bp.route("/api/papers/generate", methods=["POST"])
def generate_paper():
    """
    Trigger AI-driven question-paper generation.

    Request body (JSON): subject_id, topics, blooms, difficulty, num_questions
    """
    user_id = _get_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    data["user_id"] = user_id
    result, status = paper_service.generate_paper(data)
    return jsonify(result), status


@paper_bp.route("/api/papers/<int:paper_id>", methods=["GET", "PUT"])
def get_or_update_paper(paper_id: int):
    """Retrieve (GET) or update metadata (PUT) for a specific paper."""
    user_id = _get_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == "PUT":
        result, status = paper_service.update_paper_details(
            paper_id, request.get_json(), user_id
        )
        return jsonify(result), status

    result, status = paper_service.get_paper_details(paper_id, user_id)
    return jsonify(result), status


@paper_bp.route("/api/papers/<int:paper_id>/download", methods=["GET"])
def download_paper(paper_id: int):
    """Generate and stream a PDF for the given question paper."""
    user_id = _get_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    pdf_buffer, paper, status = paper_service.get_paper_pdf(paper_id, user_id)
    if status != 200:
        return jsonify(paper), status

    filename = f"{paper['subject']}_{paper['difficulty']}_Paper.pdf".replace(" ", "_")
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf",
    )
