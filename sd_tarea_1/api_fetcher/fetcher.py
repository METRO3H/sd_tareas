import os
import json
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = "What is the capital of France?"


try:
    response = model.generate_content(prompt)
    
    data = {
        "prompt": prompt,
        "gemini_response": response.text.strip()
    }
    
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # Leer respuestas existentes si el archivo existe
    responses = []
    if os.path.exists("response.json"):
        with open("response.json", "r", encoding="utf-8") as file:
            try:
                responses = json.load(file)
            except json.JSONDecodeError:
                responses = []

    responses.append(data)

    with open("response.json", "w", encoding="utf-8") as file:
        json.dump(responses, file, indent=2, ensure_ascii=False)

    print("Response saved to response.json")

except Exception as e:
    print(f"Error occurred: {e}")