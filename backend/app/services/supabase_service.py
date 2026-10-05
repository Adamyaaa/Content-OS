import os
from typing import List, Dict, Any, Optional
from datetime import datetime
try:
    from supabase import create_client, Client
except ImportError:
    Client = Any

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

def get_supabase_client() -> Optional[Client]:
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Warning: SUPABASE_URL or SUPABASE_KEY not set")
        return None
    try:
        from supabase import create_client
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        return None

def insert_trends(trends: List[Dict[str, Any]]) -> Dict:
    supabase = get_supabase_client()
    if not supabase:
        raise Exception("Supabase client not initialized")
    
    # Ensure trends have default pending_review status and timestamps
    formatted_trends = []
    for trend in trends:
        formatted_trends.append({
            "source_url": trend.get("source_url", ""),
            "topic": trend.get("topic", ""),
            "hook_idea": trend.get("hook_idea", ""),
            "source_platform": trend.get("source_platform", "unknown"),
            "status": "pending_review"
        })

    result = supabase.table("trend_queue").insert(formatted_trends).execute()
    return result

def get_pending_trends() -> List[Dict]:
    supabase = get_supabase_client()
    if not supabase:
        raise Exception("Supabase client not initialized")
    
    result = supabase.table("trend_queue").select("*").eq("status", "pending_review").execute()
    return result.data

def get_trend_by_id(trend_id: str) -> Optional[Dict]:
    supabase = get_supabase_client()
    if not supabase:
        raise Exception("Supabase client not initialized")
    
    result = supabase.table("trend_queue").select("*").eq("id", trend_id).execute()
    if result.data:
        return result.data[0]
    return None

def update_trend_status(trend_id: str, status: str, generated_script_id: Optional[str] = None) -> Dict:
    supabase = get_supabase_client()
    if not supabase:
        raise Exception("Supabase client not initialized")
    
    update_data = {
        "status": status,
        "updated_at": datetime.utcnow().isoformat()
    }
    if generated_script_id:
        update_data["generated_script_id"] = generated_script_id

    result = supabase.table("trend_queue").update(update_data).eq("id", trend_id).execute()
    return result
