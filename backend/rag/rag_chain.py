import os, json, re
from dotenv import load_dotenv
import google.generativeai as genai
from backend.retrieval.retriever import FaissRetriever, Reranker
from backend.prompt_template import RAG_PROMPT

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def build_evidence_block(retrieved):
    lines=[]
    for i,r in enumerate(retrieved):
        lines.append(f"[{i}] {r['text'][:800].replace('\\n',' ')}")
    return "\n\n".join(lines)

def call_gemini(prompt_text):
    model = genai.models.get("gemini-1.5-pro")  # adapt if SDK uses another call
    # NOTE: SDK may use different call; adapt to your installed google-generativeai version
    resp = genai.generate_text(model=model, text=prompt_text)  # pseudo; replace with working call
    return resp.text if hasattr(resp, 'text') else str(resp)

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
        # extract JSON substring robustly
        j = self._extract_json(llm_out)
        j["_raw"] = llm_out
        j["_evidence"] = reranked
        return j

    def _extract_json(self, text):
        start = text.find("{")
        end = text.rfind("}")
        if start==-1 or end==-1: return {"raw": text}
        try:
            return json.loads(text[start:end+1])
        except Exception:
            # best-effort cleaning
            cleaned = text[start:end+1].replace("'", '"')
            cleaned = re.sub(r",\s*}", "}", cleaned)
            try:
                return json.loads(cleaned)
            except Exception:
                return {"raw": text}
