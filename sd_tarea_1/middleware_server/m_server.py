from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import db

class QA(BaseModel):
    idx: int
    question: str
    yahoo_answer: str
    

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

def process_request(table_name: str, idx: int, question: str, yahoo_answer: str):
    
    idx_status = db.check_qa(table_name, idx)
    
    if idx_status:
        print(f'[Status] Request with idx "{idx}" already processed')
        return
    
    response = compare_answers(question, yahoo_answer)
    
    if response is None:
        print(f'[Error] Request with idx "{idx}" not processed')
        return
    
    gemini_answer = response["gemini_answer"]
    score = response["score"]
    
    db.save_qa(table_name, idx, question, yahoo_answer, gemini_answer, score)
    
    
    return 

@app.post("/")
def qa_request(request: QA):
    
    try:
        
        idx = request.idx
        question = request.question
        yahoo_answer = request.yahoo_answer
        
        process_request("qa_yahoo", idx, question, yahoo_answer)
        
        message = f'[Status] Request with idx "{idx}" processed successfully'
        
        return message
    
    except Exception as e:
        print(f"[Error] Request not processed:\n", e)
        return None
    
    
    
    
    
    
