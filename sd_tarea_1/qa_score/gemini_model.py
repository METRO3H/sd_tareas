import time
import google.generativeai as genai

WINDOW_SECONDS = 60
MAX_RPM = 30
MAX_TPM = 15000

class GeminiModel:
    def __init__(self, api_key, model_name, idx):
        self.idx = idx
        self.api_key = api_key
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        self.request_times = []  # RPM
        self.token_requests = []  # TPM [[timestamp, tokens]]
        genai.configure(api_key=api_key)

    # --- Rate limiters ---
    def check_rpm(self):
        now = time.time()
        self.request_times = [t for t in self.request_times if now - t < WINDOW_SECONDS]

        if len(self.request_times) >= MAX_RPM:
            sleep_time = WINDOW_SECONDS - (now - self.request_times[0])
            print(f"⏳ {self.model_name} límite RPM alcanzado, esperando {sleep_time:.2f}s...")
            time.sleep(sleep_time)
            now = time.time()
            self.request_times = [t for t in self.request_times if now - t < WINDOW_SECONDS]

        self.request_times.append(time.time())

    def check_tpm(self):
        now = time.time()
        self.token_requests = [[t, tok] for t, tok in self.token_requests if now - t < WINDOW_SECONDS]

        if self.token_requests:
            total_tokens = sum(tok for _, tok in self.token_requests)
            max_tokens_last_minute = max(tok for _, tok in self.token_requests)
        else:
            total_tokens = 0
            max_tokens_last_minute = 0

        if total_tokens + max_tokens_last_minute > MAX_TPM:
            sleep_time = WINDOW_SECONDS - (now - self.token_requests[0][0])
            print(f"⏳ {self.model_name} límite TPM alcanzado, esperando {sleep_time:.2f}s...")
            time.sleep(sleep_time)
            now = time.time()
            self.token_requests = [[t, tok] for t, tok in self.token_requests if now - t < WINDOW_SECONDS]

    def generate(self, prompt):
        self.check_rpm()
        self.check_tpm()

        response = self.model.generate_content(prompt)
        tokens_used = response.usage_metadata.total_token_count
        
        self.token_requests.append([time.time(), tokens_used])
        
        return response.text.strip()
