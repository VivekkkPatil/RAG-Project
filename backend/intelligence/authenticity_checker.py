from backend.intelligence.authenticator import call_llm
from backend.intelligence.prompt_manager import get_authenticity_prompt

def check_authenticity(text: str) -> dict:
    prompt = get_authenticity_prompt(text)
    result = call_llm(prompt)
    
    score = 7
    issues = "None found"
    verdict = "Authentic"
    
    for line in result.strip().split("\n"):
        line = line.strip()
        if "Authenticity Score:" in line:
            try:
                score = int(line.split(":")[1].strip().split("/")[0].strip())
            except:
                score = 7
        elif "Issues Found:" in line:
            issues = line.split(":", 1)[1].strip()
        elif "Verdict:" in line:
            verdict = line.split(":", 1)[1].strip()

    # If issues still empty, use full result
    if not issues or issues == "":
        issues = result

    return {"score": score, "issues": issues, "verdict": verdict}