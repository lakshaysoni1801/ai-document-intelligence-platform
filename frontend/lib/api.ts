import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export const api = axios.create({ baseURL: API_BASE });

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await api.post("/api/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function queryDocuments(question: string) {
  const res = await api.post("/api/query", { question });
  return res.data;
}

export async function queryChart(question: string) {
  const res = await api.post("/api/chart", { question });
  return res.data;
}

export async function getDocuments() {
  const res = await api.get("/api/documents");
  return res.data;
}
