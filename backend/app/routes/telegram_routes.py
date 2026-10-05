import os
import httpx
from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.app.config import get_telegram_bot_token
from backend.app.services.telegram_service import (
    process_telegram_update,
    get_bot_url,
    TELEGRAM_API_BASE
)

router = APIRouter(prefix="/api/telegram", tags=["telegram"])

class SetWebhookPayload(BaseModel):
    webhook_url: str

@router.get("/status")
async def get_telegram_status():
    """Checks if Telegram bot token is valid and gets bot profile info."""
    bot_token = get_telegram_bot_token()
    if not bot_token:
        return {
            "configured": False,
            "message": "TELEGRAM_BOT_TOKEN is not configured in .env"
        }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.get(f"{get_bot_url()}/getMe")
            if res.status_code == 200:
                bot_info = res.json().get("result", {})
                
                # Also check webhook status
                hook_res = await client.get(f"{get_bot_url()}/getWebhookInfo")
                hook_info = hook_res.json().get("result", {}) if hook_res.status_code == 200 else {}

                return {
                    "configured": True,
                    "bot_name": bot_info.get("first_name"),
                    "username": bot_info.get("username"),
                    "can_join_groups": bot_info.get("can_join_groups"),
                    "webhook_info": hook_info
                }
            return {
                "configured": False,
                "message": f"Telegram API returned {res.status_code}: {res.text}"
            }
    except Exception as e:
        return {
            "configured": False,
            "error": str(e)
        }

@router.post("/webhook")
async def telegram_webhook_endpoint(request: Request, background_tasks: BackgroundTasks):
    """Receives inbound Telegram updates when running in webhook mode."""
    try:
        update_data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    background_tasks.add_task(process_telegram_update, update_data)
    return {"ok": True}

@router.post("/set-webhook")
async def set_telegram_webhook(payload: SetWebhookPayload):
    """Helper endpoint to register or update the webhook URL with Telegram."""
    bot_token = get_telegram_bot_token()
    if not bot_token:
        raise HTTPException(status_code=400, detail="TELEGRAM_BOT_TOKEN is not configured")

    async with httpx.AsyncClient(timeout=15.0) as client:
        res = await client.post(
            f"{get_bot_url()}/setWebhook",
            json={"url": payload.webhook_url.strip()}
        )
        return res.json()

@router.post("/delete-webhook")
async def delete_telegram_webhook():
    """Removes the webhook URL (needed before switching to long-polling mode)."""
    bot_token = get_telegram_bot_token()
    if not bot_token:
        raise HTTPException(status_code=400, detail="TELEGRAM_BOT_TOKEN is not configured")

    async with httpx.AsyncClient(timeout=15.0) as client:
        res = await client.post(f"{get_bot_url()}/deleteWebhook")
        return res.json()
