import os
import json
import random

class PaperService:
    def __init__(self, paper_repo, extractor, analyzer, classifier, pdf_gen):
        self.paper_repo = paper_repo
        self.extractor = extractor
        self.analyzer = analyzer
        self.classifier = classifier
        self.pdf_gen = pdf_gen
        self.RESOURCE_FOLDER = "resources"
        self.MAPPING_FILE = "mapping.json"

    def get_papers(self):
        papers = self.paper_repo.get_all()
        return papers, 200

    def generate_paper(self, data):
        subject = data.get("subject")
        topics = data.get("topics", [])
        blooms = data.get("blooms", [])
        difficulty = data.get("difficulty")

        if not subject or not topics or not blooms or not difficulty:
            return {"error": "Missing required fields"}, 400

        # Load mapping
        if not os.path.exists(self.MAPPING_FILE):
            return {"error": "Mapping file not found"}, 500
            
        with open(self.MAPPING_FILE, "r") as f:
            mapping = json.load(f)

        subject_files = [fname for fname, sub in mapping.items() if sub == subject]
        if not subject_files:
            return {"error": f"No reference files found for subject {subject}. Please upload a file first."}, 400

        file_path = os.path.join(self.RESOURCE_FOLDER, subject_files[0])
        try:
            raw_text = self.extractor.extract(file_path)
        except Exception as e:
            return {"error": f"Failed to extract text from file: {str(e)}"}, 500

        analysis = self.analyzer.analyze(raw_text)
        worthy_data = analysis["question_worthy_sentences"]

        potential_questions = []
        for qd in worthy_data:
            sent = qd["original"]
            level = self.classifier.classify(sent)
            matches_topic = any(topic.lower() in sent.lower() for topic in topics)
            if matches_topic and level in blooms:
                potential_questions.append({"text": qd["question"], "level": level, "original": sent})

        if not potential_questions:
            potential_questions = [
                {"text": d["question"], "level": self.classifier.classify(d["original"]), "original": d["original"]}
                for d in worthy_data[:10]
            ]

        # Selection logic
        mcq_count = min(5, len(potential_questions))
        mcqs = [{"text": potential_questions[i]["text"], "level": potential_questions[i]["level"]} for i in range(mcq_count)]
        
        short_answers = []
        for i in range(mcq_count, min(10, len(potential_questions))):
            short_answers.append({
                "text": potential_questions[i]["text"],
                "level": potential_questions[i]["level"],
                "marks": 5 if difficulty == "Medium" else (3 if difficulty == "Easy" else 10)
            })

        # Save to Repo
        try:
            total_marks = (len(mcqs) * 2) + sum(q["marks"] for q in short_answers)
            title = f"{subject} {difficulty} Assessment"
            paper_id = self.paper_repo.create_paper(subject, title, total_marks, "90 Mins", difficulty)

            for q in mcqs:
                qid = self.paper_repo.create_question(q["text"], q["level"], difficulty, 'MCQ')
                self.paper_repo.link_question_to_paper(paper_id, qid, 2)

            for q in short_answers:
                qid = self.paper_repo.create_question(q["text"], q["level"], difficulty, 'Descriptive')
                self.paper_repo.link_question_to_paper(paper_id, qid, q["marks"])

            return {"message": "Paper generated successfully", "paperId": paper_id}, 201
        except Exception as e:
            return {"error": f"Failed to save paper: {str(e)}"}, 500

    def get_paper_details(self, paper_id):
        paper = self.paper_repo.get_by_id(paper_id)
        if not paper:
            return {"error": "Paper not found"}, 404

        questions = self.paper_repo.get_questions_by_paper_id(paper_id)
        
        mcqs = [q for q in questions if q['question_type'] == 'MCQ']
        short_answers = [q for q in questions if q['question_type'] == 'Descriptive']

        for q in mcqs:
            q["text"] = q["question_text"]
            q["options"] = ["Option A", "Option B", "Option C", "Option D"]
            
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

        return paper, 200

    def get_paper_pdf(self, paper_id):
        paper, status = self.get_paper_details(paper_id)
        if status != 200:
            return paper, status

        try:
            pdf_buffer = self.pdf_gen.generate_pdf(paper)
            return pdf_buffer, 200
        except Exception as e:
            return {"error": f"Failed to generate PDF: {str(e)}"}, 500
