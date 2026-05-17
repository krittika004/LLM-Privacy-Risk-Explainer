from fastapi import APIRouter, UploadFile, Form, HTTPException, Body
from pydantic import BaseModel
import tempfile, os, json

# LAZY INIT: don't instantiate services at module import time
_opp_service = None
_med_service = None

def get_opp_service():
    global _opp_service
    if _opp_service is None:
        from backend.rag.rag_chain import RAGService
        _opp_service = RAGService("indexes/faiss_opp.index", "indexes/meta_opp.pkl")
    return _opp_service

def get_med_service():
    global _med_service
    if _med_service is None:
        from backend.rag.rag_chain import RAGService
        _med_service = RAGService("indexes/faiss_med.index", "indexes/meta_med.pkl")
    return _med_service

router = APIRouter()

class AnalyzeRequest(BaseModel):
    doc_type: str
    text: str

@router.post("/analyze/")
async def analyze(req: AnalyzeRequest):
    """Accept JSON body instead of form data"""
    try:
        try:
            service = get_opp_service() if req.doc_type=="opp" else get_med_service()
        except ImportError as e:
            raise HTTPException(
                status_code=503,
                detail=f"RAG service not available (faiss/numpy issue): {str(e)}"
            )
        
        return service.analyze(req.text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate/")
async def evaluate(question: str = Form(...), answer: str = Form(...), contexts: str = Form(...)):
    """
    Run ragas evaluation on a single example.
    - contexts: JSON array string or newline-separated contexts
    Lazy imports ragas only when this endpoint is called.
    """
    try:
        try:
            from backend.evaluation.ragas_eval import evaluate_rag_pipeline
            from backend.evaluation.config import get_llm
            from backend.evaluation.metrics import get_metrics
        except ImportError as e:
            raise HTTPException(
                status_code=503,
                detail=f"RAGAS evaluation not available: {str(e)}"
            )

        try:
            ctx_list = json.loads(contexts)
            if not isinstance(ctx_list, list):
                ctx_list = [str(ctx_list)]
        except Exception:
            ctx_list = [c for c in contexts.splitlines() if c.strip()]

        try:
            _llm = get_llm()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"LLM config failed: {str(e)}")

        result = evaluate_rag_pipeline(question, answer, ctx_list)
        return {"question": question, "answer": answer, "contexts": ctx_list, "evaluation": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
