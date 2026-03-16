from .base_repository import BaseRepository

class SubjectRepository(BaseRepository):
    def get_all(self):
        return self.execute_query("SELECT * FROM subjects ORDER BY name")

    def get_all_with_topics(self):
        """Fetches all subjects and their topics in a single JOIN query."""
        query = """
        SELECT 
            s.id as subject_id, 
            s.name as subject_name, 
            s.description as subject_description,
            t.id as topic_id, 
            t.name as topic_name
        FROM subjects s
        LEFT JOIN topics t ON s.id = t.subject_id
        ORDER BY s.name, t.name
        """
        return self.execute_query(query)

    def get_by_id(self, subject_id):
        result = self.execute_query("SELECT * FROM subjects WHERE id = %s", (subject_id,))
        return result[0] if result else None

    def get_by_name(self, name):
        result = self.execute_query("SELECT * FROM subjects WHERE name = %s", (name,))
        return result[0] if result else None

    def create(self, name, description=""):
        query = "INSERT INTO subjects (name, description) VALUES (%s, %s)"
        return self.execute_query(query, (name, description), commit=True)

    def update(self, subject_id, name, description):
        query = "UPDATE subjects SET name = %s, description = %s WHERE id = %s"
        return self.execute_query(query, (name, description, subject_id), commit=True)

    def delete(self, subject_id):
        return self.execute_query("DELETE FROM subjects WHERE id = %s", (subject_id,), commit=True)


class TopicRepository(BaseRepository):
    def get_by_subject(self, subject_id):
        return self.execute_query("SELECT * FROM topics WHERE subject_id = %s ORDER BY name", (subject_id,))

    def get_by_subject_and_name(self, subject_id, name):
        result = self.execute_query("SELECT * FROM topics WHERE subject_id = %s AND name = %s", (subject_id, name))
        return result[0] if result else None

    def create(self, subject_id, name):
        query = "INSERT INTO topics (subject_id, name) VALUES (%s, %s)"
        return self.execute_query(query, (subject_id, name), commit=True)

    def delete_by_subject(self, subject_id):
        return self.execute_query("DELETE FROM topics WHERE subject_id = %s", (subject_id,), commit=True)

    def delete(self, topic_id):
        return self.execute_query("DELETE FROM topics WHERE id = %s", (topic_id,), commit=True)
