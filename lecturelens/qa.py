"""Ask questions about a lecture: local semantic search + LLM answer."""
import numpy as np


class LectureQA:
    def __init__(self, llm, embed_model="sentence-transformers/all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.embedder = SentenceTransformer(embed_model)
        self.llm = llm
        self.chunks, self.vectors = [], None

    def index(self, transcript: str, size: int = 400):
        words = transcript.split()
        self.chunks = [" ".join(words[i:i + size]) for i in range(0, len(words), size)]
        self.vectors = self.embedder.encode(self.chunks, normalize_embeddings=True)

    def ask(self, question: str, k: int = 3) -> str:
        q = self.embedder.encode([question], normalize_embeddings=True)[0]
        top = np.argsort(self.vectors @ q)[::-1][:k]
        context = "\n---\n".join(self.chunks[i] for i in top)
        return self.llm(f"Answer using only this lecture context.\n{context}\n\nQuestion: {question}")
