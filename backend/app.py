from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
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


