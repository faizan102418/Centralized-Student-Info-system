# 5. Function to call the Groq API with a prompt.
import requests

from config import GROQ_API_KEY


def query_groq_api(query):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",  # Adjust the model if needed.
        "messages": [
            {"role": "system", "content": "You are an intelligent assistant that extracts and synthesizes student records from provided text."},
            {"role": "user", "content": query}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }
    
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    
    # Uncomment the next line for debugging raw response:
    
    # print("\n🔹 Raw API Response:\n", response.json())
    
    return response.json()["choices"][0]["message"]["content"]