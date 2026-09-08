import json
import re
from typing import Any, Dict

def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """
    Extracts and parses JSON from model output, handling potential markdown fences (```json ... ```)
    or preamble/postamble.
    """
    if not raw_text:
        raise ValueError("Empty response from AI model")

    text = raw_text.strip()
    
    # Remove markdown code block fences if present
    if "```" in text:
        # Match ```json { ... } ``` or ``` { ... } ```
        pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            text = match.group(1).strip()
            
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
        
    # Find outer bracket { ... }
    first_bracket = text.find("{")
    last_bracket = text.rfind("}")
    if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
        bracketed = text[first_bracket:last_bracket + 1]
        try:
            return json.loads(bracketed)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON content: {e}. Raw snippet: {bracketed[:200]}")

    raise ValueError(f"No valid JSON object found in response: {raw_text[:200]}")
