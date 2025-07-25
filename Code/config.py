# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in your .env file. Please set it accordingly.")

# --- New MySQL Configuration ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root") # Your MySQL root user or a dedicated user
DB_PASSWORD = os.getenv("DB_PASSWORD") # The password you set for the root user
DB_NAME = os.getenv("DB_NAME", "project_data") # Your database name

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD is missing in your .env file. Please set it accordingly.")