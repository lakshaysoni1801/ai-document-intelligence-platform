"use client";

import { useState } from "react";
import UploadBox from "@/components/UploadBox";
import ChatBox from "@/components/ChatBox";
import ChartPanel from "@/components/ChartPanel";

export default function Home() {
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <main className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">AI Document Intelligence Platform</h1>

      <section>
        <h2 className="text-lg font-semibold mb-2">1. Upload a document</h2>
        <UploadBox onUploaded={() => setRefreshKey((k) => k + 1)} />
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-2">2. Ask questions</h2>
        <ChatBox key={`chat-${refreshKey}`} />
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-2">3. Generate charts</h2>
        <ChartPanel key={`chart-${refreshKey}`} />
      </section>
    </main>
  );
}
