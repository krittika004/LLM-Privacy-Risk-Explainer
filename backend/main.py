from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PrivAware API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "PrivAware backend running!"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Accepts uploaded document (text/pdf/image), extracts text, 
    and performs basic analysis (mock RAG pipeline placeholder).
    """
    try:
        contents = await file.read()
        text = contents.decode("utf-8", errors="ignore")

        # Basic simulation — later replace with real RAG + Gemini logic
        risk_terms = ["share", "data", "third party", "track", "collect"]
        found = [term for term in risk_terms if term in text.lower()]

        summary = (
            f"The document '{file.filename}' was analyzed. "
            f"Detected {len(found)} potential data risk terms: {', '.join(found)}."
        )

        return {
            "filename": file.filename,
            "word_count": len(text.split()),
            "red_flags": found,
            "trust_score": max(0, 100 - len(found) * 10),
            "summary": summary,
            "consent_recommendation": "No" if len(found) > 3 else "Yes"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
