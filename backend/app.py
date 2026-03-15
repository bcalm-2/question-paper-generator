from services.config_service import config_service
from flask import Flask, jsonify, request
from flask_cors import CORS
from db_config import init_db
from routes.auth_routes import auth_bp
from routes.paper_routes import paper_bp
import logging

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Database
init_db()

app = Flask(__name__)

# Production-ready CORS
allowed_origins = config_service.get("ALLOWED_ORIGINS", "").split(",")
if not any(allowed_origins):
    if config_service.get("FLASK_ENV") != "development":
        raise RuntimeError("ALLOWED_ORIGINS environment variable is missing!")
    allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

CORS(app, resources={r"/api/*": {
    "origins": allowed_origins,
    "expose_headers": ["X-Session-Id"],
    "allow_headers": ["Content-Type", "X-Session-Id"]
}})

from constants import SUBJECT_TOPICS, BLOOMS

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(paper_bp)

@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    logger.info("Health check endpoint called")
    return jsonify({"status": "ok", "message": "Server is running"}), 200

from routes.auth_routes import auth_service

@app.route("/api/config", methods=["GET"])
def get_config():
    logger.info("Fetching application configuration")
    session_id = request.headers.get("X-Session-Id")
    user_id = auth_service.get_user_id_by_session(session_id)
    if not user_id:
        logger.warning("Unauthorized access attempt to /api/config")
        return jsonify({"error": "Unauthorized"}), 401

    config = {
        "SUBJECT_TOPICS": SUBJECT_TOPICS,
        "BLOOMS": BLOOMS
    }
    logger.info("Config fetched successfully")
    return jsonify(config), 200

if __name__ == "__main__":
    debug_mode = config_service.get("FLASK_ENV") == "development"
    port = int(config_service.get("PORT", 5000))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
