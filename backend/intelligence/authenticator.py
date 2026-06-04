from groq import Groq
from backend.config import GROQ_API_KEY, LLM_MODEL

client = Groq(api_key=GROQ_API_KEY)

def web_search(query: str) -> str:
    try:
        from ddgs import DDGS
        results = DDGS().text(query, max_results=2, timeout=5)
        return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except:
        return ""

def call_llm(prompt: str, max_tokens: int = 1024) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()