from fastapi import FastAPI
from pydantic import BaseModel
from ask_gemini import ask_gemini
from score_answer import score_answer
import json
class QA(BaseModel):
    question: str
    yahoo_answer: str
    

app = FastAPI()

@app.post("/")
def qa_request(request: QA):
    
    question = request.question
    yahoo_answer = request.yahoo_answer
    
    gemini_answer = ask_gemini(question)
    
    score = score_answer(yahoo_answer, gemini_answer)
    
    
    response = {
            "question": question,
            "yahoo_answer": yahoo_answer, 
            "gemini_answer": gemini_answer, 
            "score": score
        }
    
    response_json = json.dumps(response, indent=4, ensure_ascii=False)
    print(response_json)
    
    return response
    
    
