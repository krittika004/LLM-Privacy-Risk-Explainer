import streamlit as st
import requests
import json
import os

#CONFIG
BACKEND_URL = "http://127.0.0.1:8000"  # FastAPI backend URL

st.set_page_config(page_title="PrivAware", page_icon="🛡️", layout="wide")

#UI TITLE
st.title("🛡️ PrivAware: AI-Powered Privacy Policy Explainer")
st.markdown("""
Upload a **Privacy Policy** or **Terms of Service** document to analyze data risks, 
highlight red flags, and get an easy-to-read summary powered by RAG and Gemini.
""")

#File Upload
uploaded_file = st.file_uploader("Upload PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    st.info("Uploading and processing your document... ⏳")

    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post(f"{BACKEND_URL}/analyze", files=files)

    if response.status_code == 200:
        data = response.json()

        #Trust Score
        st.subheader("🔒 Trust Score")
        trust_score = data.get("trust_score", "N/A")
        st.metric(label="User Data Trust Level", value=f"{trust_score}/100")

        #Summary
        st.subheader("📄 Simplified Summary")
        st.write(data.get("summary", "No summary generated."))

        #Red Flags
        st.subheader("🚨 Privacy Red Flags")
        flags = data.get("red_flags", [])
        if flags:
            for flag in flags:
                st.warning(flag)
        else:
            st.success("No major red flags found.")

       
        #Q&A
        st.subheader("Ask Questions About This Policy")
        user_query = st.text_input("Ask a question (e.g., Does this policy share my data with third parties?)")
        if st.button("Ask"):
            query_response = requests.post(f"{BACKEND_URL}/query", json={"query": user_query})
            if query_response.status_code == 200:
                st.info(query_response.json().get("answer", "No answer found."))
            else:
                st.error("Error getting answer from backend.")

    else:
        st.error(f"Error: {response.status_code} - {response.text}")

#Footer
st.markdown("---")
st.caption("Built using Streamlit, LangChain, FAISS & Gemini API")
