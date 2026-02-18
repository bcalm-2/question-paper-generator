import mysql.connector
from mysql.connector import errorcode
from constants import DB_NAME, TABLES

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

if __name__ == "__main__":
    init_db()
