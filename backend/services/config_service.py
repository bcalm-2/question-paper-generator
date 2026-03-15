import os
from infisical_sdk import InfisicalClient

class ConfigService:
    def __init__(self):
        self.client = None
        self.client_id = os.getenv("INFISICAL_CLIENT_ID")
        self.client_secret = os.getenv("INFISICAL_CLIENT_SECRET")
        self.project_id = os.getenv("INFISICAL_PROJECT_ID")
        self.env = os.getenv("FLASK_ENV", "development")
        
        self._initialize_vault()

    def _initialize_vault(self):
        if self.client_id and self.client_secret:
            try:
                self.client = InfisicalClient()
                self.client.auth.universal_auth.login(
                    client_id=self.client_id,
                    client_secret=self.client_secret
                )
                print("Successfully initialized Infisical Vault.")
            except Exception as e:
                print(f"Warning: Failed to connect to Infisical Vault: {e}")
                self.client = None
        else:
            print("Notice: Vault credentials missing. Falling back to environment variables.")

    def get(self, key, default=None):
        """
        Retrieves a secret from the vault. Falls back to environment variables.
        """
        if self.client and self.project_id:
            try:
                # Infisical SDK usually returns a secret object
                secret = self.client.secrets.get_secret(
                    secret_name=key,
                    project_id=self.project_id,
                    environment=self.env
                )
                return secret.secret_value if hasattr(secret, 'secret_value') else secret
            except Exception:
                # Fallback to os.getenv if secret not found in vault or error
                pass
        
        return os.getenv(key, default)

# Singleton instance
config_service = ConfigService()
