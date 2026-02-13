import os
import json
import google.generativeai as genai


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# You can switch models later without touching logic
MODEL_NAME = "gemini-3-flash-preview"  
# (If you specifically have preview access, use "gemini-1.5-flash-preview")


class AIClientError(Exception):
    pass


def run_policy_analysis(prompt: str) -> dict:
    if not GEMINI_API_KEY:
        raise AIClientError("GEMINI_API_KEY not configured")

    try:
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel(
            MODEL_NAME,
            generation_config={
                "temperature": 0.2,
                "response_mime_type": "application/json"
            }
        )

        response = model.generate_content(prompt)

        # Gemini returns text, we force JSON
        content = response.text.strip()

        return json.loads(content)

    except Exception as e:
        raise AIClientError(f"Gemini AI error: {str(e)}")

def run_comment_reply(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise AIClientError("AI disabled (no API key)")

    try:
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel(
            MODEL_NAME,
            generation_config={
                "temperature": 0.3
            }
        )

        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:
        raise AIClientError(f"Gemini AI error: {str(e)}")
    
