"""
embeddings.py
-------------
Job: split long text into chunks, then turn each chunk into a vector
(a list of numbers) using Gemini's embedding model. These vectors are
what let us do semantic search later (finding relevant chunks by
*meaning*, not just keyword match).
"""

import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBEDDING_MODEL = "models/gemini-embedding-001"


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """
    Splits text into overlapping chunks.

    Why overlap? If we cut chunks with zero overlap, a sentence that
    spans the cut point loses context. A little overlap (e.g. 100
    chars) keeps neighboring chunks connected.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return [c.strip() for c in chunks if c.strip()]


def embed_text(text: str) -> list[float]:
    """Calls Gemini's embedding API for a single piece of text."""
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_document",
        output_dimensionality=768,
    )
    return result["embedding"]


def embed_query(text: str) -> list[float]:
    """
    Same as embed_text, but tagged as a 'query' embedding.
    Gemini embeds queries and documents slightly differently
    for better retrieval accuracy.
    """
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_query",
        output_dimensionality=768,
    )
    return result["embedding"]


def embed_chunks(chunks: list[str]) -> list[dict]:
    """Returns [{'text': ..., 'embedding': [...]}, ...]"""
    embedded = []
    for chunk in chunks:
        vector = embed_text(chunk)
        embedded.append({"text": chunk, "embedding": vector})
    return embedded
