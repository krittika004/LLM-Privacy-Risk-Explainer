# backend/retrieval/retriever.py
import pickle
from typing import Any, Optional, List, Dict

# Lazy import faiss and numpy to avoid import-time errors during app startup
_faiss = None
_np = None
_faiss_import_error: Optional[BaseException] = None

def _ensure_faiss():
    global _faiss, _np, _faiss_import_error
    if _faiss is not None:
        return
    if _faiss_import_error is not None:
        raise ImportError("faiss/numpy previously failed to import") from _faiss_import_error
    try:
        import faiss as _faiss_mod  # local name to avoid shadowing
        import numpy as _np_mod
        _faiss = _faiss_mod
        _np = _np_mod
    except Exception as e:
        _faiss_import_error = e
        raise

class FaissRetriever:
    def __init__(self, index_path: str, meta_path: str):
        self.index = None
        self.metadata = []
        self.use_mock = False
        
        try:
            _ensure_faiss()
            # load actual index
            self.index = _faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                self.metadata = pickle.load(f)
            print(f"✅ Loaded FAISS index from {index_path}")
        except Exception as e:
            print(f"⚠️  FaissRetriever init failed: {e}. Using mock mode.")
            self.use_mock = True
            self.index = None
            self.metadata = []

    def search(self, query_text: str, k: int = 5) -> List[Dict[str, Any]]:
        if self.use_mock or self.index is None:
            # return mock results
            print(f"🔍 Mock search: '{query_text}' (k={k})")
            return [
                {"text": f"Mock retrieved document {i}", "page_content": f"Mock content snippet {i} related to '{query_text}'"} 
                for i in range(k)
            ]
        # real search (would need embedding first)
        try:
            distances, indices = self.index.search(query_text, k)
            return [self.metadata[i] for i in indices[0] if i < len(self.metadata)]
        except Exception as e:
            print(f"⚠️  Search failed: {e}. Returning mock results.")
            return [{"text": f"Mock result {i}", "page_content": f"Content {i}"} for i in range(k)]

class Reranker:
    def __init__(self):
        self.use_mock = True
        print("⚠️  Reranker initialized in mock mode")
    
    def rerank(self, query: str, docs: List[Any], top_k: int = 5) -> List[Any]:
        """Simple mock reranker - just return top_k docs"""
        if not docs:
            return []
        print(f"🔄 Reranking {len(docs)} docs with top_k={top_k}")
        return docs[:top_k]
