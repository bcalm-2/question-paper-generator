from __future__ import annotations

"""
Database schema definitions and seed data.

This module owns everything that describes *how the database is structured*
and *what goes into it on first run*:

* ``DB_NAME``               — default database name (overridable via env var)
* ``TABLES``                — ordered dict of table-name → CREATE TABLE DDL
* ``INITIAL_SUBJECT_TOPICS``— seed data inserted on first :func:`~infrastructure.db_config.init_db` run
"""

from infrastructure.config_service import config_service

# ---------------------------------------------------------------------------
# Database name
# ---------------------------------------------------------------------------
DB_NAME: str = config_service.get("DB_NAME", "question_paper_gen")

# ---------------------------------------------------------------------------
# Table definitions (in dependency/creation order)
# ---------------------------------------------------------------------------
TABLES: dict[str, str] = {}

TABLES["users"] = """
CREATE TABLE IF NOT EXISTS users (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    email    VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
"""

TABLES["subjects"] = """
CREATE TABLE IF NOT EXISTS subjects (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    description TEXT,
    INDEX (name)
);
"""

TABLES["topics"] = """
CREATE TABLE IF NOT EXISTS topics (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    name       VARCHAR(100) NOT NULL,
    INDEX (name),
    INDEX idx_topic_subject (subject_id)
);
"""

TABLES["questions"] = """
CREATE TABLE IF NOT EXISTS questions (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    topic_id      INT DEFAULT NULL,
    question_text TEXT NOT NULL,
    bloom_level   VARCHAR(50) NOT NULL,
    difficulty    VARCHAR(50) NOT NULL,
    question_type ENUM('MCQ','Descriptive') NOT NULL,
    INDEX (bloom_level),
    INDEX (difficulty),
    INDEX idx_question_topic (topic_id),
    INDEX idx_question_type  (question_type)
);
"""

TABLES["papers"] = """
CREATE TABLE IF NOT EXISTS papers (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL,
    subject_id INT NOT NULL,
    title      VARCHAR(255) NOT NULL,
    marks      INT NOT NULL,
    duration   VARCHAR(50) NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (created_at),
    INDEX idx_paper_user    (user_id),
    INDEX idx_paper_subject (subject_id)
);
"""

TABLES["paper_questions"] = """
CREATE TABLE IF NOT EXISTS paper_questions (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    paper_id    INT NOT NULL,
    question_id INT NOT NULL,
    marks       INT DEFAULT 0,
    INDEX idx_pq_paper    (paper_id),
    INDEX idx_pq_question (question_id)
);
"""

TABLES["question_options"] = """
CREATE TABLE IF NOT EXISTS question_options (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_text TEXT NOT NULL,
    is_correct  BOOLEAN DEFAULT FALSE,
    INDEX idx_opt_question (question_id)
);
"""

# ---------------------------------------------------------------------------
# Seed data — inserted once on first init_db() run
# ---------------------------------------------------------------------------
INITIAL_SUBJECT_TOPICS: dict[str, list[str]] = {
    "DBMS": [
        "Normalization", "ER Model", "Transactions", "SQL",
        "Indexing", "Relational Algebra", "NoSQL", "Query Optimization",
    ],
    "OS": [
        "Processes", "Memory Management", "Deadlocks", "Scheduling",
        "File Systems", "Virtual Memory", "Threads", "Distributed Systems",
    ],
    "CN": [
        "OSI Model", "TCP/IP", "Routing", "Network Security",
        "DNS", "HTTP/HTTPS", "Socket Programming", "Wireless Networks",
    ],
    "DSA": [
        "Arrays", "Linked Lists", "Trees", "Graphs",
        "Dynamic Programming", "Sorting", "Searching", "Recursion",
    ],
    "AI": [
        "Search Algorithms", "Neural Networks", "ML Basics",
        "NLP", "Robotics", "Expert Systems", "Fuzzy Logic",
    ],
}
