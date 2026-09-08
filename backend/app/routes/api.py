import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from backend.app.config import (
    UPLOADS_DIR,
    AUDIO_DIR,
    FRAMES_DIR,
    RESULTS_DIR,
    GROQ_API_KEY,
    GEMINI_API_KEY
)
from backend.app.models.schemas import AnalysisResult
from backend.app.services.video_service import (
    extract_audio,
    extract_representative_frames,
    get_video_duration,
    get_ffmpeg_path
)
from backend.app.services.transcription_service import transcribe_audio
from backend.app.services.gemini_service import analyze_video_content
from backend.app.services.generation_service import generate_original_concept
from backend.app.services.qa_service import evaluate_brand_qa

router = APIRouter(prefix="/api")

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}
MAX_FILE_SIZE_BYTES = 120 * 1024 * 1024  # 120MB limit for demo

@router.get("/health")
def health_check():
    ffmpeg_ok = False
    try:
        get_ffmpeg_path()
        ffmpeg_ok = True
    except Exception:
        ffmpeg_ok = False

    return {
        "status": "healthy",
        "groq_configured": bool(GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here"),
        "gemini_configured": bool(GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here"),
        "ffmpeg_available": ffmpeg_ok,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_video(file: UploadFile = File(...)):
    # 1. Validate File
    if not file.filename:
        raise HTTPException(status_code=400, detail="No video file provided.")
        
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{ext}'. Please upload an MP4, MOV, or WEBM video."
        )

    # 2. Check API keys early
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        raise HTTPException(
            status_code=400,
            detail="GROQ_API_KEY is not configured in .env. Please configure your API key to enable transcription."
        )
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise HTTPException(
            status_code=400,
            detail="GEMINI_API_KEY is not configured in .env. Please configure your API key to enable multimodal analysis."
        )

    # 3. Create unique analysis ID and save video
    analysis_id = str(uuid.uuid4())
    video_path = UPLOADS_DIR / f"{analysis_id}{ext}"
    
    try:
        content = await file.read()
        if len(content) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=400, detail="Video file exceeds 120MB limit.")
        with open(video_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded video: {str(e)}")

    # 4. Process Video: Duration & Audio extraction
    try:
        duration = get_video_duration(video_path)
    except Exception as e:
        duration = 30.0

    audio_path = AUDIO_DIR / f"{analysis_id}.wav"
    try:
        extract_audio(video_path, audio_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio extraction failed: {str(e)}")

    # 5. Transcribe Audio via Groq Whisper
    try:
        transcript_data = transcribe_audio(audio_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription service error: {str(e)}")

    # 6. Extract Keyframes via FFmpeg
    analysis_frames_dir = FRAMES_DIR / analysis_id
    try:
        frame_paths = extract_representative_frames(video_path, analysis_frames_dir, num_frames=7)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Frame extraction failed: {str(e)}")

    # 7. Gemini Multimodal Analysis
    try:
        content_analysis = analyze_video_content(
            frame_paths=frame_paths,
            transcript=transcript_data.get("text", ""),
            duration=duration
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content intelligence analysis failed: {str(e)}")

    # 8. Gemini Original Concept & Script Generation
    try:
        generated_content = generate_original_concept(content_analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Original concept generation failed: {str(e)}")

    # 9. Gemini Brand QA Critic
    try:
        qa_result = evaluate_brand_qa(content_analysis, generated_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brand QA evaluation failed: {str(e)}")

    # Determine production readiness
    is_ready = qa_result.status == "PASS" and qa_result.overall_score >= 80
    readiness = "Ready for production" if is_ready else "Needs review"

    # Construct frame and video public relative URLs
    video_url = f"/data/uploads/{analysis_id}{ext}"
    frame_urls = [f"/data/frames/{analysis_id}/{fp.name}" for fp in frame_paths]

    result = AnalysisResult(
        analysis_id=analysis_id,
        filename=file.filename,
        created_at=datetime.utcnow().isoformat(),
        video_url=video_url,
        video_duration=round(duration, 1),
        frame_urls=frame_urls,
        transcript=transcript_data,
        analysis=content_analysis,
        generated_content=generated_content,
        qa_result=qa_result,
        production_readiness=readiness
    )

    # 10. Persist complete result to local JSON
    result_path = RESULTS_DIR / f"{analysis_id}.json"
    with open(result_path, "w", encoding="utf-8") as rf:
        rf.write(result.model_dump_json(indent=2))

    return result

@router.get("/analysis/{analysis_id}", response_model=AnalysisResult)
def get_analysis(analysis_id: str):
    result_path = RESULTS_DIR / f"{analysis_id}.json"
    if not result_path.exists():
        raise HTTPException(status_code=404, detail=f"Analysis '{analysis_id}' not found.")
    
    try:
        with open(result_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return AnalysisResult.model_validate(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading analysis data: {str(e)}")

@router.get("/analyses")
def list_analyses():
    """List previous analyses sorted by timestamp descending."""
    results = []
    for file_path in RESULTS_DIR.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            results.append({
                "analysis_id": data.get("analysis_id"),
                "filename": data.get("filename"),
                "created_at": data.get("created_at"),
                "topic": data.get("analysis", {}).get("topic", "Untitled"),
                "generated_title": data.get("generated_content", {}).get("title", ""),
                "qa_score": data.get("qa_result", {}).get("overall_score", 0),
                "qa_status": data.get("qa_result", {}).get("status", "PASS"),
                "production_readiness": data.get("production_readiness", "Needs review")
            })
        except Exception:
            continue

    # Sort newest first
    results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return results
