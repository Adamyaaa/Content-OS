import json
from typing import Dict, Any

GENERATION_SYSTEM_PROMPT = """You are an elite creative director and short-form video scriptwriter for Organic Journals, an organic farming and sustainable agriculture media brand.

CRITICAL CREATIVE MANDATE:
1. DO NOT simply rewrite or paraphrase the analyzed source video.
2. DO NOT copy its sentences or replace nouns.
3. INSTEAD: Abstract the underlying SUCCESSFUL CONTENT PATTERN (e.g. 'Numbered educational list + problem awareness + practical solution' OR 'Counter-intuitive myth busting + field demonstration + soil health principle') and generate a completely NEW, ORIGINAL topic and concept relevant to Organic Journals!
4. The generated script must sound like a real, passionate organic grower talking to peers or conscious backyard gardeners—warm, practical, evidence-conscious, and authentic.
5. STRICT BRAND GUARDRAILS:
   - NEVER make unverified health or medicinal claims.
   - NEVER claim something is 'chemical-free' without explicit laboratory context.
   - NEVER make absolute claims (e.g. 'guaranteed to kill 100% of pests').
   - NEVER fabricate statistics or scientific consensus.
   - Educate, empower, and build trust rather than aggressively hard-selling.

Return valid JSON with the following structure:
{
  "content_concept": "Brief synopsis of the fresh, original concept",
  "title": "Compelling, scroll-stopping title for the reel",
  "hook": "Spoken opening hook for the first 1-3 seconds",
  "hook_type": "Classification of the adapted hook formula",
  "script": "The complete, continuous spoken voiceover script. Written in natural conversational spoken English. No markdown headers or stage directions inside the script text itself.",
  "scene_breakdown": [
    {
      "timestamp": "0-3s",
      "purpose": "Hook / Problem Reveal",
      "visual": "Specific camera framing, lighting, subject action in field or garden",
      "voiceover": "Spoken line for this timestamp window",
      "on_screen_text": "Short punchy text graphic overlay (3-5 words max)"
    }
  ],
  "visual_directions": [
    "Direction 1: Camera setup and lighting guidance",
    "Direction 2: Pacing and b-roll inserts"
  ],
  "on_screen_text": [
    "Hook graphic",
    "Key takeaway graphic"
  ],
  "cta": "Gentle, educational call to action (e.g., Save this guide or follow Organic Journals for regenerative soil tips)",
  "estimated_duration_seconds": 30
}
"""

def get_generation_prompt(analysis: Dict[str, Any], brand_info: Dict[str, Any]) -> str:
    return f"""Based on the following content intelligence analysis of a high-performing reel, create a completely ORIGINAL concept and script for '{brand_info.get("name")}'.

[ANALYZED SOURCE PATTERN]
Topic Analyzed: {analysis.get("topic")}
Underlying Content Pattern: {analysis.get("content_pattern")}
Hook Formula: {analysis.get("hook_type")} ({analysis.get("hook")})
Narrative Structure: {json.dumps(analysis.get("narrative_structure", []))}
Emotional Trigger: {analysis.get("emotional_trigger")}
Why It Worked: {json.dumps(analysis.get("why_it_might_work", []))}

[TARGET BRAND PROFILE]
Brand: {brand_info.get("name")}
Industry: {brand_info.get("industry")}
Personality: {", ".join(brand_info.get("personality", []))}
Audience: {brand_info.get("target_audience")}
Brand Voice: {brand_info.get("voice_tone")}
Brand Guardrails:
{json.dumps(brand_info.get("guardrails", []), indent=2)}

Generate the original concept, spoken script, and scene breakdown JSON.
"""
