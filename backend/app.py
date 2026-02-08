from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_cors import CORS
import os
import json

app = Flask(__name__)

users = []
sessions = {}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

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


if __name__ == "__main__":
    app.run(debug=True)
