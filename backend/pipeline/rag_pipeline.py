from backend.parser.smart_parser import smart_parse
from backend.pipeline.chunker import chunk_text
from backend.pipeline.embedder import embed_texts
from backend.pipeline.vector_store import store_chunks, retrieve, doc_exists, clear_all
import os

def ingest_document(file_path: str) -> int:
    # Clear old document before ingesting new one
    clear_all()
    text = smart_parse(file_path)
    doc_id = os.path.splitext(os.path.basename(file_path))[0]
    chunks_data = chunk_text(text, doc_name=doc_id)
    chunks = [c["text"] for c in chunks_data]
    metadata = [c["metadata"] for c in chunks_data]
    embeddings = embed_texts(chunks)
    store_chunks(chunks, embeddings, doc_id, metadata)
    return len(chunks)

def query_documents(query: str) -> list[str]:
    query_embedding = embed_texts([query])[0]
    return retrieve(query_embedding)