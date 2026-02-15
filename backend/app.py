from flask import Flask, request, jsonify, make_response, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_cors import CORS
import os
import json
import random
from text_extractor import TextExtractor
from nlp_analyzer import NLPAnalyzer
from bloom_classifier import BloomClassifier
from pdf_generator import PDFGenerator
from db_config import init_db, get_db_connection

# Initialize Database
init_db()

app = Flask(__name__)

# In-memory session tracking remains for now (or could be moved to DB/Redis later)
sessions = {}
# papers list removed, will use DB

# Initialize Analyzers
extractor = TextExtractor()
analyzer = NLPAnalyzer()
classifier = BloomClassifier()
pdf_gen = PDFGenerator()

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

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        conn.commit()
        user_id = cursor.lastrowid
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

    session_id = str(uuid.uuid4())
    sessions[session_id] = user_id

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

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user["password"], password):
        session_id = str(uuid.uuid4())
        sessions[session_id] = user["id"]

        response = make_response(jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
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
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM papers ORDER BY created_at DESC")
    papers_list = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(papers_list), 200


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
    for qd in worthy_data:
        sent = qd["original"]
        question_text = qd["question"]
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

    # Split into MCQs and Short Answers
    mcq_count = min(5, len(potential_questions))
    mcqs = []
    for i in range(mcq_count):
        item = potential_questions[i]
        sent = item["text"]
        original = item["original"]
        
        available_keywords = [k for k in analysis["keywords"] if k.lower() not in original.lower()]
        distractors = random.sample(available_keywords, min(3, len(available_keywords)))
        while len(distractors) < 3: distractors.append(f"Option {len(distractors)+1}")
        
        # We store options as a comma separated string for now or just the text
        # To keep it simple, let's just use the question text.
        mcqs.append({
            "text": sent,
            "level": item["level"]
        })
        
    short_answers = []
    for i in range(mcq_count, min(10, len(potential_questions))):
        short_answers.append({
            "text": potential_questions[i]["text"],
            "level": potential_questions[i]["level"],
            "marks": 5 if difficulty == "Medium" else (3 if difficulty == "Easy" else 10)
        })

    # 3. Save to DB
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        title = f"{subject} {difficulty} Assessment"
        duration = "90 Mins"
        
        # Calculate total marks
        mcq_marks = len(mcqs) * 2
        short_marks = sum(q["marks"] for q in short_answers)
        total_marks = mcq_marks + short_marks

        # Insert Paper
        cursor.execute(
            "INSERT INTO papers (subject, title, marks, duration, difficulty) VALUES (%s, %s, %s, %s, %s)",
            (subject, title, total_marks, duration, difficulty)
        )
        paper_id = cursor.lastrowid

        # Function to save question and link it
        def save_q(q_data, q_type, q_marks):
            cursor.execute(
                "INSERT INTO questions (question_text, bloom_level, difficulty, question_type) VALUES (%s, %s, %s, %s)",
                (q_data["text"], q_data.get("level", "Understand"), difficulty, q_type)
            )
            qid = cursor.lastrowid
            cursor.execute(
                "INSERT INTO paper_questions (paper_id, question_id, marks) VALUES (%s, %s, %s)",
                (paper_id, qid, q_marks)
            )

        for q in mcqs:
            save_q(q, 'MCQ', 2)

        for q in short_answers:
            save_q(q, 'Descriptive', q["marks"])

        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to save paper: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Paper generated successfully", "paperId": paper_id}), 201


@app.route("/api/papers/<int:paper_id>", methods=["PUT"])
def update_paper(paper_id):
    # For now, let's just return a placeholder or implement if needed
    # Usually update means regenerating or editing specific fields
    return jsonify({"message": "Update functionality not yet fully migrated, but paper persists in DB."}), 200


@app.route("/api/papers/<int:paper_id>", methods=["GET"])
def get_paper(paper_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM papers WHERE id = %s", (paper_id,))
    paper = cursor.fetchone()
    
    if not paper:
        cursor.close()
        conn.close()
        return jsonify({"error": "Paper not found"}), 404
        
    # Fetch questions
    query = """
    SELECT q.*, pq.marks 
    FROM questions q
    JOIN paper_questions pq ON q.id = pq.question_id
    WHERE pq.paper_id = %s
    """
    cursor.execute(query, (paper_id,))
    questions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Format for UI
    mcqs = [q for q in questions if q['question_type'] == 'MCQ']
    short_answers = [q for q in questions if q['question_type'] == 'Descriptive']
    
    # In DB we don't store options separately currently, so we'll mock them if needed for the UI
    for q in mcqs:
        q["text"] = q["question_text"]
        q["options"] = ["Option A", "Option B", "Option C", "Option D"] # Placeholder for now
        
    for q in short_answers:
        q["text"] = q["question_text"]

    paper["sections"] = []
    if mcqs:
        paper["sections"].append({
            "name": "Section A: Multiple Choice Questions",
            "marks": sum(q['marks'] for q in mcqs),
            "questions": mcqs
        })
    if short_answers:
        paper["sections"].append({
            "name": "Section B: Short Answer Questions",
            "marks": sum(q['marks'] for q in short_answers),
            "questions": short_answers
        })
        
    return jsonify(paper), 200


@app.route("/api/papers/<int:paper_id>/download", methods=["GET"])
def download_paper(paper_id):
    # Fetch paper data from DB for PDF generation
    response = get_paper(paper_id)
    if response[1] != 200:
        return response
    
    paper = response[0].get_json()
        
    try:
        pdf_buffer = pdf_gen.generate_pdf(paper)
        filename = f"{paper['subject']}_{paper['difficulty']}_Paper.pdf".replace(" ", "_")
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
