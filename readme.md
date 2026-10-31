 📚 RAG Project using Gemini + FAISS

A simple Retrieval-Augmented Generation (RAG) chatbot built using Python, Google Gemini Embeddings, Gemini LLM, and FAISS Vector Database.

## 🚀 Project Overview

This project demonstrates the complete RAG (Retrieval-Augmented Generation) pipeline from document loading to AI-generated responses.

The chatbot can read documents from a local data folder, convert them into embeddings, store them in a FAISS vector database, retrieve the most relevant chunks for a user question, and generate an answer using Gemini.

---

# 🏗️ RAG Architecture

```text
Documents
(TXT / PDF / DOCX)
        │
        ▼
Document Loader
        │
        ▼
Text Chunking
        │
        ▼
Gemini Embeddings
        │
        ▼
FAISS Vector Store
        │
        ▼
Similarity Search
        │
        ▼
Relevant Chunks
        │
        ▼
Gemini LLM
        │
        ▼
Final Answer
```

---

# 📂 Folder Structure

```text
Rag_project/
│
├── data/
│   ├── sample.docx
│   ├── sample.pdf
│   └── sample.txt
│
├── vector_store/
│   ├── faiss.index
│   └── chunks.json
│
├── myenv/
│
├── .env
├── .gitignore
├── rag.py
├── template.py
└── README.md
```

---

# ✨ Features

✅ Load TXT files

✅ Load PDF files

✅ Load DOCX files

✅ Automatic text chunking

✅ Generate embeddings using Gemini

✅ Store vectors in FAISS

✅ Semantic Search

✅ Context Retrieval

✅ Source Tracking

✅ Question Answering using Gemini LLM

✅ Persistent Vector Database

---

# 🧠 What I Learned

Through this project I learned:

### 1. Document Loading

How to read information from multiple file formats:

- TXT
- PDF
- DOCX

### 2. Chunking

Breaking large documents into smaller chunks for better retrieval.

```python
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
```

### 3. Embeddings

Converting text into numerical vectors using:

```python
gemini-embedding-001
```

### 4. Vector Databases

Storing embeddings in FAISS for fast similarity search.

### 5. Retrieval

Finding the most relevant chunks related to the user's question.

```python
index.search(query_vector, TOP_K)
```

### 6. Context Augmentation

Injecting retrieved chunks into the LLM prompt.

### 7. LLM Response Generation

Generating grounded answers using:

```python
gemini-3.5-flash
```

### 8. Source Attribution

Displaying which document was used to answer the question.

---

# 🔧 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/rag-project.git
cd rag-project
```

---

## Create Virtual Environment

```bash
python -m venv myenv
```

Activate:

### Windows

```bash
myenv\Scripts\activate
```

### Linux / Mac

```bash
source myenv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

# ▶️ Run Project

```bash
python rag.py
```

---

# Example

### User Question

```text
What is the hospital policy?
```

### Retrieved Chunks

```text
Chunk 1
Chunk 2
Chunk 3
```

### AI Response

```text
According to the provided document...
```

### Sources

```text
hospital_policy.txt
```

---

# 📦 Technologies Used

- Python
- Google Gemini API
- FAISS
- NumPy
- PyPDF
- Python-Docx
- Dotenv

---

# Future Improvements

- Streamlit UI
- Chat History
- Metadata Filtering
- Hybrid Search
- Reranking
- Multi-document QA
- LangChain Integration

---
👨‍💻 Author
Sunny Kumar
🚀 AI & Backend Development Enthusiast

I enjoy building projects that help me understand how modern AI systems work internally. This RAG project was created from scratch to learn document ingestion, chunking, embeddings, vector databases, semantic retrieval, prompt engineering, and LLM-based answer generation.

Skills & Technologies
🐍 Python
🟢 Node.js
⚡ Express.js
🤖 Generative AI
📚 RAG Systems
🗄️ FAISS Vector Database
🔍 Semantic Search
🔗 REST APIs

Connect
💻 GitHub: https://github.com/your-github-username

⭐ Thanks for visiting this repository!