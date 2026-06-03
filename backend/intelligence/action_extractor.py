from backend.intelligence.authenticator import call_llm
from backend.intelligence.prompt_manager import get_action_prompt

def extract_actions(text: str) -> str:
    prompt = get_action_prompt(text)
    return call_llm(prompt)