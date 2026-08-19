"""Centralized configuration loaded from environment variables (.env)."""

import os

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    """Fetch a required environment variable or raise a clear error."""
    value = os.getenv(name)
    if not value:
        raise ValueError(
            f"{name} is missing. Copy .env.example to .env and set {name}."
        )
    return value


# --- Groq / LLM configuration ---
GROQ_API_KEY = _require("GROQ_API_KEY")
# Groq periodically deprecates older models. If this default stops working,
# check https://console.groq.com/docs/models for the current recommendation
# and override it via the GROQ_MODEL env var instead of editing code.
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# --- MySQL configuration ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = _require("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "project_data")
