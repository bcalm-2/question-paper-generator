"""
Application entry point for the Questify backend.

Responsibilities:
    - Bootstrap logging
    - Initialise the database schema (once, guarded against the Werkzeug reloader)
    - Configure CORS
    - Register Flask blueprints
    - Expose health-check and run the development server
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

from infrastructure.config_service import config_service
from infrastructure.db_config import init_db
from routes.auth_routes import auth_bp
from routes.paper_routes import paper_bp
from routes.config_routes import config_bp

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Database initialisation (skip in Werkzeug's child reloader process)
# ---------------------------------------------------------------------------
if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
    init_db()
else:
    logger.info("Skipping init_db in reloader subprocess.")

# ---------------------------------------------------------------------------
# Flask application
# ---------------------------------------------------------------------------
app = Flask(__name__)

# CORS — require explicit origin allowlist in production
allowed_origins = [
    o.strip()
    for o in config_service.get("ALLOWED_ORIGINS", "").split(",")
    if o.strip()
]
if not allowed_origins:
    if config_service.get("FLASK_ENV") != "development":
        raise RuntimeError("ALLOWED_ORIGINS environment variable is missing!")
    allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

CORS(
    app,
    resources={
        r"/api/*": {
            "origins":        allowed_origins,
            "expose_headers": ["X-Session-Id"],
            "allow_headers":  ["Content-Type", "X-Session-Id"],
        }
    },
)

# ---------------------------------------------------------------------------
# Blueprints
# ---------------------------------------------------------------------------
app.register_blueprint(auth_bp,   url_prefix="/api/auth")
app.register_blueprint(paper_bp)
app.register_blueprint(config_bp)

# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    """Basic liveness probe — returns 200 OK when the server is running."""
    logger.info("Health check called.")
    return jsonify({"status": "ok", "message": "Questify Server is running"}), 200

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    debug_mode = config_service.get("FLASK_ENV") == "development"
    port       = int(config_service.get("PORT", 5000))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
