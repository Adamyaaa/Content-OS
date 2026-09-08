from google import genai
from google.genai import types

from backend.app.config import GEMINI_API_KEY
from backend.app.config.brand import BRAND_CONFIG
from backend.app.models.schemas import ContentAnalysis, GeneratedContent, QAResult
from backend.app.prompts.qa_prompt import QA_SYSTEM_PROMPT, get_qa_prompt
from backend.app.utils.json_helper import clean_json_response

def evaluate_brand_qa(
    analysis: ContentAnalysis,
    generated: GeneratedContent
) -> QAResult:
    """
    Run an independent QA critic evaluation against brand guardrails,
    unsupported claims (especially 'chemical-free'), originality, and hook strength.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise ValueError("Gemini API Key is not configured. Please add GEMINI_API_KEY to your .env file.")
        
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = get_qa_prompt(analysis.model_dump(), generated.model_dump(), BRAND_CONFIG)
    
    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash"]
    last_error = None
    
    for m_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=m_name,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    system_instruction=QA_SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            
            if not response.text:
                raise ValueError("Received empty response from QA critic model")
                
            parsed_json = clean_json_response(response.text)
            return QAResult.model_validate(parsed_json)
        except Exception as e:
            last_error = e
            print(f"QA critic attempt with {m_name} failed: {e}")
            continue
            
    raise RuntimeError(f"Brand QA evaluation failed: {last_error}")
