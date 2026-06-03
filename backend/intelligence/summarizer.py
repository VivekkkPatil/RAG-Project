from backend.intelligence.authenticator import call_llm
from backend.intelligence.prompt_manager import get_summary_prompt

def summarize(text: str) -> str:
    prompt = get_summary_prompt(text)
    return call_llm(prompt)