from backend.pipeline.rag_pipeline import query_documents
from backend.intelligence.authenticator import call_llm
from backend.intelligence.prompt_manager import get_explanation_prompt

def chat(question: str, history: list = [], mode: str = "default") -> dict:
    context_chunks = query_documents(question)
    context = "\n".join(context_chunks)

    history_text = ""
    for h in history[-4:]:
        history_text += f"User: {h['question']}\nAssistant: {h['answer']}\n"

    if mode == "default":
        prompt = f"""You are a helpful assistant. Use context and history to answer.

Context:
{context}

Conversation History:
{history_text}

Question: {question}
Answer:"""
    else:
        prompt = get_explanation_prompt(context, question, mode)

    answer = call_llm(prompt)
    return {"question": question, "answer": answer, "sources": context_chunks}