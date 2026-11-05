
from backend.pipeline.rag_pipeline import query_documents
from backend.intelligence.authenticator import call_llm
from backend.intelligence.prompt_manager import get_explanation_prompt


def chat(question: str, history: list = None, mode: str = "default") -> dict:

    if history is None:
        history = []

    # Retrieve relevant information from uploaded documents
    context_chunks = query_documents(question)
    context = "\n".join(context_chunks)

    # Prepare recent conversation history
    history_text = ""

    for h in history[-4:]:
        history_text += (
            f"User: {h['question']}\n"
            f"Assistant: {h['answer']}\n"
        )

    # Generate answer based on selected mode
    if mode == "default":

        prompt = f"""You are DocuSimple, a concise AI document assistant.

Answer the user's question using the provided document context.

Rules:
- Keep answers short and direct.
- Use simple, easy-to-understand language.
- Answer in 3-5 sentences maximum unless more detail is requested.
- Use bullet points only when necessary.
- Do not repeat information.
- Do not add unnecessary introductions or conclusions.
- If the answer is not available in the document, clearly say so.
- Never invent facts.

Document Context:
{context}

Conversation History:
{history_text}

Question:
{question}

Answer:"""

    else:
        prompt = get_explanation_prompt(
            context,
            question,
            mode
        )

    # Generate final answer
    answer = call_llm(prompt)

    # Return only question and answer
    return {
        "question": question,
        "answer": answer
    }
