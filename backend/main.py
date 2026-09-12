import os
from dotenv import load_dotenv
load_dotenv()

import cloudinary
import cloudinary.uploader
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.extraction import extract_document
from services.embeddings import chunk_text, embed_chunks
from services.vector_store import save_document, save_chunks, list_documents
from services.agent import run_agent
from services.chart_data import generate_chart_data

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

app = FastAPI(title="Doc Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    file_bytes = await file.read()

    try:
        extracted = extract_document(file.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    upload_result = cloudinary.uploader.upload(
        file_bytes, resource_type="raw", public_id=file.filename
    )
    file_url = upload_result.get("secure_url")

    document_id = save_document(file.filename, file_url, extracted["text"])

    chunks = chunk_text(extracted["text"])
    embedded_chunks = embed_chunks(chunks)
    save_chunks(document_id, embedded_chunks)

    return {
        "document_id": document_id,
        "filename": file.filename,
        "num_chunks": len(chunks),
        "file_url": file_url,
    }


@app.post("/api/query")
async def query_documents(req: QueryRequest):
    result = run_agent(req.question)
    return result


@app.post("/api/chart")
async def query_chart(req: QueryRequest):
    agent_result = run_agent(req.question)
    context_text = "\n".join(agent_result["full_chunks"])
    chart = generate_chart_data(req.question, context_text)
    return {"chart": chart, "answer": agent_result["answer"]}


@app.get("/api/documents")
async def get_documents():
    return list_documents()


@app.get("/api/health")
async def health():
    return {"status": "ok"}
