from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredImageLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

import json
import os

def load_json_dataset(path):
    try:
        out = []
        with open(path, 'r', encoding='utf-8') as fh:
            for line in fh:
                out.append(json.loads(line))
        return out
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {path} was not found")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSONL format in {path}")

def load_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} was not found")
        
    path = str(path)
    try:
        if path.lower().endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif path.lower().endswith((".png", ".jpg", ".jpeg")):
            loader = UnstructuredImageLoader(path)
        else:
            loader = TextLoader(path, encoding="utf-8")
        return loader.load()
    except Exception as e:
        raise Exception(f"Error loading file {path}: {str(e)}")

def chunk_documents(docs, chunk_size=500, chunk_overlap=100):
    if not docs:
        return []
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return splitter.split_documents(docs)
    except Exception as e:
        raise Exception(f"Error chunking documents: {str(e)}")

def docs_from_json_records(records):
    if not records:
        return []
    
    out = []
    for r in records:
        text = r.get("text", "")
        meta = {
            "id": r.get("id"),
            "category": r.get("category"),
            "label": r.get("label")
        }
        out.append(Document(page_content=text, metadata=meta))
    return out
