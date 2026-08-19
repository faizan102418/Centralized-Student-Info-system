"""Thin client for calling the Groq chat completions API."""

import requests

from chatbot.config import GROQ_API_KEY, GROQ_MODEL

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
SYSTEM_PROMPT = (
    "You are an intelligent assistant that extracts and synthesizes "
    "student records from provided text."
)


def query_groq_api(prompt: str, timeout: int = 30) -> str:
    """Send a prompt to the Groq API and return the model's text response."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 300,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        return f"⚠️ Could not reach the Groq API: {exc}"

    body = response.json()
    try:
        return body["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return f"⚠️ Unexpected response from Groq API: {body}"
