from backend.chatbot.general_chat import chat
from backend.intelligence.authenticator import call_llm

def score_answer(question: str, answer: str, context: str) -> dict:
    faithfulness_prompt = f"""Rate how faithful this answer is to the context (1-10).
Context: {context}
Answer: {answer}
Reply with just a number."""

    relevancy_prompt = f"""Rate how relevant this answer is to the question (1-10).
Question: {question}
Answer: {answer}
Reply with just a number."""

    try:
        f = int(call_llm(faithfulness_prompt, max_tokens=5).strip())
    except:
        f = 5
    try:
        r = int(call_llm(relevancy_prompt, max_tokens=5).strip())
    except:
        r = 5

    return {"faithfulness": f, "answer_relevancy": r, "overall": round((f + r) / 2, 1)}

def run_evaluation(questions: list[str]) -> list[dict]:
    results = []
    for q in questions:
        result = chat(q)
        scores = score_answer(q, result["answer"], "\n".join(result["sources"]))
        results.append({"question": q, "answer": result["answer"], "scores": scores})
    return results