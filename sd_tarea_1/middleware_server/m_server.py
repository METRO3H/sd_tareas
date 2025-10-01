from fastapi import FastAPI, HTTPException
from cache_manager import CacheManager
from p_types.types import QA, Gauss, Zipf
from tests import gauss_tests, zipf_tests
import random
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

def process_request(config: str, idx: int, question: str, yahoo_answer: str, gemini_answer: str, score: int):
    
    idx_status = CacheManager.check_cache(config, idx)
    
    if idx_status:
        print(f'[Status] Request with idx "{idx}" already in cache')
        db.register_cache_event(config, idx, 'hit')
        
        return gemini_answer, score
    
        
    
    db_qa = db.check_qa(config, idx)
    
    if db_qa:
        print(f'[Status] Request with idx "{idx}" already in database')
        
        db.register_cache_event(config, idx, 'miss')
        
        CacheManager.save_cache(config, idx, db_qa)
        
        return gemini_answer, score

    if not gemini_answer and score < 0 :
        response = compare_answers(question, yahoo_answer)
        
        if response is None:
            print(f'[Error] Request with idx "{idx}" not processed')
            return gemini_answer, score
        
        gemini_answer = response["gemini_answer"]
        score = response["score"]
    
    
    db.save_qa(config, idx, question, yahoo_answer, gemini_answer, score)
    
    data = {
        "question": question,
        "yahoo_answer": yahoo_answer,
        "gemini_answer": gemini_answer,
        "score": score
        }
    
    CacheManager.save_cache(config, idx, data)
    
    return gemini_answer, score
    
def process_gauss_request(gauss_data: Gauss):
    try:
        idx = gauss_data.idx
        question = gauss_data.question
        yahoo_answer = gauss_data.yahoo_answer
        
        gemini_answer = ""
        score = -1
        for config in gauss_tests:
            print(f'[Status] Processing request with config "{config}" and idx "{idx}"')
            gemini_answer, score = process_request(config, idx, question, yahoo_answer, gemini_answer, score)
        
        message = f'[Status] Request with gauss distribution, and idx "{idx}" processed successfully'
        
        return message

    except Exception as e:
        print(f'[Error] Request with gauss distribution, and idx "{idx}" not processed:\n', e)
        return None

def process_zipf_request(zipf_data: Zipf):
    try:
        idx = zipf_data.idx
        question = zipf_data.question
        yahoo_answer = zipf_data.yahoo_answer
        
        gemini_answer = ""
        score = -1
        for config in zipf_tests:
            print(f'[Status] Processing request with config "{config}" and idx "{idx}"')
            gemini_answer, score = process_request(config, idx, question, yahoo_answer, gemini_answer, score)

        message = f'[Status] Request with zipf distribution, and idx "{idx}" processed successfully'

        return message

    except Exception as e:
        print(f'[Error] Request with zipf distribution, and idx "{idx}" not processed:\n', e)
        return None


@app.post("/")
def qa_request(request: QA):
    
    try:

        gauss_data = request.gauss
        zipf_data  = request.zipf
        
        gauss_result = process_gauss_request(gauss_data)
        zipf_result  = process_zipf_request(zipf_data)
    
        if not gauss_result:
            raise Exception("There was an error processing the gauss request")
    
        if not zipf_result:
            raise Exception("There was an error processing the zipf request")
        
        result = {
            "gauss": gauss_result,
            "zipf": zipf_result
        }
        
        return result
    
    except Exception as e:
        print(f"[Error] Request not processed:\n", e)
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
@app.get("/health")
def status():
    return {"status": "ok"}
    
