from fastapi import FastAPI
from pydantic import BaseModel
from services.rag_service import answer_question
from services.ingestion import ingest_document
from fastapi import BackgroundTasks

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    return answer_question(request.question)

class IngestRequest(BaseModel):
    document_id: str
    source: str
    content: str

@app.post("/ingest")
def ingest(request: IngestRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        ingest_document,
        request.document_id,
        request.source,
        request.content
    )
    return {"status": "Ingestion started"}