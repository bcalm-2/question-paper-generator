import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

class ConfigService:
    def __init__(self):
        # Mapping common DB naming conventions to our internal keys
        self.mappings = {
            "DB_HOST": ["MYSQLHOST", "DATABASE_HOST", "DB_HOST"],
            "DB_USER": ["MYSQLUSER", "DATABASE_USER", "DB_USER"],
            "DB_PASSWORD": ["MYSQLPASSWORD", "DATABASE_PASSWORD", "DB_PASSWORD"],
            "DB_NAME": ["MYSQLDATABASE", "MYSQL_DATABASE", "DATABASE_NAME", "DB_NAME"],
            "DB_PORT": ["MYSQLPORT", "DATABASE_PORT", "DB_PORT"]
        }

    def get(self, key, default=None):
        """
        Retrieves a secret from environment variables with mapping support.
        """
        # Check if the key has defined aliases
        if key in self.mappings:
            for alias in self.mappings[key]:
                val = os.getenv(alias)
                if val:
                    return val
        
        # Fallback to direct lookup
        return os.getenv(key, default)

# Singleton instance
config_service = ConfigService()
