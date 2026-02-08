import mysql.connector
from mysql.connector import errorcode

# ----------------------------
# Configuration
# ----------------------------
config = {
    'user': 'root',           # your MySQL username
    'password': 'yourpassword',  # your MySQL password
    'host': 'localhost',      # usually localhost
}

DB_NAME = 'project_db'

TABLES = {}

# Users table
TABLES['users'] = """
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('admin', 'teacher', 'student') DEFAULT 'student'
);
"""

# Subjects table
TABLES['subjects'] = """
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);
"""

# Topics table
TABLES['topics'] = """
CREATE TABLE topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);
"""

# Questions table
TABLES['questions'] = """
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic_id INT NOT NULL,
    question_text TEXT NOT NULL,
    bloom_level ENUM('Remember','Understand','Apply','Analyze','Evaluate','Create') NOT NULL,
    difficulty ENUM('Easy','Medium','Hard') NOT NULL,
    question_type ENUM('MCQ','Descriptive') NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);
"""

# Answers table
TABLES['answers'] = """
CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    answer_text TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
"""

# Papers table
TABLES['papers'] = """
CREATE TABLE papers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    created_by INT NOT NULL,
    total_marks INT NOT NULL,
    difficulty ENUM('Easy','Medium','Hard') NOT NULL,
    status ENUM('Draft','Published','Archived') DEFAULT 'Draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
);
"""

# Paper_questions table
TABLES['paper_questions'] = """
CREATE TABLE paper_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paper_id INT NOT NULL,
    question_id INT NOT NULL,
    marks INT NOT NULL,
    question_order INT NOT NULL,
    FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
"""

# ----------------------------
# Connect to MySQL
# ----------------------------
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    print("Connected to MySQL successfully!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# ----------------------------
# Create database
# ----------------------------
try:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    print(f"Database `{DB_NAME}` created or already exists.")
    cursor.execute(f"USE {DB_NAME}")
except mysql.connector.Error as err:
    print(f"Failed creating database: {err}")
    exit(1)

# ----------------------------
# Create tables
# ----------------------------
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        cursor.execute(table_description)
        print(f"Table `{table_name}` created successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print(f"Table `{table_name}` already exists.")
        else:
            print(err.msg)

# ----------------------------
# Test the connection with a simple query
# ----------------------------
try:
    cursor.execute("SELECT NOW() AS current_time;")
    row = cursor.fetchone()
    print(f"Test Query Result: Current Time = {row[0]}")
except mysql.connector.Error as err:
    print(f"Failed to execute test query: {err}")

# Close connection
cursor.close()
cnx.close()
print("MySQL connection closed.")
