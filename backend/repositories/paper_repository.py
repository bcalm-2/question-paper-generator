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

    def save_batch_questions(self, paper_id, questions_data):
        """
        High-performance save for all questions and options.
        questions_data: list of dicts {text, level, difficulty, type, marks, options}
        """
        if not questions_data:
            return True

        # 1. Batch Insert Questions
        q_query = "INSERT INTO questions (question_text, bloom_level, difficulty, question_type) VALUES (%s, %s, %s, %s)"
        q_params = [(q['text'], q['level'], q['difficulty'], q['type']) for q in questions_data]
        
        # We need the IDs. In MySQL, executemany doesn't return them easily.
        # So we'll use a single multi-row insert string to get LAST_INSERT_ID.
        placeholders = ", ".join(["(%s, %s, %s, %s)"] * len(questions_data))
        flat_q_params = []
        for p in q_params:
            flat_q_params.extend(p)
            
        full_q_query = f"INSERT INTO questions (question_text, bloom_level, difficulty, question_type) VALUES {placeholders}"
        
        conn = self._get_connection()
        if not conn: return False
        
        try:
            cursor = conn.cursor()
            cursor.execute(full_q_query, flat_q_params)
            first_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            # Since IDs are sequential in InnoDB, we can map them
            for i, q in enumerate(questions_data):
                q['id'] = first_id + i

            # 2. Batch Link to Paper
            pq_query = "INSERT INTO paper_questions (paper_id, question_id, marks) VALUES (%s, %s, %s)"
            pq_params = [(paper_id, q['id'], q['marks']) for q in questions_data]
            self.execute_batch(pq_query, pq_params)

            # 3. Batch Insert Options
            all_options = []
            for q in questions_data:
                if 'options' in q:
                    for opt in q['options']:
                        all_options.append((q['id'], opt['text'], opt['is_correct']))
            
            if all_options:
                opt_query = "INSERT INTO question_options (question_id, option_text, is_correct) VALUES (%s, %s, %s)"
                self.execute_batch(opt_query, all_options)
                
            return True
        except Exception as e:
            if conn: conn.close()
            logger.error(f"Failed bulk question save: {e}")
            return False
