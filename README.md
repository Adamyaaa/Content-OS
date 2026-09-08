# Organic Content OS

> **AI-Powered Content Intelligence & Generation for Organic Agriculture Brands**  
> *Client-Demo Prototype for Organic Journals*

Organic Content OS is a vertical-slice prototype demonstrating how high-performing short-form video reels can be ingested, analyzed down to their core structural and psychological formula, and transformed into brand-safe, original content concepts and production-ready video scripts for **Organic Journals**.

---

## Architecture Overview

```
User (Upload Reel: MP4/MOV/WEBM)
            │
            ▼
   React + Vite Frontend (Tailwind CSS, Lucide React)
            │  POST /api/analyze
            ▼
   FastAPI Application
            │
      ┌─────┴─────────────────┐
      │                       │
      ▼                       ▼
  FFmpeg Audio            FFmpeg Frames
  (16kHz Mono WAV)      (6-8 distributed keyframes)
      │                       │
      ▼                       │
  Groq Whisper API            │
  (Spoken Transcript)         │
      │                       │
      └───────────┬───────────┘
                  ▼
         Gemini 2.5 Flash
   (Multimodal Content Intelligence)
                  │
                  ▼
         Gemini 2.5 Flash
   (Original Concept & Script Generation)
                  │
                  ▼
      Gemini Brand QA Critic
   (Independent Compliance Audit against Guardrails)
                  │
                  ▼
      Local JSON Persistence & React Dashboard
```

---

## What the System Does

1. **Video Ingestion**: Accepts videos up to 120MB in `.mp4`, `.mov`, or `.webm`.
2. **Audio Extraction**: FFmpeg extracts audio normalized for speech recognition.
3. **Groq Whisper Transcription**: High-accuracy spoken dialogue transcription.
4. **Keyframe Extraction**: Extracts 7 representative visual frames spaced across the video runtime (0% to 90%).
5. **Multimodal Content Intelligence**: Gemini analyzes observable vs. inferred attributes:
   - Topic & Hook
   - Hook classification (Problem Agitation, Curiosity, Listicle, etc.)
   - Content Format (Field Demo, Talking Head, POV)
   - Narrative Structure (Step-by-step sequence)
   - Visual Style & Editing Pacing
   - Target Audience & Emotional Triggers
   - Underlying Content Pattern formula
6. **Brand-Safe Original Content Generation**:
   - **Does NOT** rewrite competitor scripts or substitute nouns.
   - Extracts the successful formula and invents a completely fresh, evidence-based topic for **Organic Journals**.
   - Generates an opening hook, complete spoken voiceover script, and scene-by-scene storyboard (visuals, voiceover lines, on-screen text overlays, CTA).
7. **Independent AI QA / Critic**:
   - Evaluates compliance against agricultural brand guardrails.
   - Strictly enforces rules (e.g., forbids scientifically invalid "chemical-free" claims, unverified health claims, or absolute yield guarantees).
   - Assigns a 0–100 safety score and declares `Ready for production` or `Needs review`.
8. **Client-Facing SaaS UI**:
   - Real-time pipeline status tracking.
   - Interactive media player and keyframe filmstrip.
   - One-click "Copy Full Script" action with estimated speaking pace.
   - Interactive history drawer to reload past analyses.
   - Instant "Explore Pre-analyzed Agriculture Reel Demo" button for zero-delay live client presentations.

---

## Prerequisites

- **Python**: 3.10, 3.11, 3.12, or 3.13
- **Node.js**: 18+ and npm
- **FFmpeg**: Bundled automatically via `imageio-ffmpeg` (or detected from system `PATH` if installed).
- **API Keys**:
  - `GROQ_API_KEY`: [Groq Console](https://console.groq.com/)
  - `GEMINI_API_KEY`: [Google AI Studio](https://aistudio.google.com/)

---

## Setup & Installation

### 1. Clone & Configure Environment

Create `.env` in the project root:
```bash
cp .env.example .env
```
Fill in your keys:
```env
GROQ_API_KEY=gsk_your_groq_api_key
GEMINI_API_KEY=AIzaSy_your_gemini_api_key
PORT=8000
HOST=127.0.0.1
```

### 2. Backend Setup

From the project root:
```bash
# Install Python dependencies
python -m pip install -r backend/requirements.txt

# Start the FastAPI backend server
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
The backend will be available at:
- API Root: `http://127.0.0.1:8000`
- Interactive API Docs: `http://127.0.0.1:8000/docs`
- Health Check: `http://127.0.0.1:8000/api/health`

### 3. Frontend Setup

In a separate terminal:
```bash
cd frontend

# Install Node dependencies
npm install

# Start Vite dev server
npm run dev
```
Open your browser at:
`http://localhost:5173`

---

## API Endpoints Reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/health` | Checks API key configuration and FFmpeg status |
| `POST` | `/api/analyze` | Multipart video upload (`file`). Runs the complete pipeline and returns structured JSON. |
| `GET` | `/api/analysis/{analysis_id}` | Retrieves a previously stored analysis by UUID |
| `GET` | `/api/analyses` | Lists past analyses for the history drawer |
| `GET` | `/data/*` | Serves uploaded videos and extracted keyframes |

---

## Brand DNA & Guardrails (`Organic Journals`)

Configured in [`backend/app/config/brand.py`](backend/app/config/brand.py):
- **Personality**: Educational, trustworthy, practical, approachable, evidence-conscious.
- **Strict Guardrails**:
  - Never make unsupported health claims.
  - Never claim a method or product is "chemical-free" unless verified (soil and water are chemicals; "chemical-free" is scientifically misleading).
  - Never make absolute agricultural claims ("guaranteed 100% pest eradication").
  - Never fabricate statistics or scientific facts.
  - Avoid fearmongering or vilifying conventional farmers.
  - Educate and build trust rather than aggressively hard-selling.

---

## Known Limitations of Prototype

- **Local Storage**: Uploads, keyframes, and results are persisted to local disk (`backend/data/`), not cloud storage.
- **Synchronous Upload Request**: The HTTP request completes once all stages finish (~10–18s depending on video length).
- **Single Brand Profile**: Currently configured for *Organic Journals*.

---

## Production Roadmap (Phases 2 – 5)

- **Phase 2 (Persistent Memory & Deduplication)**:
  - Supabase / PostgreSQL storage with `pgvector`.
  - Vector embeddings for hooks, scripts, and video concepts.
  - Cosine-similarity checks to avoid publishing repetitive themes.
- **Phase 3 (Ingestion & Delivery Integrations)**:
  - Make.com orchestration.
  - Telegram bot for on-the-go video uploads from field creators.
  - Notion workspace auto-sync for script approvals.
- **Phase 4 (Automated Discovery)**:
  - Meta Ad Library and Instagram Reels scraping.
  - Google Trends & agricultural keyword monitoring.
- **Phase 5 (Autonomous Learning Loop)**:
  - Ingest published reel retention curves and view-through rates.
  - Retrain/update the pattern library based on top-performing hooks.
