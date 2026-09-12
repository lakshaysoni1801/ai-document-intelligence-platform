"""
vector_store.py
----------------
Job: save document chunks + their embeddings into MongoDB, and search
them later using MongoDB Atlas Vector Search.

IMPORTANT SETUP STEP (do this in MongoDB Atlas UI, not in code):
1. Go to your cluster -> Atlas Search -> Create Search Index
2. Choose "Vector Search" index, on collection "chunks"
3. Use this index definition (name it "vector_index"):

{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 768,
      "similarity": "cosine"
    }
  ]
}

Without this index, vector search queries below will fail.
"""

import os
from pymongo import MongoClient

import certifi
client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where())
db = client[os.getenv("MONGODB_DB", "doc_intelligence")]
chunks_collection = db["chunks"]
documents_collection = db["documents"]


def save_document(filename: str, file_url: str, extracted_text: str) -> str:
    """Saves a document record, returns its Mongo ID as a string."""
    doc = {
        "filename": filename,
        "file_url": file_url,
        "text_preview": extracted_text[:500],
    }
    result = documents_collection.insert_one(doc)
    return str(result.inserted_id)


def save_chunks(document_id: str, embedded_chunks: list[dict]):
    """Stores each chunk + its vector, tagged with the parent document."""
    records = [
        {
            "document_id": document_id,
            "text": c["text"],
            "embedding": c["embedding"],
        }
        for c in embedded_chunks
    ]
    if records:
        chunks_collection.insert_many(records)


def vector_search(query_embedding: list[float], top_k: int = 5) -> list[dict]:
    """
    Runs a $vectorSearch aggregation to find the most semantically
    similar chunks to the query.
    """
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": top_k,
            }
        },
        {
            "$project": {
                "text": 1,
                "document_id": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]
    return list(chunks_collection.aggregate(pipeline))


def list_documents() -> list[dict]:
    docs = list(documents_collection.find({}, {"filename": 1, "file_url": 1}))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs
