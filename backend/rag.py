import uuid

from huggingface_hub import InferenceClient
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    HF_TOKEN
)


# -------------------- Clients --------------------

hf_client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)

qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=60,
    check_compatibility=False
)


# -------------------- Embeddings --------------------

def create_embeddings(texts):

    result = hf_client.feature_extraction(
        texts,
        model=EMBEDDING_MODEL
    )

    return result.tolist()


# -------------------- Qdrant --------------------

def create_collection():

    collections = qdrant.get_collections().collections

    names = [
        collection.name
        for collection in collections
    ]

    if COLLECTION_NAME not in names:

        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


# -------------------- Chunking --------------------

def split_document(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    return splitter.split_text(text)


# -------------------- Add Document --------------------

def add_document(text, source):

    create_collection()

    chunks = split_document(text)

    vectors = create_embeddings(chunks)

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


# -------------------- Search --------------------

def search_documents(question, sources=None, top_k=5):
    question_vector = create_embeddings([question])[0]

    query_filter = None

    if sources:
        query_filter = {
            "should": [
                {
                    "key": "source",
                    "match": {
                        "value": source
                    }
                }
                for source in sources
            ]
        }

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=question_vector,
        query_filter=query_filter,
        limit=top_k
    ).points

    return results


# -------------------- Generate Answer --------------------

def generate_answer(question, results):

    if not results:
        return (
            "I could not find relevant information.",
            []
        )

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

    sources = list(
        set(
            result.payload["source"]
            for result in results
        )
    )

    return response.content, sources