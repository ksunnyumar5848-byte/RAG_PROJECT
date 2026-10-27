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
        raise FileNotFoundError(f"Data folder are found here : {DATA_DIR}")

    documents=[]

    for file_path in sorted(DATA_DIR.rglob("*")):
        if not file_path.is_file():
            continue
        suffix=file_path.suffix.lower()     
        text=""

        try:
            if suffix==".txt":
                text=file_path.read_text(encoding="utf-8",errors= "ignore")
            elif suffix==".pdf":
                reader=PdfReader(str(file_path))
                text="\n".join(page.extract_text() or "" for page in reader.pages)
            elif suffix==".docx":
                doc = Document(str(file_path))
                text="\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
            else:
                continue 
                
        except Exception as e:
            print(f"  Warning Could not read the {file_path.name} : e ")
            continue

        text=text.strip()

        if text:
            documents.append({
                "source":file_path.relative_to(DATA_DIR),
                "text":text
            })
            print(f"Loaded : {file_path.relative_to(DATA_DIR)}")
        else:
            print(f" Skipped (no extracable text found ): {file_path.name}")

    if not documents:
        raise ValueError("No readable text found in the data folder ")

    return documents


# simple chunking 

def split_into_chunks(documents):
    chunks=[]
    step =CHUNK_SIZE - CHUNK_OVERLAP

    for document in documents:
        text=document["text"]

        for start in range(0,len(text),step):
            chunk_text=text[start:start+CHUNK_SIZE].strip()

            if chunk_text:
                chunks.append({
                    "source":document["source"],
                    "text":chunk_text
                })

    if not chunks:
        raise ValueError("chunking produced no text chunks or data ")

    print(f"created {len(chunks)} chunks.")  

    return chunks



# ----------GEmini Embedding----------------#

import numpy as np
import faiss

def create_embeddings(texts):
    """Generate embedding vectors in batches using Gemini."""

    all_embeddings = []

    for start in range(0, len(texts),EMBIDDING_BATCH_SIZE):
        batch = texts[start:start+EMBIDDING_BATCH_SIZE]

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=batch
        )

        batch_embeddings = [
            embedding.values
            for embedding in response.embeddings
        ]

        all_embeddings.extend(batch_embeddings)

    vectors = np.asarray(all_embeddings, dtype=np.float32)

    if vectors.ndim != 2 or len(vectors) != len(texts):
        raise RuntimeError(
            "Embedding response did not match the input text count."
        )

    # Normalize vectors so inner-product search behaves like cosine similarity
    faiss.normalize_L2(vectors)

    return vectors



#Build and save the FAISS vector database 
def build_vector_store():
    documents=load_document()
    chunks=split_into_chunks(documents)

    print("Create embedding .... this may take a little while")

    vector=create_embeddings([chunk["text"] for chunk in chunks])

    index=faiss.IndexFlatIP(vector.shape[1])
    index.add(vector)

    VECTOR_STORE_DIR.mkdir(parents=True,exist_ok=True)

    faiss.write_index(index,str(INDEX_PATH))

    with CHUNKS_PATH.open("w",encoding="utf-8") as file:
        json.dumps(chunks,file,ensure_ascii=False,indent=2)

    print(f"Saved FAISS Index to : {INDEX_PATH}")

    print(f" Saved chunk meta data : {CHUNKS_PATH}")

    return index ,chunks


def load_or_build_vector_store():
    VECTOR_STORE_DIR.mkdir(parents=True , exist_ok=True)

    if INDEX_PATH.exists() and CHUNKS_PATH.exists():
        print("Found saved vector store loading it without rebuilding .....")
        index=faiss.read_index(str(INDEX_PATH))

        with CHUNKS_PATH.open("r",encoding="utf-8") as file:
            chunks=json.load(file)
        if index.ntotal !=len(chunks):
            print("saved index and chunk meta data do not match  rebuilding index ...........")

            return build_vector_store
        if index.ntotal ==0:
            print("saved vector store in empty there for rebuilding........")

            return build_vector_store

        print(f"Loaded {len(chunks)} chunks saved vector db ")
        return index ,chunks
    print("no Complete saved vector db found buliding it now ")

    return build_vector_store


#========================= Retrival 


def retieve_relevent_chunks(question,index,chunks):
    query_vector=create_embeddings([question])
    number_to_fetch=TOP_K

    scores, positions=index.search(query_vector,number_to_fetch)

    results=[]

    
        






