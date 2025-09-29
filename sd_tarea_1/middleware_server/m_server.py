from fastapi import FastAPI
from pydantic import BaseModel
from cache_manager import CacheManager
from p_types.types import QA, Gauss
from tests import gauss_tests
import requests
import db

    

app = FastAPI()

def compare_answers(question: str, yahoo_answer: str):
    
    request_data = {
        "question": question,
        "yahoo_answer": yahoo_answer
    }
    
    URL = "http://qa_score:8000"
    
    try:
        # Have to define the URL
        response = requests.post(URL, json=request_data)
        
        if response.status_code != 200:
            raise Exception(f"There is an error. Status code: {response.status_code}")
        
        print("    ↳ Scored successfully")
        
        return response.json()
       
    
    except Exception as e:
        print(f"    ↳ Error scoring it :\n", e)
        return None

def process_request(config: str, idx: int, question: str, yahoo_answer: str):
    
    idx_status = CacheManager.check_cache(config, idx)
    
    if idx_status:
        print(f'[Status] Request with idx "{idx}" already in cache')
        return db.register_cache_hit(config, idx) 
        
    
    db_qa = db.check_qa(config, idx)
    
    if db_qa:
        print(f'[Status] Request with idx "{idx}" already in database')
        
        return CacheManager.save_cache(config, idx, db_qa)

    response = compare_answers(question, yahoo_answer)
    
    if response is None:
        print(f'[Error] Request with idx "{idx}" not processed')
        return
    
    gemini_answer = response["gemini_answer"]
    score = response["score"]
    
    db.save_qa(config, idx, question, yahoo_answer, gemini_answer, score)
    
    data = {
        "question": question,
        "yahoo_answer": yahoo_answer,
        "gemini_answer": gemini_answer,
        "score": score
        }
    
    return CacheManager.save_cache(config, idx, data)
    
def process_gauss_request(gauss_data: Gauss):
    try:
        idx = gauss_data.idx
        question = gauss_data.question
        yahoo_answer = gauss_data.yahoo_answer
        
        for config in gauss_tests:
            print(f'[Status] Processing request with config "{config}" and idx "{idx}"')
            process_request(config, idx, question, yahoo_answer)
        
        message = f'[Status] Request with gauss distribution, and idx "{idx}" processed successfully'
        
        return message

    except Exception as e:
        print(f'[Error] Request with gauss distribution, and idx "{idx}" not processed:\n', e)
        return None

@app.post("/")
def qa_request(request: QA):
    
    try:

        gauss_data = request.gauss
        
        gauss_result = process_gauss_request(gauss_data)

        
        result = {
            "gauss": gauss_result
        }
        
        return result
    
    except Exception as e:
        print(f"[Error] Request not processed:\n", e)
        return None
    
    
    
    
@app.get("/health")
def status():
    return {"status": "ok"}
    
