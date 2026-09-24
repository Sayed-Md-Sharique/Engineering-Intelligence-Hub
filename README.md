# Engineering Intelligence Hub

A simple and easy-to-understand RAG project for engineering knowledge.

## What can it read?

- PDF
- TXT
- Markdown
- Python
- JavaScript
- TypeScript
- Java
- C / C++
- JSON
- YAML

## Technology

- Python
- FastAPI
- LangChain
- HuggingFace Embeddings
- Qdrant
- Groq
- Streamlit

## How the project works

Document
-> Text extraction
-> Chunking
-> Embeddings
-> Qdrant
-> Similarity search
-> Groq LLM
-> Answer + Sources

## Setup

### 1. Create environment

Windows:

python -m venv .venv
.venv\\Scripts\\activate

### 2. Install backend

cd backend
pip install -r requirements.txt

### 3. Configure API keys

Copy `.env.example` to `.env`.

Add:

GROQ_API_KEY=your_key
QDRANT_URL=your_url
QDRANT_API_KEY=your_key

### 4. Run FastAPI

From the backend folder:

uvicorn main:app --reload

Open:

http://127.0.0.1:8000/docs

### 5. Run Streamlit

Open another terminal:

cd frontend
pip install -r requirements.txt
streamlit run app.py

## Interview explanation

"I built a multi-source RAG application for engineering knowledge. It reads documents and source code, splits the content into smaller chunks, converts the chunks into embeddings and stores them in Qdrant. When a user asks a question, the system retrieves the most relevant chunks and sends them as context to a Groq-hosted LLM. FastAPI provides the backend APIs and Streamlit provides the user interface."
