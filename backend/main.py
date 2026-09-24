import os
import tempfile

from fastapi import FastAPI, UploadFile, File

from document_loader import load_file
from rag import add_document, search_documents, generate_answer

app = FastAPI(title="Engineering Intelligence Hub")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    ) as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        text = load_file(temp_path)
        chunk_count = add_document(
            text,
            file.filename
        )
    finally:
        os.remove(temp_path)

    return {
        "message": "Document uploaded successfully",
        "file": file.filename,
        "chunks": chunk_count
    }

@app.post("/query")
def query(
    question: str,
    sources: list[str] | None = None
):
    results = search_documents(
        question,
        sources=sources
    )

    answer, result_sources = generate_answer(
        question,
        results
    )

    return {
        "answer": answer,
        "sources": result_sources
    }