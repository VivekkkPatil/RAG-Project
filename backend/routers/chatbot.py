from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime

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

    prompt = f"""You are a friendly helpful AI assistant. Be natural and concise.
Today's date and time is: {datetime.now().strftime("%A, %d %B %Y, %I:%M %p")}
{f"Previous conversation:{chr(10)}{history_text}" if history_text else ""}
User: {request.message}
Assistant:"""

    response = call_llm(prompt)
    return {"response": response}

@router.post("/chat/stream")
def stream_chat(request: ChatRequest):
    from groq import Groq
    from backend.config import GROQ_API_KEY, LLM_MODEL
    from backend.intelligence.authenticator import web_search

    messages = [
        {"role": "system", "content": f"""You are a friendly helpful AI assistant. Be natural and concise.
Today's date and time is: {datetime.now().strftime("%A, %d %B %Y, %I:%M %p")}"""}
    ]

    for h in request.history[-4:]:
        messages.append({"role": "user", "content": h.question})
        messages.append({"role": "assistant", "content": h.answer})

    search_keywords = ["president", "prime minister", "ceo", "current", "latest",
                       "today", "now", "recent", "2024", "2025", "who is", "winner"]

    user_message = request.message
    if any(k in user_message.lower() for k in search_keywords):
        results = web_search(user_message)
        if results:
            user_message += f"\n\nWeb search results:\n{results}\n\nUse these to answer accurately."

    messages.append({"role": "user", "content": user_message})

    def generate():
        client = Groq(api_key=GROQ_API_KEY)
        stream = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            stream=True,
            max_tokens=1024
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    return StreamingResponse(generate(), media_type="text/plain")

@router.post("/voice-input")
def voice_input():
    from backend.voice.speech_to_text import listen
    text = listen()
    return {"transcribed": text}

@router.post("/voice-output")
def voice_output(request: ChatRequest):
    from backend.voice.text_to_speech import speak
    speak(request.message)
    return {"status": "spoken"}