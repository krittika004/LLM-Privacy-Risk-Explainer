# frnt.py
import streamlit as st
import requests
from PIL import Image

# ---------- CONFIG ----------
BACKEND_URL = "http://127.0.0.1:8000"
ANALYZE_URL = f"{BACKEND_URL}/analyze/"
QUERY_URL = f"{BACKEND_URL}/query"

st.set_page_config(page_title="PrivAware RAG Explainer", page_icon="🛡️", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center; color: #4A90E2;'>🛡️ PrivAware — AI RAG Document Explainer</h1>
    <p style='text-align: center; font-size: 18px; color: #666;'>
    Upload a <strong>Privacy Policy</strong> like <strong>Terms & Conditions</strong>, or <strong>Medical Document</strong> 
    to analyze data risks and get an AI-powered summary.
    </p>
    """,
    unsafe_allow_html=True,
)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    mode = st.radio(
        "Choose explainer type:",
        ("Terms & Conditions Explainer", "Medical Bond Docs Explainer"),
    )
    st.markdown("---")
    st.caption("Developed by PrivAware Inc.")

# ---------- MAIN INPUT ----------
st.markdown("### 📄 Upload or Paste Your Document")

col1, col2 = st.columns([1.7, 1])

with col1:
    input_method = st.radio("Input Method:", ("Paste Text", "Upload File"), horizontal=True)
    uploaded_file = None
    text_input = ""

    if input_method == "Paste Text":
        text_input = st.text_area(
            "Paste your document text here:",
            placeholder="Paste the Terms or Medical Bond document text...",
            height=250,
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload PDF, TXT, or Image file",
            type=["pdf", "txt", "png", "jpg", "jpeg"],
        )
        if uploaded_file and uploaded_file.type.startswith("image/"):
            try:
                img = Image.open(uploaded_file)
                st.image(img, caption="Uploaded image preview", use_container_width=True)
            except Exception:
                st.warning("Could not preview the image file.")

with col2:
    st.write("")
    st.write("")
    analyze_btn = st.button("🚀 Analyze Document", use_container_width=True)

# ---------- ANALYSIS LOGIC ----------
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

if analyze_btn:
    doc_type = "opp" if "Terms" in mode else "medical"
    
    # Validate input
    if input_method == "Paste Text" and not text_input.strip():
        st.error("❌ Please paste some text to analyze!")
    elif input_method == "Upload File" and not uploaded_file:
        st.error("❌ Please upload a file to analyze!")
    else:
        try:
            with st.spinner("🔍 Analyzing document..."):
                if input_method == "Paste Text":
                    # Send JSON payload for text
                    payload = {
                        "doc_type": doc_type,
                        "text": text_input
                    }
                    resp = requests.post(
                        ANALYZE_URL,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=300
                    )
                else:
                    # Send file upload
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    data = {"doc_type": doc_type}
                    resp = requests.post(
                        ANALYZE_URL,
                        files=files,
                        data=data,
                        timeout=300
                    )
                
                if resp.status_code == 200:
                    st.session_state["last_result"] = resp.json()
                    st.success("✅ Document analyzed successfully!")
                    st.balloons()
                else:
                    error_msg = resp.text
                    try:
                        error_detail = resp.json().get("detail", error_msg)
                    except:
                        error_detail = error_msg
                    st.error(f"❌ Backend error: {resp.status_code}\n\n{error_detail}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend! Make sure uvicorn is running:\n`uvicorn backend.main:app --reload`")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Backend is slow to respond.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ---------- DISPLAY RESULTS ----------
result = st.session_state.get("last_result")

if result:
    st.markdown("---")
    
    # Extract analysis results
    summary = result.get("summary", "No summary available.")
    key_points = result.get("key_points", [])
    trust_score = result.get("trust_score", "N/A")
    recommendation = result.get("consent_recommendation", "N/A")
    red_flags = result.get("red_flags", [])
    
    st.subheader("📘 Simplified Summary")
    st.markdown(
        f"<div style='background-color:#f0f8ff; padding:15px; border-radius:10px; border-left:4px solid #4A90E2;'>{summary}</div>",
        unsafe_allow_html=True,
    )

    # Key points
    st.subheader("📌 Key Points")
    if key_points:
        for i, point in enumerate(key_points, 1):
            st.write(f"{i}. {point}")
    else:
        st.info("No key points extracted.")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.subheader("🚨 Red Flags")
        if red_flags:
            for flag in red_flags:
                st.warning(flag)
        else:
            st.success("No major red flags detected ✅")

    with col_b:
        st.subheader("🔒 Trust Score")
        if trust_score != "N/A":
            try:
                score = int(trust_score)
                st.metric("Document Trust Level", f"{score}/100")
                if score >= 70:
                    st.success("High trust")
                elif score >= 50:
                    st.warning("Medium trust")
                else:
                    st.error("Low trust")
            except:
                st.write(f"Trust Score: {trust_score}")
        else:
            st.write("No trust score available.")

    with col_c:
        st.subheader("✅ Recommendation")
        if str(recommendation).lower() in ["yes", "true", "y", "recommended"]:
            st.success("✅ Consent Recommended")
        elif str(recommendation).lower() in ["no", "false", "n", "not recommended"]:
            st.error("❌ Consent NOT Recommended")
        else:
            st.info(f"Recommendation: {recommendation}")

    # Evaluation metrics (if available)
    if result.get("_evaluation"):
        st.markdown("---")
        st.subheader("📈 Evaluation Metrics (RAGAS)")
        
        eval_data = result.get("_evaluation", {})
        eval_col1, eval_col2, eval_col3, eval_col4 = st.columns(4)
        
        with eval_col1:
            if "faithfulness" in eval_data:
                st.metric("Faithfulness", f"{float(eval_data['faithfulness']):.3f}")
        with eval_col2:
            if "answer_relevancy" in eval_data:
                st.metric("Answer Relevancy", f"{float(eval_data['answer_relevancy']):.3f}")
        with eval_col3:
            if "context_precision" in eval_data:
                st.metric("Context Precision", f"{float(eval_data['context_precision']):.3f}")
        with eval_col4:
            if "context_recall" in eval_data:
                st.metric("Context Recall", f"{float(eval_data['context_recall']):.3f}")

    # Question section
    st.markdown("---")
    st.subheader("💬 Ask Questions About This Document")
    user_q = st.text_input("Enter your question (e.g., 'Does this share my medical data?')")

    if st.button("🔍 Ask Question"):
        if not user_q.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Searching for answer..."):
                    # For now, just show a mock answer
                    st.info(f"Q: {user_q}\n\nA: Based on the document analysis, the answer would be derived from the retrieved context.")
            except Exception as e:
                st.error(f"Query failed: {e}")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#888;'>Built using Streamlit | PrivAware Inc.</p>",
    unsafe_allow_html=True,
)
