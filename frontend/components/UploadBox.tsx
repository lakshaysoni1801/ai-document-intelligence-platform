"use client";

import { useState } from "react";
import { uploadDocument } from "@/lib/api";

export default function UploadBox({ onUploaded }: { onUploaded: () => void }) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  async function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setError("");
    try {
      await uploadDocument(file);
      onUploaded();
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="border-2 border-dashed border-slate-600 rounded-xl p-6 text-center">
      <input
        type="file"
        accept=".pdf,.docx"
        onChange={handleChange}
        disabled={uploading}
        className="text-sm"
      />
      {uploading && <p className="mt-2 text-sm text-slate-400">Uploading & indexing...</p>}
      {error && <p className="mt-2 text-sm text-red-400">{error}</p>}
    </div>
  );
}
