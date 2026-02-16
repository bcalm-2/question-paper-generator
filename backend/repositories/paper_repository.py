from .base_repository import BaseRepository

class PaperRepository(BaseRepository):
    def get_all(self):
        return self.execute_query("SELECT * FROM papers ORDER BY created_at DESC")

    def get_by_id(self, paper_id):
        result = self.execute_query("SELECT * FROM papers WHERE id = %s", (paper_id,))
        return result[0] if result else None

    def create_paper(self, subject, title, marks, duration, difficulty):
        query = "INSERT INTO papers (subject, title, marks, duration, difficulty) VALUES (%s, %s, %s, %s, %s)"
        params = (subject, title, marks, duration, difficulty)
        return self.execute_query(query, params, commit=True)

    def create_question(self, text, level, difficulty, q_type):
        query = "INSERT INTO questions (question_text, bloom_level, difficulty, question_type) VALUES (%s, %s, %s, %s)"
        params = (text, level, difficulty, q_type)
        return self.execute_query(query, params, commit=True)

    def link_question_to_paper(self, paper_id, question_id, marks):
        query = "INSERT INTO paper_questions (paper_id, question_id, marks) VALUES (%s, %s, %s)"
        params = (paper_id, question_id, marks)
        return self.execute_query(query, params, commit=True)

    def get_questions_by_paper_id(self, paper_id):
        query = """
        SELECT q.*, pq.marks 
        FROM questions q
        JOIN paper_questions pq ON q.id = pq.question_id
        WHERE pq.paper_id = %s
        """
        return self.execute_query(query, (paper_id,))
