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