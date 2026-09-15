import os
import json
import asyncio
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional

from backend.app.config import (
    get_elevenlabs_api_key,
    get_openai_api_key
)

DEFAULT_NEURAL_VOICE = "en-US-GuyNeural"  # Warm, authentic, natural American creator tone
ELEVENLABS_DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel / Crisp conversational voice
OPENAI_DEFAULT_VOICE = "onyx"  # Deep, warm, professional narrator

def generate_voiceover_elevenlabs(text: str, output_file: Path, voice_id: str = ELEVENLABS_DEFAULT_VOICE_ID) -> bool:
    """Synthesizes text using ElevenLabs API with human-grade prosody."""
    api_key = get_elevenlabs_api_key()
    if not api_key:
        return False
        
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.80,
            "style": 0.15,
            "use_speaker_boost": True
        }
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "wb") as f:
                f.write(resp.read())
        print("ElevenLabs voiceover synthesis succeeded!")
        return True
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        print(f"ElevenLabs TTS HTTP {e.code}: {err_body[:160]}")
        return False
    except Exception as e:
        print(f"ElevenLabs TTS error: {e}")
        return False

def generate_voiceover_openai(text: str, output_file: Path, voice: str = OPENAI_DEFAULT_VOICE) -> bool:
    """Synthesizes text using OpenAI TTS-1 API."""
    api_key = get_openai_api_key()
    if not api_key:
        return False
        
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "model": "tts-1",
        "input": text,
        "voice": voice
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "wb") as f:
                f.write(resp.read())
        print("OpenAI voiceover synthesis succeeded!")
        return True
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        print(f"OpenAI TTS HTTP {e.code}: {err_body[:160]}")
        return False
    except Exception as e:
        print(f"OpenAI TTS error: {e}")
        return False

async def generate_voiceover_edge_async(text: str, output_file: Path, voice: str = DEFAULT_NEURAL_VOICE) -> Path:
    """Synthesizes text into high-fidelity neural MP3 using Edge-TTS with natural cadence."""
    import edge_tts
    output_file.parent.mkdir(parents=True, exist_ok=True)
    if output_file.exists():
        output_file.unlink()
        
    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+0%", pitch="+0Hz")
    await communicate.save(str(output_file))
    return output_file

def generate_voiceover_edge(text: str, output_file: Path, voice: str = DEFAULT_NEURAL_VOICE) -> Path:
    """Synchronous/threaded wrapper for Edge-TTS."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(lambda: asyncio.run(generate_voiceover_edge_async(text, output_file, voice)))
            return future.result()
    else:
        return asyncio.run(generate_voiceover_edge_async(text, output_file, voice))

def generate_voiceover(
    text: str,
    output_file: Path,
    voice: Optional[str] = None
) -> Dict[str, Any]:
    """
    Multi-Tier Intelligent TTS Engine:
    1. Attempts ElevenLabs if API key configured and active.
    2. Attempts OpenAI TTS if API key configured and funded.
    3. Falls back to high-grade Edge-TTS neural voice (Guy / natural creator).
    """
    if not text or not text.strip():
        raise ValueError("Cannot synthesize empty text")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 1. ElevenLabs Tier
    el_key = get_elevenlabs_api_key()
    if el_key and el_key.startswith("sk_"):
        success = generate_voiceover_elevenlabs(text, output_file)
        if success and output_file.exists() and output_file.stat().st_size > 500:
            return {
                "path": output_file,
                "engine": "ElevenLabs",
                "voice": "Rachel / Creator Studio",
                "status": "success"
            }

    # 2. OpenAI Tier
    oai_key = get_openai_api_key()
    if oai_key and oai_key.startswith("sk-"):
        success = generate_voiceover_openai(text, output_file)
        if success and output_file.exists() and output_file.stat().st_size > 500:
            return {
                "path": output_file,
                "engine": "OpenAI TTS",
                "voice": "Onyx (Natural Narrator)",
                "status": "success"
            }

    # 3. High-Quality Neural Fallback (Free & Reliable)
    chosen_voice = voice or DEFAULT_NEURAL_VOICE
    generate_voiceover_edge(text, output_file, voice=chosen_voice)
    return {
        "path": output_file,
        "engine": "Neural HD Engine",
        "voice": f"{chosen_voice} (Natural Creator)",
        "status": "success"
    }

