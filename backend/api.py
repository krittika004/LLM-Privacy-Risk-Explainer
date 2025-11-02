from fastapi import FastAPI, UploadFile, Form
from backend.rag.rag_chain import RAGService
import tempfile, os

app = FastAPI()
# instantiate services for both indexes
opp_service = RAGService("indexes/faiss_opp.index", "indexes/meta_opp.pkl")
med_service = RAGService("indexes/faiss_med.index", "indexes/meta_med.pkl")

@app.post("/analyze/")
async def analyze(doc_type: str = Form(...), file: UploadFile = None, text: str = Form(None)):
    # accept either uploaded file or raw text
    if file:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
        tmp.write(await file.read()); tmp.close()
        # load text using loaders
        from backend.loaders.loaders import load_file
        docs = load_file(tmp.name)
        user_text = " ".join([d.page_content for d in docs])
        os.unlink(tmp.name)
    elif text:
        user_text = text
    else:
        return {"error":"Provide file or text"}
    service = opp_service if doc_type=="opp" else med_service
    return service.analyze(user_text)
