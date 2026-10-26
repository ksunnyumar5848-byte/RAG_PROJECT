import json
import os 
from pathlib import Path
from dotenv import load_dotenv
import faiss
import numpy as pd
from docx import Document
from pypdf import PdfReader
from google import genai

#  setting 

BASE_DIR=Path(__file__).resolve().parent

DATA_DIR=BASE_DIR /"data"
VECTOR_STORE_DIR=BASE_DIR / "vector_store"
INDEX_PATH=VECTOR_STORE_DIR / "faiss.index"
CHUNKS_PATH=VECTOR_STORE_DIR / "chunks.json"

EMBEDDING_MODEL="models/text-embedding-004"
CHAT_MODEL="gemini-2.0-flash"

CHUNK_SIZE=1000
CHUNK_OVERLAP=150
TOP_K=3
EMBIDDING_BATCH_SIZE=100

TEMPERATURE=0.2
TOP_P=0.7
MAX_TOKENS=700


# client setup 

load_dotenv(BASE_DIR/ ".evn")
api_key=os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RecursionError(" GEMINI_API_KEY was are the not found ")

client = genai.Client(api_key=api_key)



# rag introduces 

# document loader 


def load_document():

    if not DATA_DIR.exists():
        raise RuntimeError(f"Data folder are found here : {DATA_DIR}")

    documents=[]