import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

CHART_PROMPT = """Given the context below, extract any numeric data suitable
for a chart and return ONLY valid JSON in this exact format, no markdown, no
extra text:

{{
  "chart_type": "bar" | "line" | "pie",
  "title": "string",
  "labels": ["label1", "label2"],
  "values": [number1, number2]
}}

If there is no meaningful numeric data, return {{"chart_type": null}}.

Context:
{context}

Question: {question}
"""


def generate_chart_data(question: str, context_text: str) -> dict:
    resp = model.generate_content(CHART_PROMPT.format(context=context_text, question=question))
    raw = resp.text.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
    print("=== CHART DEBUG ===")
    print("CONTEXT LENGTH:", len(context_text))
    print("HAS Q1 DATA:", "45 lakhs" in context_text or "Q1" in context_text)
    print("FULL CONTEXT:", context_text)
    print("RAW GEMINI OUTPUT:", raw)
    print("===================")
    try:
        return json.loads(raw.strip())
    except Exception as e:
        return {"chart_type": None}