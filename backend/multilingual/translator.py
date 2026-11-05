
from deep_translator import GoogleTranslator

def translate_to_english(text: str, source_lang: str = "auto") -> str:
    if not text or not text.strip():
        return text

    # English questions don't need translation
    if source_lang.lower() in ("en", "english"):
        return text

    try:
        return GoogleTranslator(
            source=source_lang,
            target="en"
        ).translate(text) or text
    except Exception as e:
        print(f"Translation warning: {e}")
        return text


def translate_from_english(text: str, target_lang: str = "en") -> str:
    if not text or not text.strip():
        return text

    if target_lang.lower() in ("en", "english"):
        return text

    try:
        return GoogleTranslator(
            source="en",
            target=target_lang
        ).translate(text) or text
    except Exception as e:
        print(f"Translation warning: {e}")
        return text
