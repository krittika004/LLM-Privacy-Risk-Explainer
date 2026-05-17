from dotenv import load_dotenv
import os
import json

load_dotenv()

from backend.retrieval.retriever import FaissRetriever, Reranker
from backend.prompt_template import RAG_PROMPT

# LAZY IMPORT: defer ragas import to avoid startup-time C extension issues
_evaluate_rag_pipeline = None

def get_evaluate_rag_pipeline():
    global _evaluate_rag_pipeline
    if _evaluate_rag_pipeline is None:
        try:
            from backend.evaluation.ragas_eval import evaluate_rag_pipeline
            _evaluate_rag_pipeline = evaluate_rag_pipeline
        except ImportError as e:
            print(f"⚠️  RAGAS not available: {e}")
            _evaluate_rag_pipeline = None
    return _evaluate_rag_pipeline

def build_evidence_block(retrieved):
    lines = []
    for i, r in enumerate(retrieved or []):
        text = ""
        if isinstance(r, dict):
            text = r.get("text") or r.get("page_content") or r.get("pageContent") or ""
        elif hasattr(r, "page_content"):
            text = getattr(r, "page_content") or ""
        else:
            try:
                text = str(r)
            except Exception:
                text = ""
        text = text.replace("\n", " ")[:800]
        lines.append(f"[{i}] {text}")
    return "\n\n".join(lines)

def call_gemini(prompt_text):
    """Lazy-import google.generativeai"""
    try:
        import google.generativeai as genai
    except Exception as e:
        print(f"⚠️  Gemini not available: {e}. Returning mock response.")
        return '{"summary":"Mock analysis","key_points":["Mock point"],"trust_score":50,"consent_recommendation":"Maybe","evidence_refs":[],"rationale":"Using mock mode"}'
    
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    except Exception:
        pass

    try:
        model = genai.models.get("gemini-1.5-pro")
        resp = genai.generate_text(model=model, text=prompt_text)
        return resp.text if hasattr(resp, "text") else str(resp)
    except Exception as e:
        print(f"⚠️  Gemini call failed: {e}. Returning mock response.")
        return '{"summary":"Mock analysis (Gemini unavailable)","key_points":["Mock"],"trust_score":50,"consent_recommendation":"Maybe","evidence_refs":[],"rationale":"Service unavailable"}'

class RAGService:
    def __init__(self, index_path, meta_path):
        self.retriever = FaissRetriever(index_path, meta_path)
        self.reranker = Reranker()

    def analyze(self, user_text, top_k=50):
        retrieved = self.retriever.search(user_text, k=top_k)
        reranked = self.reranker.rerank(user_text, retrieved, top_k=6)
        evidence = build_evidence_block(reranked)
        prompt = RAG_PROMPT.format(context=evidence, query=user_text)
        llm_out = call_gemini(prompt)

        query = user_text
        response = llm_out

        # Extract contexts
        if isinstance(reranked, list) and all(isinstance(d, str) for d in reranked):
            contexts = reranked
        elif isinstance(retrieved, list) and all(isinstance(d, str) for d in retrieved):
            contexts = retrieved
        else:
            contexts = []
            for doc in (reranked or retrieved or []):
                text = None
                if hasattr(doc, "page_content"):
                    text = getattr(doc, "page_content")
                if text is None and isinstance(doc, dict):
                    text = doc.get("text") or doc.get("page_content") or doc.get("pageContent")
                if text is None:
                    try:
                        text = str(doc)
                    except Exception:
                        text = ""
                if text:
                    contexts.append(text)

        evaluation_result = None
        try:
            evaluate_fn = get_evaluate_rag_pipeline()
            if evaluate_fn:
                evaluation_result = evaluate_fn(question=query, answer=response, contexts=contexts)
                print("✅ RAGAS Evaluation:", evaluation_result)
        except Exception as e:
            print(f"⚠️  RAGAS evaluation failed (non-blocking): {str(e)}")

        j = self._extract_json(llm_out)
        j["_raw"] = llm_out
        j["_evidence"] = reranked
        j["_evaluation"] = evaluation_result
        return j

    def _extract_json(self, text):
        start = text.find("{")
        if start == -1:
            return {"error": "no json found", "raw": text}
        try:
            j = json.loads(text[start:])
            return j
        except Exception:
            end = text.rfind("}")
            try:
                j = json.loads(text[start:end+1])
                return j
            except Exception:
                return {"error": "failed to parse json", "raw": text}
