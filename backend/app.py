from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_cors import CORS
import os
import json

app = Flask(__name__)

users = []
sessions = {}
papers = []

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

@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    for u in users:
        if u["email"] == email:
            return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    user = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "password": hashed_password
    }

    users.append(user)

    session_id = str(uuid.uuid4())
    sessions[session_id] = user["id"]

    response = make_response(jsonify({"message": "User registered successfully"}), 201)
    response.headers["X-Session-Id"] = session_id
    return response


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    for u in users:
        if u["email"] == email and check_password_hash(u["password"], password):
            session_id = str(uuid.uuid4())
            sessions[session_id] = u["id"]

            response = make_response(jsonify({
                "message": "Login successful",
                "user": {
                    "id": u["id"],
                    "name": u["name"],
                    "email": u["email"]
                }
            }), 200)
            response.headers["X-Session-Id"] = session_id
            return response

    return jsonify({"error": "Invalid credentials"}), 401

CORS(app)

RESOURCE_FOLDER = "resources"
MAPPING_FILE = "mapping.json"

if not os.path.exists(RESOURCE_FOLDER):
    os.makedirs(RESOURCE_FOLDER)

if not os.path.exists(MAPPING_FILE):
    with open(MAPPING_FILE, "w") as f:
        json.dump({}, f)


@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]
    subject = request.form.get("subject")

    if not subject:
        return jsonify({"message": "Subject is required"}), 400

    if file.filename == "":
        return jsonify({"message": "No filename"}), 400

    if not (file.filename.endswith(".pdf") or file.filename.endswith(".txt")):
        return jsonify({"message": "Only PDF or TXT allowed"}), 400

    save_path = os.path.join(RESOURCE_FOLDER, file.filename)
    file.save(save_path)

    # update mapping.json
    with open(MAPPING_FILE, "r") as f:
        data = json.load(f)

    data[file.filename] = subject

    with open(MAPPING_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return jsonify({"message": "Uploaded successfully"})


@app.route("/api/papers", methods=["GET"])
def get_papers():
    return jsonify(papers), 200


@app.route("/api/papers/generate", methods=["POST"])
def generate_paper():
    data = request.get_json()
    
    subject = data.get("subject")
    topics = data.get("topics")
    blooms = data.get("blooms")
    difficulty = data.get("difficulty")
    
    if not subject or not topics or not blooms or not difficulty:
        return jsonify({"error": "Missing required fields"}), 400
        
    paper_id = len(papers) + 1
    
    # Mock Paper Generation Logic
    # In a real system, this would use NLP/TextExtractor to generate questions
    mock_paper = {
        "id": paper_id,
        "subject": subject,
        "title": f"{subject} {difficulty} Assessment",
        "date": "2024-02-09", # Dynamic date ideally
        "marks": 50,
        "duration": "90 Mins",
        "sections": [
            {
                "name": "Section A: Multiple Choice Questions",
                "marks": 10,
                "questions": [
                    {"id": 1, "text": f"Which of the following relates to {topics[0] if topics else 'Topic'}?", "options": ["A", "B", "C", "D"]}
                ]
            },
            {
                "name": "Section B: Short Answer Questions",
                "marks": 20,
                "questions": [
                    {"id": 2, "text": f"Explain the concept of {topics[1] if len(topics)>1 else 'Topic'} in detail.", "marks": 5}
                ]
            }
        ]
    }
    
    papers.append(mock_paper)
    
    return jsonify({"message": "Paper generated successfully", "paperId": paper_id}), 201


@app.route("/api/papers/<int:paper_id>", methods=["PUT"])
def update_paper(paper_id):
    data = request.get_json()
    
    subject = data.get("subject")
    topics = data.get("topics")
    blooms = data.get("blooms")
    difficulty = data.get("difficulty")
    
    if not subject or not topics or not blooms or not difficulty:
        return jsonify({"error": "Missing required fields"}), 400
        
    paper_index = next((i for i, p in enumerate(papers) if p["id"] == paper_id), None)
    if paper_index is None:
        return jsonify({"error": "Paper not found"}), 404
        
    # Reuse mock generation logic to "update" the paper
    updated_paper = {
        "id": paper_id,
        "subject": subject,
        "title": f"{subject} {difficulty} Assessment",
        "date": papers[paper_index].get("date", "2024-02-09"),
        "marks": 50,
        "duration": "90 Mins",
        "sections": [
            {
                "name": "Section A: Multiple Choice Questions",
                "marks": 10,
                "questions": [
                    {"id": 1, "text": f"Which of the following relates to {topics[0] if topics else 'Topic'}?", "options": ["A", "B", "C", "D"]}
                ]
            },
            {
                "name": "Section B: Short Answer Questions",
                "marks": 20,
                "questions": [
                    {"id": 2, "text": f"Explain the concept of {topics[1] if len(topics)>1 else 'Topic'} in detail.", "marks": 5}
                ]
            }
        ]
    }
    
    papers[paper_index] = updated_paper
    
    return jsonify({"message": "Paper updated successfully", "paperId": paper_id}), 200


@app.route("/api/papers/<int:paper_id>", methods=["GET"])
def get_paper(paper_id):
    paper = next((p for p in papers if p["id"] == paper_id), None)
    if not paper:
        return jsonify({"error": "Paper not found"}), 404
    return jsonify(paper), 200


if __name__ == "__main__":
    app.run(debug=True)
