import os
import json
import google.generativeai as genai
from services.embeddings import embed_query
from services.vector_store import vector_search

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

PLANNER_PROMPT = """You are a retrieval planning agent. Given a user question,
decide how many separate search queries are needed to fully answer it, and
what they should be. Return ONLY valid JSON, no markdown fences, no preamble.

Format: {{"sub_queries": ["query1", "query2"]}}

User question: {question}
"""

SYNTH_PROMPT = """Answer the user's question using ONLY the context below.
If the context doesn't contain the answer, say so honestly.

Context:
{context}

Question: {question}

Answer:
"""


def plan_sub_queries(question: str) -> list[str]:
    resp = model.generate_content(PLANNER_PROMPT.format(question=question))
    try:
        parsed = json.loads(resp.text.strip())
        return parsed.get("sub_queries", [question])
    except Exception:
        return [question]


def retrieve_context(sub_queries: list[str], top_k: int = 5) -> list[dict]:
    all_chunks = []
    seen = set()
    for q in sub_queries:
        vector = embed_query(q)
        results = vector_search(vector, top_k=top_k)
        for r in results:
            if r["text"] not in seen:
                seen.add(r["text"])
                all_chunks.append(r)
    return all_chunks


def synthesize_answer(question: str, chunks: list[dict]) -> str:
    context = "\n\n---\n\n".join(c["text"] for c in chunks)
    resp = model.generate_content(SYNTH_PROMPT.format(context=context, question=question))
    return resp.text


def run_agent(question: str) -> dict:
    """Full pipeline: plan -> retrieve -> synthesize."""
    sub_queries = plan_sub_queries(question)
    chunks = retrieve_context(sub_queries)
    answer = synthesize_answer(question, chunks)
    return {
        "answer": answer,
        "sub_queries": sub_queries,
        "sources": [{"text": c["text"][:200], "score": c.get("score")} for c in chunks],
        "full_chunks": [c["text"] for c in chunks],
    }
