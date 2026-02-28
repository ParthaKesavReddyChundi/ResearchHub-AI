import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

MODEL_CONFIG = {
    "model": "llama-3.3-70b-versatile",
    "temperature": 0.3,
    "max_tokens": 2000,
}

def call_llm(messages):
    if not messages:
        raise ValueError("messages parameter cannot be empty")
    
    try:
        response = client.chat.completions.create(
            messages=messages,
            **MODEL_CONFIG
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"LLM API call failed: {str(e)}")