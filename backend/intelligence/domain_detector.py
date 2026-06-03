from backend.intelligence.authenticator import call_llm
from backend.intelligence.prompt_manager import get_domain_prompt

def detect_domain(text: str) -> str:
    prompt = get_domain_prompt(text)
    return call_llm(prompt, max_tokens=10).lower()