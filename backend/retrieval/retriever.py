# backend/retrieval/retriever.py
import faiss, pickle, numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from typing import List, Dict

EMBED_MODEL = "all-mpnet-base-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"  # efficient cross-encoder

class FaissRetriever:
    def __init__(self, index_path, meta_path, embed_model=EMBED_MODEL):
        self.idx = faiss.read_index(index_path)
        with open(meta_path, "rb") as fh:
            self.meta = pickle.load(fh)
        self.embed = SentenceTransformer(embed_model)

    def embed_query(self, q):
        v = self.embed.encode([q], convert_to_numpy=True)
        faiss.normalize_L2(v)
        return v.astype('float32')

    def search(self, q, k=50):
        v = self.embed_query(q)
        D, I = self.idx.search(v, k)
        results = []
        for score, i in zip(D[0].tolist(), I[0].tolist()):
            if i < 0: continue
            results.append({"score": float(score), "text": self.meta["texts"][i], "meta": self.meta["metas"][i]})
        return results

class Reranker:
    def __init__(self, model_name=RERANKER_MODEL):
        self.model = CrossEncoder(model_name, device='cpu')  # use GPU if available

    def rerank(self, query:str, candidates:List[Dict], top_k=6):
        pairs = [(query, c["text"]) for c in candidates]
        scores = self.model.predict(pairs)
        # attach scores & sort
        for c, s in zip(candidates, scores):
            c["_rerank_score"] = float(s)
        candidates.sort(key=lambda x: x["_rerank_score"], reverse=True)
        return candidates[:top_k]
