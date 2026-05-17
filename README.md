# 🕵️‍♀️ PrivAware – AI-Powered Privacy Policy Explainer

PrivAware is an intelligent AI-powered RAG (Retrieval-Augmented Generation) system that analyzes Terms of Service and Privacy Policies, identifies potential privacy risks, and generates simplified user-friendly explanations with contextual Q&A support.

The project leverages Large Language Models (LLMs), vector retrieval, and trust/risk analysis to help users better understand complex legal and policy documents.

---

## 🚀 Features

### 📄 Privacy Policy & Terms Analysis
- Upload or paste Terms & Conditions / Privacy Policies
- AI-powered summarization
- Simplified explanations for non-technical users

### ⚠️ Risk Detection
- Detects:
  - Data-sharing risks
  - Third-party tracking concerns
  - Sensitive permissions
  - Potential privacy red flags

### 🤖 RAG-Based Question Answering
- Context-aware chatbot
- Retrieval-Augmented Generation pipeline
- Semantic document search

### 📊 Evaluation Framework
- Evaluation metrics for model performance
- Scenario-based testing
- Retrieval quality assessment

### 🎨 Interactive UI
- Streamlit-based frontend
- User-friendly interface
- Multiple explainer modes

---

# 🏗️ Project Architecture

```text
                ┌────────────────────┐
                │     User Input      │
                │ Upload / Paste Docs │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   Streamlit UI      │
                │   Frontend Layer    │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │    Backend API      │
                │  RAG Processing     │
                └─────────┬──────────┘
                          │
          ┌───────────────┴────────────────┐
          ▼                                ▼
 ┌─────────────────┐              ┌─────────────────┐
 │  Vector Indexes │              │   LLM Engine    │
 │   FAISS/RAG DB  │              │ Gemini/OpenAI   │
 └─────────────────┘              └─────────────────┘
```

---

# 📂 Current Project Structure

```text
LLM-Privacy-Risk-Explainer/
│
├── backend/
│   ├── evaluation/
│   │   ├── config.py
│   │   ├── metrics.py
│   │   └── ragas_eval.py
│   │
│   ├── rag/
│   │   └── rag_chain.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── api.py
│   ├── main.py
│   └── test_evaluation.py
│
├── frontend/
│   └── streamlit_app.py
│
├── data/
├── indexes/
├── models/
│
├── eval_scenarios_table.py
├── test_metrics.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🛠️ Tech Stack

## Backend
- Python
- FastAPI / Flask
- LangChain
- FAISS
- RAG Pipeline

## Frontend
- Streamlit

## AI / NLP
- Gemini API / OpenAI
- Sentence Transformers
- Retrieval-Augmented Generation (RAG)

## Evaluation
- RAGAS
- Custom evaluation metrics

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/krittika004/LLM-Privacy-Risk-Explainer.git
cd LLM-Privacy-Risk-Explainer
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory.

Example:

```env
GOOGLE_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
```

---

# ▶️ Running the Project

## Start Backend

```bash
python backend/main.py
```

---

## Start Frontend

```bash
streamlit run frontend/streamlit_app.py
```

---

# 📊 Evaluation Modules

The project includes:
- Retrieval evaluation
- Scenario testing
- Metric calculation
- RAGAS-based assessment

Run tests:

```bash
python test_metrics.py
```

```bash
python backend/test_evaluation.py
```

---

# 🧠 Core Functionalities

- Document ingestion
- Vector embedding generation
- Semantic retrieval
- LLM-based explanation
- Risk summarization
- Trust evaluation
- Contextual Q&A

---

# 🔮 Future Improvements

- 🌐 Multi-language support
- 🧩 Browser extension
- 📱 Mobile-friendly UI
- ☁️ Cloud deployment
- 🔐 Advanced privacy scoring
- 📈 Analytics dashboard

---

# 📸 Screenshots

> Add screenshots of:
- Homepage
- Upload interface
- Risk analysis output
- Chatbot responses
- Evaluation dashboard

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a pull request

---
