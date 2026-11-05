from pypdf import PdfReader

def parse_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()

def is_scanned_pdf(file_path: str) -> bool:
    reader = PdfReader(file_path)
    for page in reader.pages:
        text = page.extract_text()
        if text and len(text.strip()) > 20:
            return False
    return True