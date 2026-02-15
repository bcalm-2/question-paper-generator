import mysql.connector
from mysql.connector import errorcode

# ----------------------------
# Configuration
# ----------------------------
def get_db_config():
    return {
        'user': 'root',
        'password': 'yourpassword',  # UPDATE THIS
        'host': 'localhost',
        'database': DB_NAME
    }

def get_db_connection():
    try:
        config = get_db_config()
        # Remove database key for initial connection if you want to create it
        # but for general use, we assume it exists after init_db()
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to DB: {err}")
        return None

def init_db():
    try:
        # Connect without DB first to create it if it doesn't exist
        temp_config = {
            'user': 'root',
            'password': 'yourpassword',
            'host': 'localhost'
        }
        cnx = mysql.connector.connect(**temp_config)
        cursor = cnx.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")

        for table_name in TABLES:
            try:
                cursor.execute(TABLES[table_name])
                print(f"Table `{table_name}` created successfully.")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    pass # Table already exists
                else:
                    print(f"Error creating table {table_name}: {err.msg}")

        cursor.close()
        cnx.close()
        print("Database initialized successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to initialize database: {err}")

# Users table updated with password
TABLES['users'] = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'teacher', 'student') DEFAULT 'student'
);
"""

# Rest of the tables (adding IF NOT EXISTS for safety)
TABLES['subjects'] = """
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);
"""

TABLES['topics'] = """
CREATE TABLE IF NOT EXISTS topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);
"""

TABLES['questions'] = """
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic_id INT DEFAULT NULL,
    question_text TEXT NOT NULL,
    bloom_level VARCHAR(50) NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    question_type ENUM('MCQ','Descriptive') NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE SET NULL
);
"""

TABLES['papers'] = """
CREATE TABLE IF NOT EXISTS papers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    marks INT NOT NULL,
    duration VARCHAR(50) NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

TABLES['paper_questions'] = """
CREATE TABLE IF NOT EXISTS paper_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paper_id INT NOT NULL,
    question_id INT NOT NULL,
    marks INT DEFAULT 0,
    FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
"""

if __name__ == "__main__":
    init_db()
