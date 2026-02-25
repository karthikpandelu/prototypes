from fastapi import FastAPI
from pydantic import BaseModel
from services.rag_service import answer_question

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    return answer_question(request.question)
