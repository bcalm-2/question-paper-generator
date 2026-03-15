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

    def get_papers(self, user_id):
        papers = self.paper_repo.get_all(user_id)
        return papers, 200

    def generate_paper(self, data):
        subject = data.get("subject")
        topics = data.get("topics", [])
        blooms = data.get("blooms", [])
        difficulty = data.get("difficulty")
        num_questions = int(data.get("num_questions", 10))

        missing = [f for f in ["subject", "topics", "blooms", "difficulty"] if not data.get(f)]
        if missing:
            return {"error": f"Missing required fields: {', '.join(missing)}"}, 400

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
                potential_questions.append({
                    "text": qd["question"], 
                    "level": level, 
                    "original": sent,
                    "subject": qd.get("subject")
                })

        if not potential_questions:
            potential_questions = [
                {
                    "text": d["question"], 
                    "level": self.classifier.classify(d["original"]), 
                    "original": d["original"],
                    "subject": d.get("subject")
                }
                for d in worthy_data[:num_questions]
            ]
        
        # Limit to requested number of questions
        potential_questions = potential_questions[:num_questions]

        # Selection logic (Split between MCQ and Descriptive)
        mcq_target = num_questions // 2
        mcqs = []
        for i in range(min(mcq_target, len(potential_questions))):
            q = potential_questions[i]
            # Use keywords for distractors
            distractors = [kw.title() for kw in analysis["keywords"] if q["subject"] and kw.lower() != q["subject"].lower()]
            random.shuffle(distractors)
            
            options = [{"text": q["subject"] if q["subject"] else "None of the above", "is_correct": True}]
            for d in distractors[:3]:
                options.append({"text": d, "is_correct": False})
            
            while len(options) < 4:
                options.append({"text": f"Alternative {len(options)}", "is_correct": False})
            
            random.shuffle(options)
            mcqs.append({
                "text": f"Which of the following refers to: {q['original']}?",
                "level": q["level"],
                "options": options
            })
        
        short_answers = []
        for i in range(len(mcqs), len(potential_questions)):
            short_answers.append({
                "text": potential_questions[i]["text"],
                "level": potential_questions[i]["level"],
                "marks": 5 if difficulty == "Medium" else (3 if difficulty == "Easy" else 10)
            })

        # Save to Repo
        try:
            total_marks = (len(mcqs) * 2) + sum(q["marks"] for q in short_answers)
            title = f"{subject} {difficulty} Assessment"
            paper_id = self.paper_repo.create_paper(data.get("user_id"), subject, title, total_marks, "90 Mins", difficulty)

            for q in mcqs:
                qid = self.paper_repo.create_question(q["text"], q["level"], difficulty, 'MCQ')
                self.paper_repo.link_question_to_paper(paper_id, qid, 2)
                for opt in q["options"]:
                    self.paper_repo.add_question_option(qid, opt["text"], opt["is_correct"])

            for q in short_answers:
                qid = self.paper_repo.create_question(q["text"], q["level"], difficulty, 'Descriptive')
                self.paper_repo.link_question_to_paper(paper_id, qid, q["marks"])

            return {"message": "Paper generated successfully", "paperId": paper_id}, 201
        except Exception as e:
            return {"error": f"Failed to save paper: {str(e)}"}, 500

    def get_paper_details(self, paper_id, user_id):
        paper = self.paper_repo.get_by_id(paper_id)
        if not paper:
            return {"error": "Paper not found"}, 404
        
        if paper['user_id'] != user_id:
            return {"error": "Unauthorized access to this paper"}, 403

        questions = self.paper_repo.get_questions_by_paper_id(paper_id)
        
        mcqs = [q for q in questions if q['question_type'] == 'MCQ']
        short_answers = [q for q in questions if q['question_type'] == 'Descriptive']

        for q in mcqs:
            q["text"] = q["question_text"]
            options = self.paper_repo.get_options_by_question_id(q["id"])
            if options:
                q["options"] = [opt["option_text"] for opt in options]
            else:
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

    def get_paper_pdf(self, paper_id, user_id):
        paper, status = self.get_paper_details(paper_id, user_id)
        if status != 200:
            return paper, status

        try:
            pdf_buffer = self.pdf_gen.generate_pdf(paper)
            return pdf_buffer, 200
        except Exception as e:
            return {"error": f"Failed to generate PDF: {str(e)}"}, 500

    def update_paper_details(self, paper_id, data, user_id):
        try:
            existing_paper = self.paper_repo.get_by_id(paper_id)
            if not existing_paper:
                return {"error": "Paper not found"}, 404
            
            if existing_paper['user_id'] != user_id:
                return {"error": "Unauthorized access to update this paper"}, 403
            
            # Use provided values or fall back to existing ones
            subject = data.get("subject", existing_paper['subject'])
            title = data.get("title", existing_paper['title'])
            marks = data.get("marks", existing_paper['marks'])
            duration = data.get("duration", existing_paper['duration'])
            difficulty = data.get("difficulty", existing_paper['difficulty'])

            self.paper_repo.update_paper(paper_id, subject, title, marks, duration, difficulty)
            return {"message": "Paper updated successfully"}, 200
        except Exception as e:
            return {"error": f"Failed to update paper: {str(e)}"}, 500
