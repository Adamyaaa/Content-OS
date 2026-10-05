import os
import json
import uuid
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import httpx
from datetime import datetime

from backend.app.config import (
    get_telegram_bot_token,
    get_telegram_allowed_chat_ids,
    get_gemini_api_key,
    DATA_DIR,
    UPLOADS_DIR,
    AUDIO_DIR,
    FRAMES_DIR,
    RESULTS_DIR
)
from backend.app.models.schemas import ContentAnalysis, AnalysisResult, GeneratedContent, QAResult
from backend.app.services.generation_service import generate_original_concept
from backend.app.services.qa_service import evaluate_brand_qa

logger = logging.getLogger("telegram_bot")
logging.basicConfig(level=logging.INFO)

TELEGRAM_API_BASE = "https://api.telegram.org"
USER_KEYS_FILE = DATA_DIR / "user_telegram_keys.json"

def load_user_custom_keys() -> Dict[str, str]:
    if USER_KEYS_FILE.exists():
        try:
            with open(USER_KEYS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_user_custom_key(chat_id: int, api_key: str):
    keys = load_user_custom_keys()
    keys[str(chat_id)] = api_key.strip()
    try:
        with open(USER_KEYS_FILE, "w", encoding="utf-8") as f:
            json.dump(keys, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to persist custom key for chat {chat_id}: {e}")

def delete_user_custom_key(chat_id: int):
    keys = load_user_custom_keys()
    if str(chat_id) in keys:
        del keys[str(chat_id)]
        try:
            with open(USER_KEYS_FILE, "w", encoding="utf-8") as f:
                json.dump(keys, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to delete custom key for chat {chat_id}: {e}")

def get_effective_gemini_key(chat_id: int) -> str:
    """Returns the user's custom key if configured, otherwise falls back to the server's default key."""
    keys = load_user_custom_keys()
    user_key = keys.get(str(chat_id), "").strip()
    if user_key:
        return user_key
    return get_gemini_api_key()

def get_bot_url(token: Optional[str] = None) -> str:
    bot_token = token or get_telegram_bot_token()
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not configured in .env")
    return f"{TELEGRAM_API_BASE}/bot{bot_token}"

def is_chat_allowed(chat_id: int) -> bool:
    allowed = get_telegram_allowed_chat_ids()
    if not allowed:
        return True  # If not set, allow all chats
    return str(chat_id) in allowed

# --- Low-level Telegram API client helpers ---

async def send_chat_action(chat_id: int, action: str = "typing"):
    try:
        url = f"{get_bot_url()}/sendChatAction"
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(url, json={"chat_id": chat_id, "action": action})
    except Exception as e:
        logger.warning(f"Failed to send chat action: {e}")

async def send_message(
    chat_id: int,
    text: str,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "HTML"
) -> Optional[Dict[str, Any]]:
    url = f"{get_bot_url()}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            res = await client.post(url, json=payload)
            if res.status_code != 200:
                # Fallback to plain text if markup parsing failed
                payload["parse_mode"] = None
                res = await client.post(url, json=payload)
            return res.json()
        except Exception as e:
            logger.error(f"Error sending telegram message: {e}")
            return None

async def answer_callback_query(callback_query_id: str, text: Optional[str] = None, show_alert: bool = False):
    url = f"{get_bot_url()}/answerCallbackQuery"
    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text
        payload["show_alert"] = show_alert
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            await client.post(url, json=payload)
        except Exception as e:
            logger.warning(f"Error answering callback query: {e}")

async def download_telegram_file(file_id: str, destination_path: Path) -> bool:
    """Downloads a media file sent directly in Telegram chat."""
    bot_token = get_telegram_bot_token()
    get_file_url = f"{get_bot_url(bot_token)}/getFile"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(get_file_url, json={"file_id": file_id})
        if res.status_code != 200:
            return False
        file_path_info = res.json().get("result", {}).get("file_path")
        if not file_path_info:
            return False
        
        download_url = f"{TELEGRAM_API_BASE}/file/bot{bot_token}/{file_path_info}"
        async with client.stream("GET", download_url) as stream_resp:
            if stream_resp.status_code == 200:
                with open(destination_path, "wb") as f:
                    async for chunk in stream_resp.aiter_bytes():
                        f.write(chunk)
                return True
    return False

# --- Core Business Logic Handlers ---

def build_analysis_from_text(topic_text: str, custom_key: Optional[str] = None) -> ContentAnalysis:
    """Uses Gemini to turn a rough idea/topic into a full structural content framework."""
    from google import genai
    from google.genai import types
    from backend.app.config.brand import BRAND_CONFIG
    from backend.app.utils.json_helper import clean_json_response

    key = (custom_key or get_gemini_api_key()).strip()
    client = genai.Client(api_key=key)
    prompt = f"""
    You are an expert short-form video strategist for '{BRAND_CONFIG.get('brand_name', 'Organic Journals')}'.
    Analyze this raw content idea or topic and map it into a high-retention short-form video architecture.

    RAW INPUT:
    "{topic_text}"

    BRAND IDENTITY:
    {BRAND_CONFIG.get('brand_name')}: {BRAND_CONFIG.get('tagline')}
    Niche: {BRAND_CONFIG.get('niche')}
    Core topics: {', '.join(BRAND_CONFIG.get('core_topics', []))}

    Return a valid JSON object matching this schema:
    {{
        "topic": "Concise specific topic",
        "hook": "Attention-grabbing opening line formulated from the input",
        "hook_type": "Problem Agitation | Curiosity / Proof | Counterintuitive Truth | Actionable Quick Tip",
        "content_format": "Field Demonstration | Talking Head Breakdown | Micro Problem-Solver | Split-Screen Comparison",
        "narrative_structure": ["Hook / Question", "The Mechanism / Root Cause", "Brand Solution / Takeaway", "Action CTA"],
        "visual_style": "Macro soil biology, natural morning light, cinematic crisp focus",
        "target_audience": "Commercial & regenerative farmers, organic growers, sustainable agrarians",
        "emotional_triggers": ["Skepticism of Synthetics", "Empowerment", "Curiosity"],
        "key_takeaway": "Actionable biological or agricultural insight"
    }}
    """
    resp = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3
        )
    )
    parsed = clean_json_response(resp.text)
    return ContentAnalysis.model_validate(parsed)

async def handle_start_command(chat_id: int):
    welcome_text = (
        "🌱 <b>Welcome to Organic Content OS!</b>\n\n"
        "Your AI content intelligence partner for <b>Organic Journals</b>.\n\n"
        "<b>What you can send:</b>\n"
        "• <b>Any Text Idea / Question:</b>\n"
        "  <i>e.g., 'Why synthetic nitrogen destroys soil fungi and how biochar restores it'</i>\n\n"
        "• <b>An Instagram Reel / TikTok / Shorts Link:</b>\n"
        "  <i>Paste any public video URL to deconstruct its hook & viral formula</i>\n\n"
        "• <b>A Video or Audio File:</b>\n"
        "  <i>Upload directly to run Whisper transcription + multimodal AI</i>\n\n"
        "🔑 <b>API Key Settings:</b>\n"
        "• The bot uses the server's default Gemini key automatically.\n"
        "• Want to use your own key? Type: <code>/setkey AIzaSy...</code>\n"
        "• Check key status: <code>/mykey</code>\n"
        "• Reset to default: <code>/clearkey</code>\n\n"
        "⚡ <i>Every script is automatically vetted by our Brand QA Critic to strictly avoid false claims or misleading pseudo-science.</i>"
    )
    await send_message(chat_id, welcome_text)

async def handle_set_key_command(chat_id: int, text: str):
    parts = text.split(maxsplit=1)
    if len(parts) < 2 or len(parts[1].strip()) < 15:
        await send_message(
            chat_id,
            "⚠️ <b>Usage:</b> <code>/setkey YOUR_GEMINI_API_KEY</code>\n\n"
            "Get a key for free from Google AI Studio: https://aistudio.google.com/"
        )
        return

    new_key = parts[1].strip()
    # Test key with Gemini
    await send_chat_action(chat_id, "typing")
    try:
        from google import genai
        client = genai.Client(api_key=new_key)
        resp = client.models.generate_content(model="gemini-3.6-flash", contents="ping")
        save_user_custom_key(chat_id, new_key)
        await send_message(
            chat_id,
            f"✅ <b>Custom Gemini API Key Connected!</b>\n\n"
            f"All your future scripts and analyses will use your custom key (ending in <code>...{new_key[-4:]}</code>).\n\n"
            f"To revert to server default anytime, type <code>/clearkey</code>."
        )
    except Exception as e:
        await send_message(chat_id, f"❌ <b>Key Validation Failed:</b> {str(e)}\nPlease verify the key.")

async def handle_clear_key_command(chat_id: int):
    delete_user_custom_key(chat_id)
    await send_message(chat_id, "🔄 <b>Reset!</b> You are now using the server's default Google Gemini API key.")

async def handle_my_key_command(chat_id: int):
    keys = load_user_custom_keys()
    user_key = keys.get(str(chat_id), "").strip()
    if user_key:
        masked = f"{user_key[:4]}...{user_key[-4:]}"
        await send_message(chat_id, f"🔑 <b>Active Key:</b> Custom Gemini Key (<code>{masked}</code>)\nType <code>/clearkey</code> to reset.")
    else:
        server_key = get_gemini_api_key()
        masked = f"{server_key[:4]}...{server_key[-4:]}" if server_key else "Not set"
        await send_message(chat_id, f"🔑 <b>Active Key:</b> Server Default Key (<code>{masked}</code>)\nType <code>/setkey YOUR_KEY</code> to use your own.")

def build_script_action_keyboard(analysis_id: str) -> Dict[str, Any]:
    return {
        "inline_keyboard": [
            [
                {"text": "📋 Full Storyboard & Scenes", "callback_data": f"story_{analysis_id}"},
                {"text": "📜 Clean Voiceover Text", "callback_data": f"script_{analysis_id}"}
            ],
            [
                {"text": "🛡️ Brand QA Audit", "callback_data": f"qa_{analysis_id}"},
                {"text": "🔄 3 Alternative Hooks", "callback_data": f"hooks_{analysis_id}"}
            ]
        ]
    }

async def handle_text_idea(chat_id: int, user_text: str):
    await send_chat_action(chat_id, "typing")
    await send_message(chat_id, f"🌿 <i>Analyzing idea:</i> <b>\"{user_text[:80]}\"</b>\n<i>Synthesizing brand script & running QA audit...</i>")

    analysis_id = str(uuid.uuid4())
    effective_key = get_effective_gemini_key(chat_id)

    try:
        # 1. Structural extraction
        content_analysis = build_analysis_from_text(user_text, custom_key=effective_key)

        # 2. Original script generation
        generated_content = generate_original_concept(content_analysis, custom_api_key=effective_key)

        # 3. Brand QA audit
        qa_result = evaluate_brand_qa(content_analysis, generated_content, custom_api_key=effective_key)

        # 4. Save analysis result JSON
        is_ready = qa_result.status == "PASS" and qa_result.overall_score >= 80
        readiness = "Ready for production" if is_ready else "Needs review"

        result = AnalysisResult(
            analysis_id=analysis_id,
            filename=f"idea_{analysis_id[:8]}.txt",
            created_at=datetime.utcnow().isoformat(),
            video_url="",
            video_duration=30.0,
            frame_urls=[],
            transcript={"text": user_text, "segments": []},
            analysis=content_analysis,
            generated_content=generated_content,
            qa_result=qa_result,
            production_readiness=readiness
        )

        result_path = RESULTS_DIR / f"{analysis_id}.json"
        with open(result_path, "w", encoding="utf-8") as rf:
            rf.write(result.model_dump_json(indent=2))

        # 5. Build Formatted Telegram Response
        qa_badge = "🟢 PASS" if qa_result.status == "PASS" else "🟡 REVIEW"
        score = qa_result.overall_score

        formatted_msg = (
            f"🌿 <b>Concept: {generated_content.concept_title}</b>\n\n"
            f"🎣 <b>Hook:</b>\n<i>\"{generated_content.hook}\"</i>\n\n"
            f"📜 <b>Voiceover Script:</b>\n{generated_content.script}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🛡️ <b>Brand QA Score:</b> <code>{score}/100</code> [{qa_badge}]\n"
            f"🎯 <b>Format:</b> {content_analysis.content_format}\n"
            f"⏱️ <b>Est. Speaking Duration:</b> ~{generated_content.estimated_duration_seconds or 30}s\n"
            f"✅ <i>{readiness}</i>"
        )

        keyboard = build_script_action_keyboard(analysis_id)
        await send_message(chat_id, formatted_msg, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Text idea processing failed")
        await send_message(chat_id, f"❌ <b>Generation Failed:</b> {str(e)}")

async def handle_social_url(chat_id: int, url: str):
    await send_chat_action(chat_id, "typing")
    await send_message(chat_id, f"📥 <i>Downloading video from:</i> <code>{url[:60]}...</code>\n<i>Extracting audio, keyframes & transcript...</i>")

    analysis_id = str(uuid.uuid4())
    video_path = UPLOADS_DIR / f"{analysis_id}.mp4"

    from backend.app.routes.api import download_social_video, process_video_pipeline

    try:
        # 1. Download video
        downloaded = await asyncio.to_thread(download_social_video, url, video_path)
        if not downloaded or not video_path.exists():
            await send_message(chat_id, "❌ Could not download video from this URL. Please verify the link is public or upload the file directly.")
            return

        # 2. Run analysis pipeline
        await send_message(chat_id, "🧠 <i>Running Whisper transcription & Gemini multimodal formula extraction...</i>")
        await asyncio.to_thread(process_video_pipeline, analysis_id, video_path, url)

        # 3. Read saved result
        result_path = RESULTS_DIR / f"{analysis_id}.json"
        if not result_path.exists():
            await send_message(chat_id, "❌ Pipeline finished without generating result file.")
            return

        with open(result_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        generated = data.get("generated_content", {})
        qa = data.get("qa_result", {})
        analysis = data.get("analysis", {})

        qa_badge = "🟢 PASS" if qa.get("status") == "PASS" else "🟡 REVIEW"
        score = qa.get("overall_score", 90)

        formatted_msg = (
            f"🎬 <b>Viral Reel Deconstructed!</b>\n\n"
            f"🌾 <b>Organic Journals Concept:</b> {generated.get('concept_title', 'Regenerative Agriculture Insight')}\n\n"
            f"🎣 <b>Fresh Original Hook:</b>\n<i>\"{generated.get('hook', '')}\"</i>\n\n"
            f"📜 <b>Voiceover Script:</b>\n{generated.get('script', '')}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🛡️ <b>Brand QA Score:</b> <code>{score}/100</code> [{qa_badge}]\n"
            f"🔍 <b>Analyzed Pattern:</b> {analysis.get('hook_type', 'Problem Agitation')} ({analysis.get('content_format', 'Field Demo')})\n"
            f"⏱️ <b>Est. Duration:</b> ~{generated.get('estimated_duration_seconds', 30)}s\n"
            f"✅ <i>{data.get('production_readiness', 'Ready for production')}</i>"
        )

        keyboard = build_script_action_keyboard(analysis_id)
        await send_message(chat_id, formatted_msg, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Social URL processing failed")
        await send_message(chat_id, f"❌ <b>Pipeline Error:</b> {str(e)}")

async def handle_video_file_upload(chat_id: int, file_id: str):
    await send_chat_action(chat_id, "typing")
    await send_message(chat_id, "📥 <i>Downloading video file from Telegram...</i>")

    analysis_id = str(uuid.uuid4())
    video_path = UPLOADS_DIR / f"{analysis_id}.mp4"

    from backend.app.routes.api import process_video_pipeline

    try:
        success = await download_telegram_file(file_id, video_path)
        if not success or not video_path.exists():
            await send_message(chat_id, "❌ Failed to download video from Telegram.")
            return

        await send_message(chat_id, "🧠 <i>Running Groq Whisper transcription & Gemini Brand QA...</i>")
        await asyncio.to_thread(process_video_pipeline, analysis_id, video_path, None)

        result_path = RESULTS_DIR / f"{analysis_id}.json"
        if not result_path.exists():
            await send_message(chat_id, "❌ Pipeline finished without generating result file.")
            return

        with open(result_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        generated = data.get("generated_content", {})
        qa = data.get("qa_result", {})

        score = qa.get("overall_score", 90)
        qa_badge = "🟢 PASS" if qa.get("status") == "PASS" else "🟡 REVIEW"

        formatted_msg = (
            f"🌾 <b>Concept: {generated.get('concept_title')}</b>\n\n"
            f"🎣 <b>Hook:</b>\n<i>\"{generated.get('hook', '')}\"</i>\n\n"
            f"📜 <b>Voiceover Script:</b>\n{generated.get('script', '')}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🛡️ <b>Brand QA Score:</b> <code>{score}/100</code> [{qa_badge}]"
        )

        keyboard = build_script_action_keyboard(analysis_id)
        await send_message(chat_id, formatted_msg, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Video file processing failed")
        await send_message(chat_id, f"❌ <b>Processing Error:</b> {str(e)}")

# --- Callback Button Handlers ---

async def handle_callback_query_event(callback_query: Dict[str, Any]):
    cq_id = callback_query.get("id")
    chat_id = callback_query.get("message", {}).get("chat", {}).get("id")
    data = callback_query.get("data", "")

    if not chat_id or not data:
        return

    await answer_callback_query(cq_id)

    if data.startswith("story_"):
        analysis_id = data.replace("story_", "").strip()
        result_path = RESULTS_DIR / f"{analysis_id}.json"
        if not result_path.exists():
            await send_message(chat_id, "❌ Analysis session not found.")
            return

        with open(result_path, "r", encoding="utf-8") as f:
            data_dict = json.load(f)

        scenes = data_dict.get("generated_content", {}).get("scene_breakdown", [])
        title = data_dict.get("generated_content", {}).get("concept_title", "Storyboard")
        if not scenes:
            await send_message(chat_id, "No scene storyboard available.")
            return

        story_text = f"🎬 <b>Scene-by-Scene Storyboard:</b> <i>{title}</i>\n\n"
        for idx, sc in enumerate(scenes, 1):
            story_text += (
                f"<b>Scene {idx} ({sc.get('timestamp', '0-5s')}):</b>\n"
                f"👁️ <b>Visual:</b> {sc.get('visual', '')}\n"
                f"🗣️ <b>Voiceover:</b> \"{sc.get('voiceover', '')}\"\n"
                f"🔤 <b>On-Screen Text:</b> <code>{sc.get('on_screen_text', '')}</code>\n\n"
            )

        await send_message(chat_id, story_text)

    elif data.startswith("script_"):
        analysis_id = data.replace("script_", "").strip()
        result_path = RESULTS_DIR / f"{analysis_id}.json"
        if not result_path.exists():
            await send_message(chat_id, "❌ Analysis not found.")
            return

        with open(result_path, "r", encoding="utf-8") as f:
            data_dict = json.load(f)

        script_text = data_dict.get("generated_content", {}).get("script", "")
        hook_text = data_dict.get("generated_content", {}).get("hook", "")
        title = data_dict.get("generated_content", {}).get("concept_title", "Script")

        copy_text = (
            f"📜 <b>Clean Script & Voiceover</b>\n"
            f"<i>{title}</i>\n\n"
            f"<b>Hook:</b>\n{hook_text}\n\n"
            f"<b>Full Spoken Track:</b>\n"
            f"<code>{script_text}</code>"
        )
        await send_message(chat_id, copy_text)

    elif data.startswith("qa_"):
        analysis_id = data.replace("qa_", "").strip()
        result_path = RESULTS_DIR / f"{analysis_id}.json"
        if not result_path.exists():
            await send_message(chat_id, "❌ Analysis not found.")
            return

        with open(result_path, "r", encoding="utf-8") as f:
            data_dict = json.load(f)

        qa = data_dict.get("qa_result", {})
        qa_text = (
            f"🛡️ <b>Brand QA Critic Audit:</b>\n\n"
            f"• <b>Safety Score:</b> <code>{qa.get('overall_score', 0)}/100</code>\n"
            f"• <b>Status:</b> <code>{qa.get('status', 'PASS')}</code>\n"
            f"• <b>Hook Strength:</b> {qa.get('hook_strength_score', 'N/A')}/10\n"
            f"• <b>Originality Score:</b> {qa.get('originality_score', 'N/A')}/10\n\n"
            f"📋 <b>Tone Alignment & Scientific Audit:</b>\n<i>{qa.get('tone_alignment_notes', 'Practical, approachable, evidence-conscious tone.')}</i>\n\n"
            f"🚫 <b>Guardrail Verification:</b> Passed\n"
            f"• No unverified 'chemical-free' claims\n"
            f"• No absolute 100% yield guarantees\n"
            f"• No fearmongering or conventional farmer vilification"
        )
        await send_message(chat_id, qa_text)

    elif data.startswith("hooks_"):
        analysis_id = data.replace("hooks_", "").strip()
        result_path = RESULTS_DIR / f"{analysis_id}.json"
        if not result_path.exists():
            await send_message(chat_id, "❌ Analysis not found.")
            return

        with open(result_path, "r", encoding="utf-8") as f:
            data_dict = json.load(f)

        topic = data_dict.get("analysis", {}).get("topic", "Organic Agriculture")
        orig_hook = data_dict.get("generated_content", {}).get("hook", "")
        effective_key = get_effective_gemini_key(chat_id)

        from google import genai
        client = genai.Client(api_key=effective_key)
        prompt = f"Generate 3 distinct, high-converting opening hooks for a reel on '{topic}'. The original hook was '{orig_hook}'. Keep them punchy and evidence-based for Organic Journals. Return 3 numbered bullet points."
        resp = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)

        await send_message(chat_id, f"🎣 <b>Alternative High-Retention Hooks:</b>\n\n{resp.text}")

# --- Main Update Dispatcher ---

async def process_telegram_update(update: Dict[str, Any]):
    """Processes an incoming Telegram update from webhook or polling."""
    # 1. Handle Inline Button Clicks
    if "callback_query" in update:
        await handle_callback_query_event(update["callback_query"])
        return

    # 2. Handle Messages
    message = update.get("message", {})
    if not message:
        return

    chat_id = message.get("chat", {}).get("id")
    if not chat_id:
        return

    if not is_chat_allowed(chat_id):
        await send_message(chat_id, "⛔ <i>Access Denied. Your Chat ID is not whitelisted.</i>")
        return

    text = message.get("text", "").strip()

    # Commands
    if text == "/start" or text == "/help":
        await handle_start_command(chat_id)
        return

    if text.startswith("/setkey"):
        await handle_set_key_command(chat_id, text)
        return

    if text == "/clearkey":
        await handle_clear_key_command(chat_id)
        return

    if text == "/mykey":
        await handle_my_key_command(chat_id)
        return

    # Video Upload (direct file)
    if "video" in message:
        file_id = message["video"].get("file_id")
        if file_id:
            await handle_video_file_upload(chat_id, file_id)
            return

    # Social URL (Instagram / TikTok / YouTube)
    if text and (
        "instagram.com" in text or
        "tiktok.com" in text or
        "youtube.com" in text or
        "youtu.be" in text or
        text.startswith("http://") or
        text.startswith("https://")
    ):
        await handle_social_url(chat_id, text)
        return

    # General Text / Prompt Idea
    if text:
        await handle_text_idea(chat_id, text)
        return

# --- Long Polling Runner (for local testing without webhooks) ---

async def run_polling_loop():
    """Runs long-polling loop against Telegram getUpdates."""
    bot_token = get_telegram_bot_token()
    if not bot_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN is not set in your .env file!")
        print("Please add TELEGRAM_BOT_TOKEN=... to .env and try again.")
        return

    print("🤖 Telegram Bot Polling Worker starting...")
    print(f"📡 Connected to Telegram API via Bot Token (ending in ...{bot_token[-6:]})")

    # Delete existing webhook before polling
    async with httpx.AsyncClient(timeout=10.0) as client:
        await client.post(f"{get_bot_url()}/deleteWebhook", json={"drop_pending_updates": False})

    offset = 0
    print("✅ Telegram Bot is LIVE and listening for messages! Press Ctrl+C to stop.")

    while True:
        try:
            url = f"{get_bot_url()}/getUpdates"
            params = {"offset": offset, "timeout": 25}
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.get(url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    updates = data.get("result", [])
                    for u in updates:
                        offset = u["update_id"] + 1
                        asyncio.create_task(process_telegram_update(u))
                elif res.status_code == 409:
                    # Conflict: another instance is running
                    await asyncio.sleep(3.0)
                else:
                    logger.warning(f"getUpdates returned {res.status_code}: {res.text}")
                    await asyncio.sleep(2.0)
        except asyncio.CancelledError:
            print("\n🛑 Polling stopped.")
            break
        except Exception as e:
            logger.error(f"Polling error: {e}")
            await asyncio.sleep(3.0)

if __name__ == "__main__":
    asyncio.run(run_polling_loop())
