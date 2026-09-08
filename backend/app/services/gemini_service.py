from pathlib import Path
from typing import List, Any
from PIL import Image
from google import genai
from google.genai import types

from backend.app.config import GEMINI_API_KEY
from backend.app.config.brand import BRAND_CONFIG
from backend.app.models.schemas import ContentAnalysis
from backend.app.prompts.analysis_prompt import ANALYSIS_SYSTEM_PROMPT, get_analysis_prompt
from backend.app.utils.json_helper import clean_json_response

def analyze_video_content(
    frame_paths: List[Path],
    transcript: str,
    duration: float
) -> ContentAnalysis:
    """
    Perform multimodal content intelligence analysis using Gemini.
    Passes representative keyframe images and spoken transcript.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise ValueError("Gemini API Key is not configured. Please add GEMINI_API_KEY to your .env file.")

    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = get_analysis_prompt(transcript, duration, BRAND_CONFIG)
    
    # Load frame images as PIL Images
    contents: List[Any] = [prompt]
    for fp in frame_paths:
        if fp.exists():
            try:
                img = Image.open(fp)
                contents.append(img)
            except Exception as e:
                print(f"Warning: Failed to load image {fp}: {e}")
                
    models_to_try = ["gemini-2.5-flash", "gemini-3.5-flash-lite", "gemini-2.5-pro"]
    last_error = None
    
    import time
    for m_name in models_to_try:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=m_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=ANALYSIS_SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.2
                    )
                )
                
                if not response.text:
                    raise ValueError("Received empty response from Gemini model")
                    
                parsed_json = clean_json_response(response.text)
                return ContentAnalysis.model_validate(parsed_json)
            except Exception as e:
                last_error = e
                print(f"Gemini analysis attempt with {m_name} (attempt {attempt+1}) failed: {e}")
                if "503" in str(e):
                    time.sleep(1.5)
                    continue
                break
            
    raise RuntimeError(f"Multimodal content analysis failed: {last_error}")
