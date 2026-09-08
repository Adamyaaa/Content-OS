# Organic Content OS

> **AI-Powered Content Intelligence & Generation for Organic Agriculture Brands**

A vertical-slice client-demo prototype designed for **Organic Journals**. The platform analyzes high-performing short-form agricultural reels, unpacks their underlying narrative & visual mechanics, generates brand-aligned original concepts and video scripts, and verifies safety through an automated Brand QA Critic.

---

## Core Pipeline

1. **Video Ingestion**: Upload reels in MP4, MOV, or WebM format.
2. **Media Extraction**: FFmpeg extracts high-fidelity audio and 6–8 representative visual keyframes.
3. **Speech Transcription**: Groq Whisper (`whisper-large-v3`) produces an accurate spoken transcript.
4. **Multimodal Analysis**: Gemini Flash analyzes visual cues, narrative pacing, hook structure, target audience, and key claims.
5. **Original Concept & Script Generation**: Identifies the underlying success pattern and drafts an original, brand-safe short-form video script with scene-by-scene visual directions and on-screen overlays.
6. **Brand QA & Critic**: Evaluates the generated concept against brand guardrails (tone, unsupported claims, originality, hook strength, CTA) and assigns a confidence score.
7. **SaaS Dashboard**: Displays original content breakdown, extracted intelligence, copyable script, visual storyboard, and QA audit results.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- FFmpeg (system PATH or automatic via `imageio-ffmpeg`)
- Groq API Key
- Google Gemini API Key

### Configuration
Copy `.env.example` to `.env` and provide your API keys:
```bash
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
```

---

*Initial scaffold prepared for client-demo prototype.*
