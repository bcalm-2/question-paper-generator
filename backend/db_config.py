from services.config_service import config_service
import mysql.connector
from mysql.connector import errorcode, pooling
from constants import DB_NAME, TABLES

# ----------------------------
# Configuration
# ----------------------------
def get_db_config():
    config = {
        'host': config_service.get("DB_HOST"),
        'user': config_service.get("DB_USER"),
        'password': config_service.get("DB_PASSWORD"),
        'database': config_service.get("DB_NAME", DB_NAME)
    }
    
    port = config_service.get("DB_PORT")
    if port:
        config['port'] = int(port)
        
    return config

# Global Pool Instance
_db_pool = None

def get_db_pool():
    global _db_pool
    if _db_pool is None:
        config = get_db_config()
        if not all([config.get('host'), config.get('user'), config.get('password')]):
            return None
            
        try:
            _db_pool = pooling.MySQLConnectionPool(
                pool_name="qpg_pool",
                pool_size=5,  # Reduced for local/Railway limits
                pool_reset_session=True,
                **config
            )
            print(f"Created DB connection pool with size 5")
        except mysql.connector.Error as err:
            print(f"Error creating DB pool: {err}")
            return None
    return _db_pool

def get_db_connection():
    try:
        pool = get_db_pool()
        if pool:
            return pool.get_connection()
            
        # Fallback to direct connection if pool fails
        config = get_db_config()
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(f"Error getting connection: {err}")
        return None

def init_db():
    try:
        # Connect without DB first to create it if it doesn't exist
        temp_config = {
            'host': config_service.get("DB_HOST"),
            'user': config_service.get("DB_USER"),
            'password': config_service.get("DB_PASSWORD")
        }
        
        port = config_service.get("DB_PORT")
        if port:
            temp_config['port'] = int(port)
        
        if not all(temp_config.values()):
            print("Error: Missing database credentials for initialization.")
            return

        cnx = mysql.connector.connect(**temp_config)
        cursor = cnx.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")

        # Tables will be created if they don't exist

        for table_name in TABLES:
            try:
                cursor.execute(TABLES[table_name])
                print(f"Table `{table_name}` created successfully.")
            except mysql.connector.Error as err:
                print(f"Error creating table {table_name}: {err.msg}")

        # Seed initial data
        from constants import INITIAL_SUBJECT_TOPICS
        for subject_name, topics in INITIAL_SUBJECT_TOPICS.items():
            # Check if subject exists
            cursor.execute("SELECT id FROM subjects WHERE name = %s", (subject_name,))
            subject = cursor.fetchone()
            if not subject:
                cursor.execute("INSERT INTO subjects (name) VALUES (%s)", (subject_name,))
                subject_id = cursor.lastrowid
                print(f"Seeded subject: {subject_name}")
                for topic_name in topics:
                    cursor.execute("INSERT INTO topics (subject_id, name) VALUES (%s, %s)", (subject_id, topic_name))
                print(f"Seeded {len(topics)} topics for {subject_name}")

        cnx.commit()
        cursor.close()
        cnx.close()
        print("Database initialized and seeded successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to initialize database: {err}")

if __name__ == "__main__":
    init_db()
