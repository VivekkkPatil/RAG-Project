def get_rag_prompt(context: str, question: str) -> str:
    return f"""You are a helpful assistant. Use the context below to answer the question.
If the answer is not in the context, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:"""

def get_summary_prompt(text: str) -> str:
    return f"Summarize the following text in 3-5 sentences:\n\n{text}"

def get_domain_prompt(text: str) -> str:
    return f"""Classify the domain of this text. Reply with ONE word only.
Options: legal, medical, finance, technology, education, general

Text: {text[:300]}

Domain:"""

def get_risk_prompt(text: str) -> str:
    return f"""Rate the risk/sensitivity of this content from 1-10.
1 = completely safe, 10 = highly sensitive.
Reply with just a number.

Text: {text[:300]}

Risk score:"""

def get_action_prompt(text: str) -> str:
    return f"""Extract action items from this text as a bullet list.
If none, say "No action items found."

Text: {text}

Action items:"""

def get_faq_prompt(text: str) -> str:
    return f"""Generate 3 FAQs with answers based on this text.
Format: Q: ... A: ...

Text: {text}

FAQs:"""

def get_explanation_prompt(context: str, question: str, mode: str) -> str:
    modes = {
        "simple": "Explain this in very simple plain language anyone can understand.",
        "key_points": "Give only the key points as a short bullet list.",
        "worry_about": "What should the user be worried about or watch out for in this?",
        "action_items": "What does the user need to do? List only action items.",
        "eli5": "Explain this like I am 5 years old. Use very simple words and analogies."
    }
    instruction = modes.get(mode, "Answer the question clearly.")
    return f"""{instruction}

Context:
{context}

Question: {question}

Answer:"""

def get_confidence_prompt(question: str, answer: str, context: str) -> str:
    return f"""Rate how confident you are in this answer based on the context provided.
Reply with just a number from 1-10.
10 = answer is fully supported by context
1 = answer is mostly guessed

Question: {question}
Answer: {answer}
Context: {context[:500]}

Confidence score:"""

def get_authenticity_prompt(text: str) -> str:
    return f"""Analyze this document for internal contradictions, inconsistencies, or suspicious patterns.
Look for:
- Contradicting statements
- Inconsistent dates, numbers, or names
- Unusual clauses or hidden conditions
- Signs of tampering or manipulation

Document:
{text[:2000]}

Respond in this format:
Authenticity Score: X/10 (10 = fully authentic)
Issues Found: (list any problems or "None found")
Verdict: (Authentic / Suspicious / Likely Tampered)"""