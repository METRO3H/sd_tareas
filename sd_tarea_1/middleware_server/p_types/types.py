from pydantic import BaseModel

class Gauss(BaseModel):
    idx: int
    question: str
    yahoo_answer: str

class Zipf(BaseModel):
    idx: int
    question: str
    yahoo_answer: str

class QA(BaseModel):
    gauss: Gauss
    zipf: Zipf
