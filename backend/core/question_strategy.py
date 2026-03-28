import random
import logging

logger = logging.getLogger(__name__)

class QuestionStrategy:
    """
    Interface/Base class for question generation strategies.
    (Can be expanded for more complex strategies later)
    """
    def select_questions(self, analysis, topics, blooms, num_questions):
        """Filters analysis data by topics and bloom levels."""
        worthy_data = analysis.get("question_worthy_sentences", [])
        potential = []
        
        for qd in worthy_data:
            sent = qd["original"]
            level = qd["bloom_level"]
            
            # Simple topic matching
            matches_topic = any(topic.lower() in sent.lower() for topic in topics)
            if matches_topic and level in blooms:
                potential.append({
                    "text": qd["question"],
                    "level": level,
                    "original": sent,
                    "subject": qd.get("subject")
                })
        
        # Fallback if no matches found
        if not potential:
            logger.info("No specific matches for topics/blooms. Falling back to top segments.")
            for d in worthy_data[:num_questions]:
                potential.append({
                    "text": d["question"],
                    "level": d["bloom_level"],
                    "original": d["original"],
                    "subject": d.get("subject")
                })
                
        return potential[:num_questions]

    def format_paper(self, selected_questions, difficulty, keywords):
        """
        Formats selected questions into MCQs and Descriptive sections.
        """
        mcq_target = len(selected_questions) // 2
        mcqs = []
        short_answers = []
        
        # 1. Build MCQs
        for i in range(min(mcq_target, len(selected_questions))):
            q = selected_questions[i]
            options = self._build_mcq_options(q, keywords)
            
            mcqs.append({
                "text": f"Which of the following refers to: {q['original']}?",
                "level": q["level"],
                "options": options,
                "marks": 2
            })
            
        # 2. Build Descriptive
        for i in range(len(mcqs), len(selected_questions)):
            q = selected_questions[i]
            marks = 5 if difficulty == "Medium" else (3 if difficulty == "Easy" else 10)
            
            short_answers.append({
                "text": q["text"],
                "level": q["level"],
                "marks": marks
            })
            
        return mcqs, short_answers

    def _build_mcq_options(self, question, keywords):
        """Helper to create distractors from keywords."""
        correct_answer = question["subject"] if question["subject"] else "None of the above"
        distractors = [kw.title() for kw in keywords if correct_answer and kw.lower() != correct_answer.lower()]
        
        random.shuffle(distractors)
        
        options = [{"text": correct_answer, "is_correct": True}]
        for d in distractors[:3]:
            options.append({"text": d, "is_correct": False})
            
        # Ensure 4 options
        while len(options) < 4:
            options.append({"text": f"Alternative {len(options) + 1}", "is_correct": False})
            
        random.shuffle(options)
        return options
