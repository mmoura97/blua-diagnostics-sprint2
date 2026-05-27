from __future__ import annotations
from pathlib import Path
from typing import List, Dict
from src.config import settings

def load_documents(kb_dir: str | None = None) -> List[Dict]:
    kb = Path(kb_dir or settings.knowledge_base_dir)
    docs = []
    for path in sorted(kb.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        docs.append({"id": path.stem, "path": str(path), "content": text})
    return docs

def chunk_text(text: str, size: int = 700, overlap: int = 120) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = max(end - overlap, end)
    return chunks

class SimpleRetriever:
    """Retriever TF-IDF fallback. Mantém RAG funcional mesmo sem Chroma/SentenceTransformers."""

    def __init__(self, kb_dir: str | None = None):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        self.cosine_similarity = cosine_similarity
        self.documents = []
        for doc in load_documents(kb_dir):
            for i, chunk in enumerate(chunk_text(doc["content"])):
                self.documents.append({
                    "doc_id": doc["id"],
                    "chunk_id": f"{doc['id']}::chunk_{i}",
                    "content": chunk,
                    "path": doc["path"],
                })
        self.vectorizer = TfidfVectorizer()
        self.matrix = self.vectorizer.fit_transform([d["content"] for d in self.documents])

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        q = self.vectorizer.transform([query])
        scores = self.cosine_similarity(q, self.matrix)[0]
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        results = []
        for idx, score in ranked:
            item = dict(self.documents[idx])
            item["score"] = float(score)
            results.append(item)
        return results

def get_retriever():
    return SimpleRetriever()
