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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
PIAPI_KEY = os.getenv("PIAPI_KEY", "").strip()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "").strip()

def get_groq_api_key() -> str:
    return os.getenv("GROQ_API_KEY", GROQ_API_KEY).strip()

def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY", GEMINI_API_KEY).strip()

def get_openai_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", OPENAI_API_KEY).strip()

def get_elevenlabs_api_key() -> str:
    return os.getenv("ELEVENLABS_API_KEY", ELEVENLABS_API_KEY).strip()

def get_piapi_key() -> str:
    return os.getenv("PIAPI_KEY", PIAPI_KEY).strip()

def get_rapidapi_key() -> str:
    return os.getenv("RAPIDAPI_KEY", RAPIDAPI_KEY).strip()

def reload_settings():
    global GROQ_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY, ELEVENLABS_API_KEY, PIAPI_KEY, RAPIDAPI_KEY
    load_dotenv(PROJECT_ROOT / ".env", override=True)
    load_dotenv(BACKEND_DIR / ".env", override=True)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
    PIAPI_KEY = os.getenv("PIAPI_KEY", "").strip()
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "").strip()

def update_api_keys(new_keys: dict) -> bool:
    """Updates .env file and reloads in-memory variables without restarting server."""
    env_path = PROJECT_ROOT / ".env"
    lines = []
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    
    updated_keys = set()
    new_lines = []
    for line in lines:
        matched = False
        for k, v in new_keys.items():
            if line.strip().startswith(f"{k}=") or line.strip().startswith(f"#{k}="):
                new_lines.append(f'{k}="{v}"\n')
                updated_keys.add(k)
                matched = True
                break
        if not matched:
            new_lines.append(line)
            
    for k, v in new_keys.items():
        if k not in updated_keys:
            new_lines.append(f'{k}="{v}"\n')
            
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
        
    for k, v in new_keys.items():
        os.environ[k] = str(v)
        
    reload_settings()
    return True

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
