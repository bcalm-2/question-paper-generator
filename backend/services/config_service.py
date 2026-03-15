import os

class ConfigService:
    def __init__(self):
        pass

    def get(self, key, default=None):
        """
        Retrieves a secret from environment variables.
        """
        return os.getenv(key, default)

# Singleton instance
config_service = ConfigService()
