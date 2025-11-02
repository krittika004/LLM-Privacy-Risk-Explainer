import os, pickle
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from langchain_core.documents import Document
from backend.loaders.loaders import load_json_dataset, docs_from_json_records, chunk_documents

EMBED_MODEL = "all-mpnet-base-v2"  

class FaissIndexer:
    def __init__(self, model_name=EMBED_MODEL):
        self.model = SentenceTransformer(model_name)

    def build_index(self, docs, index_path, meta_path):
        texts = [d.page_content for d in docs]
        metas = [d.metadata for d in docs]
        embs = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    
        import faiss
        faiss.normalize_L2(embs)
        dim = embs.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embs.astype('float32'))
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(index, index_path)
        with open(meta_path, "wb") as fh:
            pickle.dump({"metas": metas, "texts": texts}, fh)
        print("Saved index and metadata:", index_path)

if __name__ == "__main__":
    # Build OPP index
    opp_records = load_json_dataset("data/opp.json")
    opp_docs = docs_from_json_records(opp_records)
    idx = FaissIndexer()
    idx.build_index(opp_docs, "indexes/faiss_opp.index", "indexes/meta_opp.pkl")

    # Build medical index
    med_records = load_json_dataset("data/medical_consents.json")
    med_docs = docs_from_json_records(med_records)
    idx.build_index(med_docs, "indexes/faiss_med.index", "indexes/meta_med.pkl")
