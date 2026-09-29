# Engineering Intelligence Hub

Engineering Intelligence Hub is a RAG-based application that helps developers find information from technical documents and source code.

Users can upload documents, select the files they want to search, and ask questions in natural language. The application retrieves relevant content from the selected documents and uses an LLM to generate the answer.

## Features

* Upload multiple documents and source-code files
* Ask questions using natural language
* Search documents using semantic similarity
* Select one or multiple documents for a query
* Get answers based on the uploaded content
* View the source documents used for retrieval
* Support for PDF, TXT, Markdown and common code files

## Tech Stack

* Python
* FastAPI
* LangChain
* Qdrant
* Hugging Face
* Groq
* Streamlit

## How It Works

```text
Upload Document
      ↓
Extract Text
      ↓
Split into Chunks
      ↓
Create Embeddings
      ↓
Store in Qdrant
      ↓
Ask Question
      ↓
Find Relevant Chunks
      ↓
Groq LLM
      ↓
Answer
```

## Project Structure

```text
Engineering-Intelligence-Hub/
│
├── backend/
│   ├── config.py
│   ├── document_loader.py
│   ├── rag.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── .env.example
├── .gitignore
└── README.md
```

## Run Locally

Clone the repository:

```bash
git clone https://github.com/Sayed-Md-Sharique/Engineering-Intelligence-Hub.git
cd Engineering-Intelligence-Hub
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

Create a `.env` file and add:

```env
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
HF_TOKEN=your_huggingface_token
```

Start the backend:

```bash
cd backend
uvicorn main:app --reload
```

Start the frontend in another terminal:

```bash
cd frontend
streamlit run app.py
```

## Live Demo

**Frontend:**
https://engineering-intelligence.streamlit.app/

**Backend:**
https://engineering-intelligence-hub.onrender.com/

## Use Cases

* Technical document search
* Developer onboarding
* Source-code Q&A
* Multi-document question answering
* Engineering knowledge retrieval


