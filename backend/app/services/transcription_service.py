import os
from pathlib import Path
from typing import Dict, Any
from groq import Groq
from backend.app.config import get_groq_api_key

def transcribe_audio(audio_path: Path) -> Dict[str, Any]:
    """
    Transcribe audio using Groq Whisper API.
    Returns:
    {
        "text": "...",
        "language": "en",
        "duration": 28.5
    }
    """
    api_key = get_groq_api_key()
    if not api_key or api_key == "your_groq_api_key_here":
        raise ValueError("Groq API Key is not configured. Please configure GROQ_API_KEY in Settings.")
        
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        client = Groq(api_key=api_key)
        
        with open(audio_path, "rb") as file_handle:
            transcription = client.audio.transcriptions.create(
                file=(audio_path.name, file_handle.read()),
                model="whisper-large-v3",
                response_format="verbose_json"
            )
            
        # verbose_json returns text, language, and duration
        text = getattr(transcription, "text", "") or ""
        language = getattr(transcription, "language", "en") or "en"
        duration = getattr(transcription, "duration", 0.0) or 0.0
        
        if not text.strip():
            text = "(No audible speech detected in video audio track)"
            
        return {
            "text": text.strip(),
            "language": language,
            "duration": round(float(duration), 2)
        }
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "authentication" in error_msg.lower():
            raise RuntimeError("Invalid Groq API Key. Please verify GROQ_API_KEY in your .env file.")
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            raise RuntimeError("Groq rate limit exceeded. Please wait a moment and try again.")
        else:
            raise RuntimeError(f"Transcription failed: {error_msg}")
