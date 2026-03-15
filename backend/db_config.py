from services.config_service import config_service
import mysql.connector
from mysql.connector import errorcode
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

def get_db_connection():
    try:
        config = get_db_config()
        if not all([config['host'], config['user'], config['password']]):
            print("Error: Missing database credentials in environment variables.")
            return None
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to DB: {err}")
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
