import os
import json
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemma-3-1b-it")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        
        return response.text.strip()

    except Exception as e:
        print(f"Error occurred: {e}")
        return None