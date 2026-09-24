from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import uuid

from config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL
)

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=60,
    check_compatibility=False
)

def create_collection():
    collections = qdrant.get_collections().collections
    names = [collection.name for collection in collections]

    if COLLECTION_NAME not in names:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

def split_document(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.split_text(text)

def add_document(text, source):
    create_collection()

    chunks = split_document(text)
    vectors = embedding_model.encode(chunks).tolist()

    points = []

    for chunk, vector in zip(chunks, vectors):
            point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": chunk,
                "source": source
            }
        )
    points.append(point)

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return len(chunks)

def search_documents(question, top_k=5):
    question_vector = embedding_model.encode(question).tolist()

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=question_vector,
        limit=top_k
    ).points

    return results

def generate_answer(question, results):
    if not results:
        return "I could not find relevant information.", []

    context = "\n\n".join(
        result.payload["text"]
        for result in results
    )

    prompt = ChatPromptTemplate.from_template("""
You are an Engineering Knowledge Assistant.

Answer the question using ONLY the context below.
Do not invent information.

If the answer is not present in the context, say:
"I could not find this information in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
""")

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0
    )

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": question
    })

    sources = list(set(
        result.payload["source"]
        for result in results
    ))

    return response.content, sources
