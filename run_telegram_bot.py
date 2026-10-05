#!/usr/bin/env python3
"""
Organic Content OS - Telegram Bot Runner
----------------------------------------
Starts the Telegram bot in Long-Polling mode for local testing and production.
Creators and clients can send:
- Text prompts & agricultural topic ideas
- Instagram / TikTok / YouTube Shorts URLs
- Direct video uploads

The bot will automatically:
1. Deconstruct the mechanics with Gemini
2. Generate an original brand-safe script + storyboard
3. Run the Brand QA Critic against Organic Journals guardrails
4. Send interactive buttons to 1-click render the 9:16 FLUX video and upload it back to Telegram.
"""
import sys
import asyncio
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.app.config import get_telegram_bot_token, get_gemini_api_key
from backend.app.services.telegram_service import run_polling_loop

def main():
    print("=" * 60)
    print("🌱 Organic Content OS - Telegram Bot Interface")
    print("=" * 60)
    
    bot_token = get_telegram_bot_token()
    if not bot_token:
        print("❌ Error: TELEGRAM_BOT_TOKEN is not set in your .env file!")
        print("\nTo configure your bot:")
        print("1. Create a bot with @BotFather on Telegram")
        print("2. Add TELEGRAM_BOT_TOKEN=your_token_here to your .env file")
        print("3. Run this script again: python run_telegram_bot.py\n")
        sys.exit(1)

    gemini_key = get_gemini_api_key()
    if not gemini_key:
        print("⚠️ Warning: GEMINI_API_KEY is not configured. Script generation will fail.")

    try:
        asyncio.run(run_polling_loop())
    except KeyboardInterrupt:
        print("\n👋 Telegram Bot stopped gracefully.")

if __name__ == "__main__":
    main()
