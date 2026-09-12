# AI-Powered Document Intelligence Platform

## Setup

### 1. MongoDB Atlas
- Create a free cluster at mongodb.com/atlas
- Get your connection string
- After you upload at least one document (step 4 below), create a Vector Search index:
  - Atlas UI -> your cluster -> Search -> Create Search Index -> JSON editor
  - Collection: `chunks`, Index name: `vector_index`
  - Use the JSON shown in `backend/services/vector_store.py`

### 2. Gemini API key
- Go to aistudio.google.com, create a free API key

### 3. Cloudinary
- Sign up free at cloudinary.com, grab cloud name / api key / api secret from dashboard

### 4. Backend
```
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then fill in your keys
uvicorn main:app --reload --port 8000
```

### 5. Frontend
```
cd frontend
npm install
echo "NEXT_PUBLIC_API_BASE=http://localhost:8000" > .env.local
npm run dev
```

Open http://localhost:3000

## How it works
1. Upload PDF/DOCX -> text extracted -> stored on Cloudinary -> chunked -> embedded with Gemini -> stored in MongoDB
2. Ask a question -> agent breaks it into sub-queries -> vector search finds relevant chunks -> Gemini synthesizes an answer
3. Chart requests -> same retrieval, then Gemini extracts numeric data as structured JSON for recharts to render

## Known limitations (be ready to discuss these in interviews)
- Table extraction from PDFs is basic (pypdf); pdfplumber/camelot would improve it
- No auth/user separation yet
- No streaming responses (answers arrive all at once)
- No caching of embeddings for repeated documents
- Free tier Gemini API allows only 20 requests/day per model — hit this during testing, had to switch to a second API key from a different Google Cloud project
- Gemini model names change frequently (had to update from gemini-1.5-flash to gemini-2.5-flash to gemini-3.6-flash during development) — check Google's model list if you get a 404 error
