from backend.intelligence.authenticator import call_llm
from backend.intelligence.prompt_manager import get_risk_prompt

def score_risk(text: str) -> int:
    prompt = get_risk_prompt(text)
    result = call_llm(prompt, max_tokens=5)
    try:
        return int(result.strip())
    except:
        return 5  # default medium risk