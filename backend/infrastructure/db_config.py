from infrastructure.config_service import config_service
import mysql.connector
from mysql.connector import errorcode, pooling
from config.db_schema import DB_NAME, TABLES
import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Connection configuration
# ---------------------------------------------------------------------------

def get_db_config() -> dict:
    """
    Assembles the MySQL connection parameters from environment variables.

    Alias resolution is handled by :class:`~infrastructure.config_service.ConfigService`,
    which maps vendor-specific variable names (e.g. ``MYSQLHOST``) to our
    canonical keys.

    Returns:
        dict suitable for passing to ``mysql.connector.connect(**config)``.
    """
    config = {
        "host":     config_service.get("DB_HOST"),
        "user":     config_service.get("DB_USER"),
        "password": config_service.get("DB_PASSWORD"),
        "database": config_service.get("DB_NAME", DB_NAME),
    }
    port = config_service.get("DB_PORT")
    if port:
        config["port"] = int(port)
    return config


# ---------------------------------------------------------------------------
# Connection pool (module-level singleton)
# ---------------------------------------------------------------------------

_db_pool = None


def get_db_pool():
    """
    Lazily initialises and returns the shared MySQL connection pool.

    Returns:
        :class:`~mysql.connector.pooling.MySQLConnectionPool` or ``None``
        if credentials are missing / pool creation fails.
    """
    global _db_pool
    if _db_pool is not None:
        return _db_pool

    config = get_db_config()
    if not all([config.get("host"), config.get("user"), config.get("password")]):
        logger.warning("DB credentials incomplete — pool not created.")
        return None

    try:
        _db_pool = pooling.MySQLConnectionPool(
            pool_name="qpg_pool",
            pool_size=10,
            pool_reset_session=True,
            **config,
        )
        logger.info("DB connection pool created (size=10).")
    except mysql.connector.Error as err:
        logger.error(f"Failed to create DB pool: {err}")
        _db_pool = None

    return _db_pool


def get_db_connection():
    """
    Returns a connection from the pool, falling back to a direct connection.

    Returns:
        :class:`~mysql.connector.connection.MySQLConnection` or ``None``.
    """
    try:
        pool = get_db_pool()
        if pool:
            return pool.get_connection()

        # Graceful fallback for environments without pooling support
        logger.warning("Pool unavailable — using direct DB connection.")
        return mysql.connector.connect(**get_db_config())
    except mysql.connector.Error as err:
        logger.error(f"DB connection error: {err}")
        return None


# ---------------------------------------------------------------------------
# Schema initialisation
# ---------------------------------------------------------------------------

def init_db() -> None:
    """
    Creates the database and all tables if they do not already exist,
    then seeds initial subjects/topics and ensures performance indexes.

    Called once at application startup (guarded against the Werkzeug reloader
    in ``app.py``).
    """
    temp_config = {
        "host":     config_service.get("DB_HOST"),
        "user":     config_service.get("DB_USER"),
        "password": config_service.get("DB_PASSWORD"),
    }
    port = config_service.get("DB_PORT")
    if port:
        temp_config["port"] = int(port)

    if not all(temp_config.values()):
        logger.error("Missing DB credentials — cannot initialise database.")
        return

    try:
        cnx = mysql.connector.connect(**temp_config)
        cursor = cnx.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")

        # Drop and recreate tables for a clean state
        logger.info("Dropping existing tables for reset…")
        for table_name in reversed(list(TABLES.keys())):
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            logger.debug(f"Dropped table `{table_name}`")

        for table_name, ddl in TABLES.items():
            try:
                cursor.execute(ddl)
                logger.info(f"Table `{table_name}` created.")
            except mysql.connector.Error as err:
                logger.error(f"Error creating table {table_name}: {err.msg}")

        _seed_data(cursor)
        _ensure_indexes(cursor)

        cnx.commit()
        cursor.close()
        cnx.close()
        logger.info("Database initialised and seeded successfully.")
    except mysql.connector.Error as err:
        logger.error(f"Database initialisation failed: {err}")


def _seed_data(cursor) -> None:
    """Seeds initial subjects and topics into the database."""
    from config.db_schema import INITIAL_SUBJECT_TOPICS

    for subject_name, topics in INITIAL_SUBJECT_TOPICS.items():
        cursor.execute("SELECT id FROM subjects WHERE name = %s", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO subjects (name) VALUES (%s)", (subject_name,))
            subject_id = cursor.lastrowid
            for topic_name in topics:
                cursor.execute(
                    "INSERT INTO topics (subject_id, name) VALUES (%s, %s)",
                    (subject_id, topic_name),
                )
            logger.info(f"Seeded subject '{subject_name}' with {len(topics)} topics.")


def _ensure_indexes(cursor) -> None:
    """Creates performance indexes if they do not already exist."""
    indexes = [
        ("subjects",        "idx_sub_name",       "name"),
        ("topics",          "idx_topic_name",      "name"),
        ("topics",          "idx_topic_subject",   "subject_id"),
        ("questions",       "idx_q_bloom",         "bloom_level"),
        ("questions",       "idx_q_difficulty",    "difficulty"),
        ("questions",       "idx_question_topic",  "topic_id"),
        ("questions",       "idx_question_type",   "question_type"),
        ("papers",          "idx_p_created",       "created_at"),
        ("papers",          "idx_paper_user",      "user_id"),
        ("papers",          "idx_paper_subject",   "subject_id"),
        ("paper_questions", "idx_pq_paper",        "paper_id"),
        ("paper_questions", "idx_pq_question",     "question_id"),
        ("question_options","idx_opt_question",    "question_id"),
    ]

    for table, idx_name, column in indexes:
        try:
            cursor.execute(f"CREATE INDEX {idx_name} ON {table} ({column})")
            logger.debug(f"Index {idx_name} applied on {table}({column}).")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_KEYNAME:
                logger.debug(f"Index {idx_name} already exists — skipped.")
            else:
                logger.warning(f"Could not apply index {idx_name}: {err.msg}")


if __name__ == "__main__":
    init_db()
