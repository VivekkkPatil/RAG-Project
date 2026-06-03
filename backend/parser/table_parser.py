from pypdf import PdfReader

def parse_tables(file_path: str) -> str:
    reader = PdfReader(file_path)
    tables_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            tables_text += f"--- Page {i+1} ---\n{text}\n"
    return tables_text.strip()