from backend.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str, doc_name: str = "document") -> list[dict]:
    words = text.split()
    chunks = []
    start = 0
    chunk_num = 1
    while start < len(words):
        end = start + CHUNK_SIZE
        chunk = " ".join(words[start:end])
        chunks.append({
            "text": chunk,
            "metadata": f"[{doc_name} | Chunk {chunk_num}]"
        })
        start += CHUNK_SIZE - CHUNK_OVERLAP
        chunk_num += 1
    return chunks