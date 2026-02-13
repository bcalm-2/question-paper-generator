from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_cors import CORS
import os
import json
import random
from text_extractor import TextExtractor
from nlp_analyzer import NLPAnalyzer
from bloom_classifier import BloomClassifier

from backend.question_generator import QuestionGeneratorService

app = Flask(__name__)

users = []
sessions = {}
papers = []

# Initialize Analyzers
extractor = TextExtractor()
analyzer = NLPAnalyzer()
classifier = BloomClassifier()

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

# CORS(app)
#
# RESOURCE_FOLDER = "resources"
# MAPPING_FILE = "mapping.json"
#
# if not os.path.exists(RESOURCE_FOLDER):
#     os.makedirs(RESOURCE_FOLDER)
#
# if not os.path.exists(MAPPING_FILE):
#     with open(MAPPING_FILE, "w") as f:
#         json.dump({}, f)


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

    # save_path = os.path.join(RESOURCE_FOLDER, file.filename)
    # file.save(save_path)
    #
    # # update mapping.json
    # with open(MAPPING_FILE, "r") as f:
    #     data = json.load(f)
    #
    # data[file.filename] = subject
    #
    # with open(MAPPING_FILE, "w") as f:
    #     json.dump(data, f, indent=4)

    return jsonify({"message": "Uploaded successfully"})

@app.route("/generate-questions", methods=["POST"])
def generate_questions():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400

    result = QuestionGeneratorService.generate_questions(
        processed_text=data["text"],
        num_questions=data.get("count", 5)
    )

    if not result["success"]:
        return jsonify({"error": result["error"]}), 500

    return jsonify(result["data"]), 200

@app.route("/api/papers", methods=["GET"])
def get_papers():
    return jsonify(papers), 200


@app.route("/api/papers/generate", methods=["POST"])
def generate_paper():
    data = request.get_json()
    
    subject = data.get("subject")
    topics = data.get("topics", [])
    blooms = data.get("blooms", [])
    difficulty = data.get("difficulty")
    
    if not subject or not topics or not blooms or not difficulty:
        return jsonify({"error": "Missing required fields"}), 400
        
    # 1. Fetch relevant files for this subject from mapping.json
    with open(MAPPING_FILE, "r") as f:
        mapping = json.load(f)
    
    subject_files = [fname for fname, sub in mapping.items() if sub == subject]
    
    if not subject_files:
        return jsonify({"error": f"No reference files found for subject {subject}. Please upload a file first."}), 400
    
    # Process the first file found
    file_path = os.path.join(RESOURCE_FOLDER, subject_files[0])
    try:
        raw_text = extractor.extract(file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to extract text from file: {str(e)}"}), 500
        
    analysis = analyzer.analyze(raw_text)
    worthy_data = analysis["question_worthy_sentences"]
    
    # 2. Filter and Classify questions based on requested Blooms and Topics
    potential_questions = []
    for data in worthy_data:
        sent = data["original"]
        question_text = data["question"]
        level = classifier.classify(sent)
        
        # Check if sentence contains any of the selected topics (case-insensitive)
        matches_topic = any(topic.lower() in sent.lower() for topic in topics)
        
        if matches_topic and level in blooms:
            potential_questions.append({
                "text": question_text,
                "level": level,
                "original": sent
            })
            
    if not potential_questions:
        # Fallback: if no perfect match, just take some worthy sentences
        potential_questions = [
            {"text": d["question"], "level": classifier.classify(d["original"]), "original": d["original"]} 
            for d in worthy_data[:10]
        ]

    # 3. Construct Paper Object
    paper_id = len(papers) + 1
    
    # Simple logic to split into MCQs and Short Answers
    mcq_count = min(5, len(potential_questions))
    mcqs = []
    for i in range(mcq_count):
        item = potential_questions[i]
        sent = item["text"]
        original = item["original"]
        
        # Basic MCQ distractor generation using keywords found in doc
        # Filter out keywords that might be in the original sentence to avoid confusion
        available_keywords = [k for k in analysis["keywords"] if k.lower() not in original.lower()]
        distractors = random.sample(available_keywords, min(3, len(available_keywords)))
        while len(distractors) < 3: distractors.append(f"Option {len(distractors)+1}")
        
        # Correct answer is usually a key word from the original sentence
        # For now, let's just pick one noun from the original sentence as the "answer" 
        # but since we are generating "Explain..." style questions, MCQs are a bit tricky.
        # Let's pivot MCQs to be more about keyword identification if possible.
        
        mcqs.append({
            "id": i + 1,
            "text": sent,
            "options": random.sample([original.split()[-1].strip(".,!?;:")] + distractors, 4)
        })
        
    short_answers = []
    for i in range(mcq_count, min(10, len(potential_questions))):
        short_answers.append({
            "id": i + 1,
            "text": potential_questions[i]["text"],
            "marks": 5 if difficulty == "Medium" else (3 if difficulty == "Easy" else 10)
        })

    real_paper = {
        "id": paper_id,
        "subject": subject,
        "topics": topics,
        "blooms": blooms,
        "difficulty": difficulty,
        "title": f"{subject} {difficulty} Assessment",
        "date": "2024-02-12",
        "marks": (len(mcqs) * 2) + (len(short_answers) * (5 if difficulty == "Medium" else (3 if difficulty == "Easy" else 10))),
        "duration": "90 Mins",
        "sections": []
    }
    
    if mcqs:
        real_paper["sections"].append({
            "name": "Section A: Multiple Choice Questions",
            "marks": len(mcqs) * 2,
            "questions": mcqs
        })
    if short_answers:
        real_paper["sections"].append({
            "name": "Section B: Short Answer Questions",
            "marks": real_paper["marks"] - (len(mcqs) * 2),
            "questions": short_answers
        })
    
    papers.append(real_paper)
    return jsonify({"message": "Paper generated successfully", "paperId": paper_id}), 201


@app.route("/api/papers/<int:paper_id>", methods=["PUT"])
def update_paper(paper_id):
    data = request.get_json()
    
    subject = data.get("subject")
    topics = data.get("topics", [])
    blooms = data.get("blooms", [])
    difficulty = data.get("difficulty")
    
    if not subject or not topics or not blooms or not difficulty:
        return jsonify({"error": "Missing required fields"}), 400
        
    paper_index = next((i for i, p in enumerate(papers) if p["id"] == paper_id), None)
    if paper_index is None:
        return jsonify({"error": "Paper not found"}), 404
        
    # 1. Fetch relevant files for this subject
    with open(MAPPING_FILE, "r") as f:
        mapping = json.load(f)
    
    subject_files = [fname for fname, sub in mapping.items() if sub == subject]
    
    if not subject_files:
        return jsonify({"error": f"No reference files found for subject {subject}"}), 400
    
    file_path = os.path.join(RESOURCE_FOLDER, subject_files[0])
    try:
        raw_text = extractor.extract(file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to extract text: {str(e)}"}), 500
        
    worthy_data = analysis["question_worthy_sentences"]
    
    potential_questions = []
    for data in worthy_data:
        sent = data["original"]
        question_text = data["question"]
        level = classifier.classify(sent)
        matches_topic = any(topic.lower() in sent.lower() for topic in topics)
        if matches_topic and level in blooms:
            potential_questions.append({
                "text": question_text,
                "level": level,
                "original": sent
            })
            
    if not potential_questions:
        potential_questions = [
            {"text": d["question"], "level": classifier.classify(d["original"]), "original": d["original"]} 
            for d in worthy_data[:10]
        ]

    mcq_count = min(5, len(potential_questions))
    mcqs = []
    for i in range(mcq_count):
        item = potential_questions[i]
        sent = item["text"]
        original = item["original"]
        
        available_keywords = [k for k in analysis["keywords"] if k.lower() not in original.lower()]
        distractors = random.sample(available_keywords, min(3, len(available_keywords)))
        while len(distractors) < 3: distractors.append(f"Option {len(distractors)+1}")
        
        mcqs.append({
            "id": i + 1,
            "text": sent,
            "options": random.sample([original.split()[-1].strip(".,!?;:")] + distractors, 4)
        })
        
    short_answers = []
    for i in range(mcq_count, min(10, len(potential_questions))):
        short_answers.append({
            "id": i + 1,
            "text": potential_questions[i]["text"],
            "marks": 5 if difficulty == "Medium" else (3 if difficulty == "Easy" else 10)
        })

    updated_paper = {
        "id": paper_id,
        "subject": subject,
        "topics": topics,
        "blooms": blooms,
        "difficulty": difficulty,
        "title": f"{subject} {difficulty} Assessment",
        "date": papers[paper_index].get("date", "2024-02-12"),
        "marks": (len(mcqs) * 2) + (len(short_answers) * (5 if difficulty == "Medium" else (3 if difficulty == "Easy" else 10))),
        "duration": "90 Mins",
        "sections": []
    }
    
    if mcqs:
        updated_paper["sections"].append({
            "name": "Section A: Multiple Choice Questions",
            "marks": len(mcqs) * 2,
            "questions": mcqs
        })
    if short_answers:
        updated_paper["sections"].append({
            "name": "Section B: Short Answer Questions",
            "marks": updated_paper["marks"] - (len(mcqs) * 2),
            "questions": short_answers
        })
    
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
