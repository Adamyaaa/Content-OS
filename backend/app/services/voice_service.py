import asyncio
from pathlib import Path
import edge_tts

DEFAULT_VOICE = "en-US-ChristopherNeural"  # Clear, authentic documentary tone

async def generate_voiceover_async(text: str, output_file: Path, voice: str = DEFAULT_VOICE) -> Path:
    """Synthesizes text into high-fidelity neural MP3 using edge-tts (100% free, 0-OPEX)."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    if output_file.exists():
        output_file.unlink()
        
    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+3%", pitch="+0Hz")
    await communicate.save(str(output_file))
    return output_file

def generate_voiceover(text: str, output_file: Path, voice: str = DEFAULT_VOICE) -> Path:
    """Synchronous wrapper for generating voiceover audio."""
    if not text or not text.strip():
        raise ValueError("Cannot synthesize empty text")
        
    return asyncio.run(generate_voiceover_async(text, output_file, voice))
