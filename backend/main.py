from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import router as api_router

app = FastAPI(title="PrivAware API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount API router (contains /analyze and /evaluate)
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "PrivAware backend running!"}
