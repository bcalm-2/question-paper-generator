from flask import Flask, jsonify
from flask_cors import CORS
from db_config import init_db
from routes.auth_routes import auth_bp
from routes.paper_routes import paper_bp

# Initialize Database
init_db()

app = Flask(__name__)
CORS(app)

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
    app.run(debug=True)
