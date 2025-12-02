import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"  # local shorthand for sentence-transformers model

class RAGStore:
    """
    Minimal FAISS-backed RAG store.
    Stores:
      - faiss index file at index_path
      - metadata list as a numpy file at meta_path
    Metadata entries: dict with keys: doc_id, chunk_text
    """
    def __init__(self, dim=384, index_path="faiss_index.index", meta_path="faiss_meta.npy"):
        self.dim = dim
        self.index_path = index_path
        self.meta_path = meta_path
        self.model = SentenceTransformer(EMBED_MODEL_NAME)
        # load or init
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            try:
                self.index = faiss.read_index(self.index_path)
                self.meta = np.load(self.meta_path, allow_pickle=True).tolist()
            except Exception:
                # fallback to fresh index
                self.index = faiss.IndexFlatL2(self.dim)
                self.meta = []
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.meta = []

    def save(self):
        faiss.write_index(self.index, self.index_path)
        np.save(self.meta_path, np.array(self.meta, dtype=object))

    def add_document(self, doc_id, text, chunk_size=200, overlap=50):
        """
        Naive whitespace chunking. chunk_size in words.
        """
        tokens = text.split()
        i = 0
        chunks = []
        while i < len(tokens):
            chunk_tokens = tokens[i:i+chunk_size]
            chunk_text = " ".join(chunk_tokens).strip()
            if chunk_text:
                chunks.append(chunk_text)
            i += chunk_size - overlap
        if not chunks:
            return
        embeddings = self.model.encode(chunks, convert_to_numpy=True, show_progress_bar=False)
        # ensure embeddings shape matches index dim
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        self.index.add(embeddings.astype("float32"))
        for c in chunks:
            self.meta.append({"doc_id": doc_id, "chunk_text": c})
        self.save()

    def query(self, query_text, top_k=5):
        q_emb = self.model.encode([query_text], convert_to_numpy=True)
        if q_emb.ndim == 1:
            q_emb = q_emb.reshape(1, -1)
        # If no vectors present, return empty
        if self.index.ntotal == 0:
            return []
        D, I = self.index.search(q_emb.astype("float32"), top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.meta):
                results.append(self.meta[idx])
        return results
