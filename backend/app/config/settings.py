import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
CONFIG_DIR = Path(__file__).resolve().parent
APP_DIR = CONFIG_DIR.parent
BACKEND_DIR = APP_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(BACKEND_DIR / ".env")

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Server Config
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "127.0.0.1")

# Storage Directories
DATA_DIR = BACKEND_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
AUDIO_DIR = DATA_DIR / "audio"
FRAMES_DIR = DATA_DIR / "frames"
RESULTS_DIR = DATA_DIR / "results"

for d in [DATA_DIR, UPLOADS_DIR, AUDIO_DIR, FRAMES_DIR, RESULTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)
