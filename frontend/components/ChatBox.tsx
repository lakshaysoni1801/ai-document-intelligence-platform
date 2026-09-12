"use client";

import { useState } from "react";
import { queryDocuments } from "@/lib/api";

type Message = { role: "user" | "assistant"; text: string; sources?: any[] };

export default function ChatBox() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSend() {
    if (!input.trim()) return;
    const question = input;
    setMessages((m) => [...m, { role: "user", text: question }]);
    setInput("");
    setLoading(true);

    try {
      const data = await queryDocuments(question);
      setMessages((m) => [
        ...m,
        { role: "assistant", text: data.answer, sources: data.sources },
      ]);
    } catch (err) {
      setMessages((m) => [...m, { role: "assistant", text: "Something went wrong." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-[500px] border border-slate-700 rounded-xl">
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
            <span
              className={`inline-block px-3 py-2 rounded-lg max-w-[80%] ${
                m.role === "user" ? "bg-blue-600" : "bg-slate-700"
              }`}
            >
              {m.text}
            </span>
          </div>
        ))}
        {loading && <p className="text-sm text-slate-400">Thinking...</p>}
      </div>
      <div className="flex gap-2 p-3 border-t border-slate-700">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask something about your documents..."
          className="flex-1 bg-slate-800 rounded-lg px-3 py-2 text-sm outline-none"
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 px-4 py-2 rounded-lg text-sm hover:bg-blue-500"
        >
          Send
        </button>
      </div>
    </div>
  );
}
