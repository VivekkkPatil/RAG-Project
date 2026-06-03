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