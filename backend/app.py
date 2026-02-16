from flask import Flask, jsonify
from flask_cors import CORS
from db_config import init_db
from routes.auth_routes import auth_bp
from routes.paper_routes import paper_bp

# Initialize Database
init_db()

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(paper_bp)

CONFIG = {
    "SUBJECT_TOPICS": {
        "DBMS": ["Normalization", "ER Model", "Transactions", "SQL", "Indexing", "Relational Algebra", "NoSQL", "Query Optimization"],
        "OS": ["Processes", "Memory Management", "Deadlocks", "Scheduling", "File Systems", "Virtual Memory", "Threads", "Distributed Systems"],
        "CN": ["OSI Model", "TCP/IP", "Routing", "Network Security", "DNS", "HTTP/HTTPS", "Socket Programming", "Wireless Networks"],
        "DSA": ["Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming", "Sorting", "Searching", "Recursion"],
        "AI": ["Search Algorithms", "Neural Networks", "ML Basics", "NLP", "Robotics", "Expert Systems", "Fuzzy Logic"]
    },
    "BLOOMS": ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify(CONFIG), 200

if __name__ == "__main__":
    app.run(debug=True)
