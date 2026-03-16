from db_config import get_db_connection
import time
import logging

logger = logging.getLogger(__name__)

class BaseRepository:
    def __init__(self):
        self._conn = None
        self._cursor = None

    def _get_connection(self):
        return get_db_connection()

    def execute_query(self, query, params=None, commit=False):
        start_time = time.time()
        conn = self._get_connection()
        conn_time = time.time() - start_time
        
        if not conn:
            logger.error(f"Failed to get DB connection (took {conn_time:.2f}s)")
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if commit:
                conn.commit()
                result = cursor.lastrowid
            else:
                result = cursor.fetchall()
            
            end_time = time.time()
            total_time = end_time - start_time
            if total_time > 1.0: # Only log slow queries (>1s) as warnings
                logger.warning(f"SLOW QUERY: {query[:50]}... took {total_time:.2f}s (Conn: {conn_time:.2f}s)")
            else:
                logger.info(f"Query executed in {total_time:.2f}s")
                
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            logger.error(f"Database Error: {e} | Query: {query[:100]}")
            return None

    def execute_batch(self, query, params_list):
        """Executes a single query with multiple sets of parameters (Batch Insert)."""
        if not params_list:
            return True
            
        start_time = time.time()
        conn = self._get_connection()
        conn_time = time.time() - start_time
        
        if not conn:
            logger.error(f"Failed to get DB connection for batch (took {conn_time:.2f}s)")
            return False
            
        try:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            
            end_time = time.time()
            total_time = end_time - start_time
            logger.info(f"Batch query executed ({len(params_list)} rows) in {total_time:.2f}s (Conn: {conn_time:.2f}s)")
            
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            logger.error(f"Batch Database Error: {e} | Query: {query[:100]}")
            return False

    def execute_scalar(self, query, params=None):
        result = self.execute_query(query, params)
        return result[0] if result else None
