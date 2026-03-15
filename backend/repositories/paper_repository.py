from .base_repository import BaseRepository

class PaperRepository(BaseRepository):
    def get_all(self, user_id):
        query = """
        SELECT p.*, s.name as subject 
        FROM papers p
        JOIN subjects s ON p.subject_id = s.id
        WHERE p.user_id = %s 
        ORDER BY p.created_at DESC
        """
        return self.execute_query(query, (user_id,))

    def get_by_id(self, paper_id):
        query = """
        SELECT p.*, s.name as subject 
        FROM papers p
        JOIN subjects s ON p.subject_id = s.id
        WHERE p.id = %s
        """
        result = self.execute_query(query, (paper_id,))
        return result[0] if result else None

    def create_paper(self, user_id, subject_id, title, marks, duration, difficulty):
        query = "INSERT INTO papers (user_id, subject_id, title, marks, duration, difficulty) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (user_id, subject_id, title, marks, duration, difficulty)
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

    def update_paper(self, paper_id, subject_id, title, marks, duration, difficulty):
        query = "UPDATE papers SET subject_id = %s, title = %s, marks = %s, duration = %s, difficulty = %s WHERE id = %s"
        params = (subject_id, title, marks, duration, difficulty, paper_id)
        return self.execute_query(query, params, commit=True)

    def add_question_option(self, question_id, text, is_correct):
        query = "INSERT INTO question_options (question_id, option_text, is_correct) VALUES (%s, %s, %s)"
        params = (question_id, text, is_correct)
        return self.execute_query(query, params, commit=True)

    def get_options_by_question_id(self, question_id):
        return self.execute_query("SELECT * FROM question_options WHERE question_id = %s", (question_id,))
