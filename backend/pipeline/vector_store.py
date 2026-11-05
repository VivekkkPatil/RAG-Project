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
            data = pickle.load(f)
        if isinstance(data, dict):
            return index, data.get("docs", []), data.get("metadata", [])
        return index, data, []
    return None, [], []

def store_chunks(chunks: list[str], embeddings: list, doc_id: str, metadata: list = []):
    index, docs, metas = _load()
    vecs = np.array(embeddings, dtype="float32")
    if index is None:
        index = faiss.IndexFlatL2(vecs.shape[1])
    index.add(vecs)
    docs.extend(chunks)
    metas.extend(metadata if metadata else [""] * len(chunks))
    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, "wb") as f:
        pickle.dump({"docs": docs, "metadata": metas}, f)

def retrieve(query_embedding: list, top_k: int = 5) -> list[str]:
    index, docs, metas = _load()
    if index is None or len(docs) == 0:
        return []
    vec = np.array([query_embedding], dtype="float32")
    _, indices = index.search(vec, min(top_k, len(docs)))
    seen = set()
    results = []
    for i in indices[0]:
        if i < len(docs):
            text = docs[i]
            if text not in seen:
                seen.add(text)
                meta = metas[i] if i < len(metas) else ""
                results.append(f"{meta}\n{text}" if meta else text)
    return results

def doc_exists(doc_id: str) -> bool:
    _, docs, _ = _load()
    return any(doc_id in str(d) for d in docs)

def clear_all():
    if os.path.exists(INDEX_PATH):
        os.remove(INDEX_PATH)
    if os.path.exists(DOCS_PATH):
        os.remove(DOCS_PATH)