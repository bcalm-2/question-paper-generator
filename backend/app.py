from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from backend.question_generator import QuestionGeneratorService

app = Flask(__name__)

users = []

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

    hashed_password = generate_password_hash(password)

    user = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "password": hashed_password
    }

    users.append(user)

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    for u in users:
        if u["email"] == email and check_password_hash(u["password"], password):
            return jsonify({
                "message": "Login successful",
                "user": {
                    "id": u["id"],
                    "name": u["name"],
                    "email": u["email"]
                }
            }), 200

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

if __name__ == "__main__":
    app.run(debug=True)
