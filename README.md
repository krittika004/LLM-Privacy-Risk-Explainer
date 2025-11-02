# 🕵️‍♀️ PrivAware – AI-Powered Privacy Policy Explainer

PrivAware is an **LLM-powered privacy risk analyzer** that helps users understand complex Terms of Service and Privacy Policies.  
It simplifies legal text into **clear summaries**, highlights **red-flag clauses**, and assigns **trust scores** for transparency.

---

## 🚀 Features
- 📄 **Policy Parsing:** Supports PDF and text uploads.
- 🤖 **RAG Pipeline:** Integrates FAISS embeddings, NER-based clause extraction, and a trust scoring engine.
- 💬 **Interactive Agent:** LLM-powered Q&A for contextual policy insights.
- 📊 **Visual Dashboard:** Streamlit interface for privacy risk visualization and clause transparency.

---

## 🧠 Tech Stack
- **Python**, **LangChain**, **FAISS**, **Streamlit**
- **Google Generative AI / OpenAI**
- **Pandas**, **PyPDF2**, **NER (spaCy)**

---
## 📁 Project Structure
```
PrivAware/
│
├── backend/
│   ├── api.py
│   ├── main.py
│   ├── prompt_template.py
│   │
│   ├── data/
│   │   ├── opp.json
│   │   └── medical_consents.json
│   │
│   ├── indexing/
│   │   └── indexer.py
│   │
│   ├── loaders/
│   │   └── loaders.py
│   │
│   ├── models/
│   │   ├── scoring.py
│   │   └── train_classifier.py
│   │
│   ├── rag/
│   │   └── rag_chain.py
│   │
│   └── retrieval/
│       ├── __init__.py
│       └── retriever.py
│
├── frontend/
│   └── streamlit_app.py
│
├── indexes/
│   ├── faiss_med.index
│   ├── faiss_opp.index
│   ├── meta_med.pkl
│   └── meta_opp.pkl
│
├── models/
│   └── label_clf.pkl
│
├── .env
├── README.md
└── requirements.txt
```




## ⚙️ Setup Instructions
```bash
# Clone the repository
git clone https://github.com/<your-username>/PrivAware.git
cd PrivAware

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate       # On Windows
source .venv/bin/activate    # On Mac/Linux

# Install dependencies
pip install -r requirements.txt
(If Streamlit installation fails, run:
pip install streamlit --no-deps
pip install protobuf pandas numpy)

# Run the app
uvicorn backend.main:app --reload (Backend: FastAPI)
python -m streamlit run frontend/streamlit_app.py (Frontend: Streamlit)
