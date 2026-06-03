import os
from backend.parser.pdf_parser import parse_pdf
from backend.parser.docx_parser import parse_docx
from backend.parser.ocr_parser import parse_image

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".png", ".jpg", ".jpeg", ".tiff"}

def smart_parse(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    elif ext in {".png", ".jpg", ".jpeg", ".tiff"}:
        return parse_image(file_path)