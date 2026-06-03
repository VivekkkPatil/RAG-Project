import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def parse_image(file_path: str) -> str:
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text.strip()