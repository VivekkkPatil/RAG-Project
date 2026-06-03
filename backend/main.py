from fastapi import FastAPI
from backend.routers import document, query, chatbot, evaluation

app = FastAPI(title="RAG Chatbot API")

app.include_router(document.router, prefix="/document", tags=["Document"])
app.include_router(query.router, prefix="/rag", tags=["RAG"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(evaluation.router, prefix="/eval", tags=["Evaluation"])

@app.get("/")
def root():
    return {"status": "RAG API is running"}