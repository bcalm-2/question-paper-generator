from flask import Blueprint, request, jsonify, send_file
import os
import json
from services.paper_service import PaperService
from repositories.paper_repository import PaperRepository
from text_extractor import TextExtractor
from nlp_analyzer import NLPAnalyzer
from bloom_classifier import BloomClassifier
from pdf_generator import PDFGenerator
from routes.auth_routes import auth_service
import logging

paper_bp = Blueprint('paper', __name__)
logger = logging.getLogger(__name__)

# Initialize dependencies
paper_repo = PaperRepository()
extractor = TextExtractor()
analyzer = NLPAnalyzer()
classifier = BloomClassifier()
pdf_gen = PDFGenerator()

paper_service = PaperService(paper_repo, extractor, analyzer, classifier, pdf_gen)

RESOURCE_FOLDER = "resources"
MAPPING_FILE = "mapping.json"

@paper_bp.route("/api/upload", methods=["POST"])
def upload_file():
    session_id = request.headers.get("X-Session-Id")
    user_id = auth_service.get_user_id_by_session(session_id)
    if not user_id:
        logger.warning("Unauthorized upload attempt")
        return jsonify({"error": "Unauthorized"}), 401

    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]
    subject_id = request.form.get("subject_id")

    if not subject_id:
        return jsonify({"message": "Subject ID is required"}), 400

    if file.filename == "":
        return jsonify({"message": "No filename"}), 400

    if not (file.filename.endswith(".pdf") or file.filename.endswith(".txt")):
        return jsonify({"message": "Only PDF or TXT allowed"}), 400

    # Get subject name for mapping
    from repositories.subject_repository import SubjectRepository
    sub_repo = SubjectRepository()
    subject_data = sub_repo.get_by_id(subject_id)
    subject_name = subject_data["name"] if subject_data else "Unknown"

    if not os.path.exists(RESOURCE_FOLDER):
        os.makedirs(RESOURCE_FOLDER)

    save_path = os.path.join(RESOURCE_FOLDER, file.filename)
    logger.info(f"Saving uploaded file: {file.filename} for subject: {subject_name}")
    file.save(save_path)

    # Load and update mapping
    mapping_data = {}
    if os.path.exists(MAPPING_FILE):
        try:
            with open(MAPPING_FILE, "r") as f:
                mapping_data = json.load(f)
        except Exception as e:
            logger.error(f"Error loading mapping file: {e}")

    mapping_data[file.filename] = subject_name
    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping_data, f, indent=4)

    return jsonify({"message": "Uploaded successfully"})

@paper_bp.route("/api/papers", methods=["GET"])
def get_papers():
    session_id = request.headers.get("X-Session-Id")
    user_id = auth_service.get_user_id_by_session(session_id)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    result, status = paper_service.get_papers(user_id)
    return jsonify(result), status

@paper_bp.route("/api/papers/generate", methods=["POST"])
def generate_paper():
    session_id = request.headers.get("X-Session-Id")
    user_id = auth_service.get_user_id_by_session(session_id)
    if not user_id:
        logger.warning("Unauthorized paper generation attempt")
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    logger.info(f"Generating paper for user {user_id}: Subject ID {data.get('subject_id')} {data.get('difficulty')}")
    data["user_id"] = user_id
    result, status = paper_service.generate_paper(data)
    if status == 201:
        logger.info(f"Paper generated successfully with ID: {result.get('paperId')}")
    else:
        logger.error(f"Paper generation failed: {result.get('error')}")
    return jsonify(result), status

@paper_bp.route("/api/papers/<int:paper_id>", methods=["GET", "PUT"])
def get_or_update_paper(paper_id):
    session_id = request.headers.get("X-Session-Id")
    user_id = auth_service.get_user_id_by_session(session_id)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == "PUT":
        data = request.get_json()
        result, status = paper_service.update_paper_details(paper_id, data, user_id)
        return jsonify(result), status
    
    result, status = paper_service.get_paper_details(paper_id, user_id)
    return jsonify(result), status

@paper_bp.route("/api/papers/<int:paper_id>/download", methods=["GET"])
def download_paper(paper_id):
    session_id = request.headers.get("X-Session-Id")
    user_id = auth_service.get_user_id_by_session(session_id)
    if not user_id:
        logger.warning(f"Unauthorized download attempt for paper {paper_id}")
        return jsonify({"error": "Unauthorized"}), 401

    logger.info(f"Generating PDF for paper {paper_id}")
    result, status = paper_service.get_paper_pdf(paper_id, user_id)
    if status == 200:
        logger.info(f"PDF generated successfully for paper {paper_id}")
        # result is the pdf_buffer
        paper, _ = paper_service.get_paper_details(paper_id, user_id)
        filename = f"{paper['subject']}_{paper['difficulty']}_Paper.pdf".replace(" ", "_")
        return send_file(
            result,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    logger.error(f"Failed to generate PDF for paper {paper_id}: {result.get('error')}")
    return jsonify(result), status
