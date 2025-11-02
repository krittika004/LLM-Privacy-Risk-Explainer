# frnt.py
import streamlit as st
import requests
from PIL import Image

# ---------- CONFIG ----------
BACKEND_URL = "http://127.0.0.1:8000"  # FastAPI backend URL
ANALYZE_URL = f"{BACKEND_URL}/analyze"
QUERY_URL = f"{BACKEND_URL}/query"

st.set_page_config(page_title="PrivAware RAG Explainer", page_icon="🛡️", layout="wide")

# Update title and description
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
    st.caption("Developed by PrivAware Inc. ")

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
    #st.info("Choose your input method on the left and click below to analyze 👇")
    analyze_btn = st.button("🚀 Analyze Document", use_container_width=True)

# ---------- ANALYSIS LOGIC ----------
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None
if "last_context_id" not in st.session_state:
    st.session_state["last_context_id"] = None

# Update API request format
if analyze_btn:
    doc_type = "terms" if "Terms" in mode else "medical_bond"
    
    if input_method == "Paste Text":
        payload = {
            "text": text_input,
            "doc_type": doc_type
        }
        headers = {"Content-Type": "application/json"}
        resp = requests.post(ANALYZE_URL, json=payload, headers=headers, timeout=300)
    else:
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        data = {"doc_type": doc_type}
        resp = requests.post(ANALYZE_URL, files=files, data=data, timeout=300)

    if resp.status_code == 200:
        st.session_state["last_result"] = resp.json()
        st.session_state["last_context_id"] = resp.json().get("context_id")
        st.success("✅ Document analyzed successfully!")
    else:
        st.error(f"Backend error: {resp.status_code} - {resp.text}")

# ---------- DISPLAY RESULTS ----------
result = st.session_state.get("last_result")

if result:
    st.markdown("---")
    st.subheader("📘 Simplified Summary")
    st.markdown(
        f"<div style='background-color:#f9f9f9; padding:15px; border-radius:10px;'>{result.get('summary', 'No summary available.')}</div>",
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🚨 Red Flags")
        flags = result.get("red_flags", [])
        if flags:
            for f in flags:
                st.warning(f)
        else:
            st.success("No major red flags detected ✅")

    with col_b:
        st.subheader("🔒 Trust Score")
        trust = result.get("trust_score", "N/A")
        if trust != "N/A":
            st.metric("Document Trust Level", f"{trust}/100")
        else:
            st.write("No trust score available.")

        consent = result.get("consent", "N/A")
        if str(consent).lower() in ["yes", "true", "y"]:
            st.success("✅ Consent Recommended: Yes")
        elif str(consent).lower() in ["no", "false", "n"]:
            st.error("❌ Consent Recommended: No")
        else:
            st.info("Consent decision not determined.")

    st.markdown("---")
    st.subheader("💬 Ask Questions About This Document")
    user_q = st.text_input("Enter your question (e.g., 'Does this share my medical data?')")

    # Update query endpoint call
    if st.button("Ask Question"):
        if not user_q.strip():
            st.warning("Please enter a question.")
        else:
            try:
                payload = {
                    "query": user_q,
                    "context_id": st.session_state.get("last_context_id")
                }
                qresp = requests.post(QUERY_URL, json=payload, timeout=120)
                if qresp.status_code == 200:
                    ans = qresp.json().get("answer", "No answer found.")
                    st.info(ans)
                else:
                    st.error(f"Error: {qresp.status_code} - {qresp.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Query failed: {e}")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#888;'>Built using Streamlit</p>",
    unsafe_allow_html=True,
)
