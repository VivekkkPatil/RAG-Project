from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class HistoryItem(BaseModel):
    question: str
    answer: str

class QueryRequest(BaseModel):
    question: str
    lang: str = "en"
    history: List[HistoryItem] = []
    mode: str = "default"

@router.post("/query")
def query(request: QueryRequest):
    from backend.chatbot.general_chat import chat
    from backend.multilingual.translator import translate_to_english, translate_from_english
    question = translate_to_english(request.question)
    history = [h.dict() for h in request.history]
    result = chat(question, history, request.mode)
    result["answer"] = translate_from_english(result["answer"], request.lang)
    return result