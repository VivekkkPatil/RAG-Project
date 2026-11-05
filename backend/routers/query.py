
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()


class HistoryItem(BaseModel):
    question: str
    answer: str


class QueryRequest(BaseModel):
    question: str
    lang: str = "en"
    history: List[HistoryItem] = Field(default_factory=list)
    mode: str = "default"


@router.post("/query")
def query(request: QueryRequest):
    from backend.chatbot.general_chat import chat
    from backend.multilingual.translator import (
        translate_to_english,
        translate_from_english
    )

    lang = (request.lang or "en").lower()

    # Avoid unnecessary Google Translate requests for English
    if lang in ("en", "english"):
        question = request.question
    else:
        question = translate_to_english(request.question)

    history = [h.dict() for h in request.history]

    result = chat(question, history, request.mode)

    result["answer"] = translate_from_english(
        result["answer"],
        lang
    )

    return result
