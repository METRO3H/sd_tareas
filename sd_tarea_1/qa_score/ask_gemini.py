from gemini_model import GeminiModel
import os
import random

# --- Pool de modelos ---
# Suponiendo que tienes varias API keys
API_KEYS = [
    os.getenv("GOOGLE_API_KEY_1"),
    os.getenv("GOOGLE_API_KEY_2"),
    os.getenv("GOOGLE_API_KEY_3"),
]

MODEL_NAME = "gemma-3-1b-it"


model_pool = [GeminiModel(api_key, MODEL_NAME, idx + 1) for idx, api_key in enumerate(API_KEYS)]

def ask_gemini(prompt):
    # Toma un modelo aleatorio del pool y hace la request respetando RPM y TPM.

    # Mezclamos el pool para rotación aleatoria
    shuffled_pool = model_pool.copy()
    random.shuffle(shuffled_pool)

    for model in shuffled_pool:
        try:
            response_text = model.generate(prompt)

            # --- Mostrar estado del modelo ---
            rpm = len(model.request_times)
            tkm = sum(tok for _, tok in model.token_requests)
            print(f"[Status] Prompt processed | model: {model.idx} | RPM: {rpm}/30 | TKM: {tkm}/15000 |")

            return response_text
        except Exception as e:
            print(f"Error with model {model.idx}: {e}")
            continue

    raise RuntimeError("Ningún modelo disponible para generar la respuesta")
