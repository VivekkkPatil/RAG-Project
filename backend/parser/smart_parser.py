import os
from backend.parser.pdf_parser import parse_pdf, is_scanned_pdf
from backend.parser.docx_parser import parse_docx
from backend.parser.ocr_parser import parse_image

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".png", ".jpg", ".jpeg", ".tiff"}

def smart_parse(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    if ext == ".pdf":
        if is_scanned_pdf(file_path):
            print(f"Scanned PDF detected — using OCR")
            return _ocr_pdf(file_path)
        else:
            print(f"Digital PDF detected — extracting text")
            return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    elif ext in {".png", ".jpg", ".jpeg", ".tiff"}:
        return parse_image(file_path)

def _ocr_pdf(file_path: str) -> str:
    from pypdf import PdfReader
    from PIL import Image
    import pytesseract
    import io

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if "/XObject" in page["/Resources"]:
            xobjects = page["/Resources"]["/XObject"].get_object()
            for obj in xobjects:
                xobj = xobjects[obj].get_object()
                if xobj["/Subtype"] == "/Image":
                    data = xobj.get_data()
                    img = Image.open(io.BytesIO(data))
                    text += pytesseract.image_to_string(img) + "\n"
    return text.strip() if text else "Could not extract text from scanned PDF"