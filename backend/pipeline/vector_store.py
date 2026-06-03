import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "./data/chroma_db/faiss.index"
DOCS_PATH = "./data/chroma_db/docs.pkl"

def _load():
    if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(DOCS_PATH, "rb") as f:
            docs = pickle.load(f)
    else:
        index = None
        docs = []
    return index, docs

def store_chunks(chunks: list[str], embeddings: list, doc_id: str):
    index, docs = _load()
    vecs = np.array(embeddings, dtype="float32")
    if index is None:
        index = faiss.IndexFlatL2(vecs.shape[1])
    index.add(vecs)
    docs.extend(chunks)
    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, "wb") as f:
        pickle.dump(docs, f)

def retrieve(query_embedding: list, top_k: int = 5) -> list[str]:
    index, docs = _load()
    if index is None or len(docs) == 0:
        return []
    vec = np.array([query_embedding], dtype="float32")
    _, indices = index.search(vec, min(top_k, len(docs)))
    return [docs[i] for i in indices[0] if i < len(docs)]