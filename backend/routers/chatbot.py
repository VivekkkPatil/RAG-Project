from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class HistoryItem(BaseModel):
    question: str
    answer: str

class ChatRequest(BaseModel):
    message: str
    history: List[HistoryItem] = []

@router.post("/chat")
def general_chat(request: ChatRequest):
    from backend.intelligence.authenticator import call_llm

    history_text = ""
    for h in request.history:
        history_text += f"User: {h.question}\nAssistant: {h.answer}\n"

    prompt = f"""You are a helpful assistant with memory of the conversation.

Previous conversation:
{history_text}
User: {request.message}
Assistant:"""

    response = call_llm(prompt)
    return {"response": response}