from services.config_service import config_service
from flask import Flask, jsonify
from flask_cors import CORS
from db_config import init_db
from routes.auth_routes import auth_bp
from routes.paper_routes import paper_bp

# Initialize Database
init_db()

app = Flask(__name__)

# Production-ready CORS
allowed_origins = config_service.get("ALLOWED_ORIGINS", "").split(",")
if not any(allowed_origins):
    if config_service.get("FLASK_ENV") != "development":
        raise RuntimeError("ALLOWED_ORIGINS environment variable is missing!")
    allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

from constants import SUBJECT_TOPICS, BLOOMS

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(paper_bp)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/config", methods=["GET"])
def get_config():
    config = {
        "SUBJECT_TOPICS": SUBJECT_TOPICS,
        "BLOOMS": BLOOMS
    }
    return jsonify(config), 200

if __name__ == "__main__":
    debug_mode = config_service.get("FLASK_ENV") == "development"
    port = int(config_service.get("PORT", 5000))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
