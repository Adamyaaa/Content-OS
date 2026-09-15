from google import genai
from google.genai import types

from backend.app.config import get_gemini_api_key
from backend.app.config.brand import BRAND_CONFIG
from backend.app.models.schemas import ContentAnalysis, GeneratedContent
from backend.app.prompts.generation_prompt import GENERATION_SYSTEM_PROMPT, get_generation_prompt
from backend.app.utils.json_helper import clean_json_response

def generate_original_concept(analysis: ContentAnalysis) -> GeneratedContent:
    """
    Generate an original content concept, voiceover script, and scene breakdown
    based on the analyzed structural pattern, tailored for Organic Journals.
    """
    api_key = get_gemini_api_key()
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("Gemini API Key is not configured. Please configure your API key in Settings.")
        
    client = genai.Client(api_key=api_key)
    prompt = get_generation_prompt(analysis.model_dump(), BRAND_CONFIG)
    
    models_to_try = ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.1-pro-preview"]
    last_error = None
    
    import time
    for m_name in models_to_try:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=m_name,
                    contents=[prompt],
                    config=types.GenerateContentConfig(
                        system_instruction=GENERATION_SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.4
                    )
                )
                
                if not response.text:
                    raise ValueError("Received empty response from generation model")
                    
                parsed_json = clean_json_response(response.text)
                return GeneratedContent.model_validate(parsed_json)
            except Exception as e:
                last_error = e
                print(f"Content generation attempt with {m_name} (attempt {attempt+1}) failed: {e}")
                if "503" in str(e):
                    time.sleep(1.5)
                    continue
                break
                
    raise RuntimeError(f"Original content generation failed: {last_error}")
