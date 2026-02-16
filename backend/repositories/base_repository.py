from db_config import get_db_connection

class BaseRepository:
    def __init__(self):
        self._conn = None
        self._cursor = None

    def _get_connection(self):
        return get_db_connection()

    def execute_query(self, query, params=None, commit=False):
        conn = self._get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if commit:
                conn.commit()
                result = cursor.lastrowid
            else:
                result = cursor.fetchall()
                
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            print(f"Database Error: {e}")
            return None

    def execute_scalar(self, query, params=None):
        result = self.execute_query(query, params)
        return result[0] if result else None
