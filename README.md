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

## ⚙️ Setup Instructions
```bash
# Clone the repository
git clone https://github.com/<your-username>/PrivAware.git
cd PrivAware

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
