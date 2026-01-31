from flask import Flask, request, jsonify
from services.openai_service import QuestionGeneratorService

app = Flask(__name__)

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
