import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/API.env")


class Config:
    OPENAI_API_KEY = os.getenv("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")
