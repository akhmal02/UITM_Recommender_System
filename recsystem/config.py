import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "config.env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME", "recsystem")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASS = os.getenv("DB_PASS", "")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "PUT YOUR API KEY HERE (GROK)")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "PUT YOUR API KEY HERE (CHATGPT)")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
