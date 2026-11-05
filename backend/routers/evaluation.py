from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class EvalRequest(BaseModel):
    text: str

class RAGEvalRequest(BaseModel):
    questions: List[str]

@router.post("/evaluate")
def evaluate(request: EvalRequest):
    from backend.intelligence.summarizer import summarize
    from backend.intelligence.domain_detector import detect_domain
    from backend.intelligence.risk_scorer import score_risk
    from backend.intelligence.action_extractor import extract_actions
    from backend.intelligence.faq_generator import generate_faqs
    return {
        "summary": summarize(request.text),
        "domain": detect_domain(request.text),
        "risk_score": score_risk(request.text),
        "actions": extract_actions(request.text),
        "faqs": generate_faqs(request.text)
    }

@router.post("/authenticity")
def authenticity(request: EvalRequest):
    from backend.intelligence.authenticity_checker import check_authenticity
    return check_authenticity(request.text)

@router.post("/rag-evaluate")
def rag_evaluate(request: RAGEvalRequest):
    from backend.evaluation.ragas_eval import run_evaluation
    results = run_evaluation(request.questions)
    return {"results": results}