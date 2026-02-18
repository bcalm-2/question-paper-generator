# Database Configuration
DB_NAME = "question_paper_gen"

# Database Tables
TABLES = {}

TABLES['users'] = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'teacher', 'student') DEFAULT 'student'
);
"""

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

# Application Config
SUBJECT_TOPICS = {
    "DBMS": ["Normalization", "ER Model", "Transactions", "SQL", "Indexing", "Relational Algebra", "NoSQL", "Query Optimization"],
    "OS": ["Processes", "Memory Management", "Deadlocks", "Scheduling", "File Systems", "Virtual Memory", "Threads", "Distributed Systems"],
    "CN": ["OSI Model", "TCP/IP", "Routing", "Network Security", "DNS", "HTTP/HTTPS", "Socket Programming", "Wireless Networks"],
    "DSA": ["Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming", "Sorting", "Searching", "Recursion"],
    "AI": ["Search Algorithms", "Neural Networks", "ML Basics", "NLP", "Robotics", "Expert Systems", "Fuzzy Logic"]
}

BLOOMS = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]

# Bloom Verb Mapping
BLOOM_VERBS = {
    "Remember": ["define", "list", "recall", "identify", "state"],
    "Understand": ["explain", "describe", "summarize", "interpret"],
    "Apply": ["solve", "use", "implement", "execute", "calculate"],
    "Analyze": ["compare", "differentiate", "analyze", "examine"],
    "Evaluate": ["justify", "critique", "evaluate", "assess"],
    "Create": ["design", "formulate", "create", "develop", "construct"]
}

# Bloom Priority (High to Low)
BLOOM_PRIORITY = [
    "Create",
    "Evaluate",
    "Analyze",
    "Apply",
    "Understand",
    "Remember"
]
