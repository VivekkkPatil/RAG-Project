from backend.parser.smart_parser import smart_parse
from backend.pipeline.chunker import chunk_text
from backend.pipeline.embedder import embed_texts
from backend.pipeline.vector_store import store_chunks, retrieve
import os

def ingest_document(file_path: str) -> int:
    text = smart_parse(file_path)
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)
    doc_id = os.path.splitext(os.path.basename(file_path))[0]
    store_chunks(chunks, embeddings, doc_id)
    return len(chunks)

def query_documents(query: str) -> list[str]:
    query_embedding = embed_texts([query])[0]
    return retrieve(query_embedding)