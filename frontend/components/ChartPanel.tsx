"use client";

import { useState } from "react";
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { queryChart } from "@/lib/api";

const COLORS = ["#3b82f6", "#22c55e", "#f97316", "#a855f7", "#ef4444"];

export default function ChartPanel() {
  const [question, setQuestion] = useState("");
  const [chart, setChart] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function handleGenerate() {
    if (!question.trim()) return;
    setLoading(true);
    const data = await queryChart(question);
    setChart(data.chart);
    setLoading(false);
  }

  const chartData =
    chart?.labels?.map((label: string, i: number) => ({
      name: label,
      value: chart.values[i],
    })) || [];

  return (
    <div className="border border-slate-700 rounded-xl p-4 space-y-4">
      <div className="flex gap-2">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. Show revenue by quarter"
          className="flex-1 bg-slate-800 rounded-lg px-3 py-2 text-sm outline-none"
        />
        <button
          onClick={handleGenerate}
          className="bg-green-600 px-4 py-2 rounded-lg text-sm hover:bg-green-500"
        >
          {loading ? "..." : "Generate Chart"}
        </button>
      </div>

      {chart?.chart_type === "bar" && (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <XAxis dataKey="name" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip />
            <Bar dataKey="value" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      )}

      {chart?.chart_type === "line" && (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <XAxis dataKey="name" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip />
            <Line dataKey="value" stroke="#22c55e" />
          </LineChart>
        </ResponsiveContainer>
      )}

      {chart?.chart_type === "pie" && (
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie data={chartData} dataKey="value" nameKey="name" outerRadius={100}>
              {chartData.map((_: any, i: number) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      )}

      {chart && chart.chart_type === null && (
        <p className="text-sm text-slate-400">No numeric data found for that question.</p>
      )}
    </div>
  );
}
