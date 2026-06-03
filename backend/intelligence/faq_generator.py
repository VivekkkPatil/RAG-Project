from backend.intelligence.authenticator import call_llm
from backend.intelligence.prompt_manager import get_faq_prompt

def generate_faqs(text: str) -> str:
    prompt = get_faq_prompt(text)
    return call_llm(prompt)