from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

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


if __name__ == "__main__":
    app.run(debug=True)
