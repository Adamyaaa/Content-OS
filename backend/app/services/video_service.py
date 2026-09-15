import os
import shutil
import subprocess
import re
from pathlib import Path
from typing import List, Tuple
import imageio_ffmpeg

def get_ffmpeg_path() -> str:
    """Resolve FFmpeg executable from system PATH or imageio_ffmpeg binary."""
    # 1. Check custom env
    custom_path = os.getenv("FFMPEG_PATH")
    if custom_path and os.path.exists(custom_path):
        return custom_path

    # 2. Check system PATH
    sys_ffmpeg = shutil.which("ffmpeg")
    if sys_ffmpeg:
        return sys_ffmpeg

    # 3. Fallback to imageio_ffmpeg bundled binary
    try:
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as e:
        raise RuntimeError(f"FFmpeg binary could not be found: {e}")

def get_video_duration(video_path: Path) -> float:
    """Probe video duration in seconds using FFmpeg."""
    ffmpeg_bin = get_ffmpeg_path()
    cmd = [ffmpeg_bin, "-i", str(video_path)]
    
    # FFmpeg writes stream info to stderr
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
    stderr = result.stderr
    
    # Match Duration: 00:00:30.50
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", stderr)
    if match:
        hours = float(match.group(1))
        minutes = float(match.group(2))
        seconds = float(match.group(3))
        duration = hours * 3600 + minutes * 60 + seconds
        if duration > 0:
            return duration
            
    # Default fallback if duration could not be parsed
    return 30.0

def extract_audio(video_path: Path, output_audio_path: Path) -> Path:
    """
    Extract audio track to 16kHz mono WAV or MP3 optimized for Groq Whisper.
    """
    ffmpeg_bin = get_ffmpeg_path()
    output_audio_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing audio if present
    if output_audio_path.exists():
        output_audio_path.unlink()

    # -vn: disable video, -ac 1: mono, -ar 16000: 16kHz sampling rate
    cmd = [
        ffmpeg_bin,
        "-y",
        "-i", str(video_path),
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-c:a", "libmp3lame" if output_audio_path.suffix.lower() == ".mp3" else "pcm_s16le",
        str(output_audio_path)
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
    if result.returncode != 0:
        raise RuntimeError(f"Audio extraction failed: {result.stderr}")
        
    return output_audio_path

def is_duplicate_frame(img1_path: Path, img2_path: Path, threshold: float = 12.0) -> bool:
    """Helper to determine if two images are visually duplicate."""
    try:
        from PIL import Image
        with Image.open(img1_path) as i1, Image.open(img2_path) as i2:
            i1 = i1.resize((32, 32)).convert("L")
            i2 = i2.resize((32, 32)).convert("L")
            
            d1 = i1.getdata()
            d2 = i2.getdata()
            diff_sum = sum(abs(p1 - p2) for p1, p2 in zip(d1, d2))
            
            avg_diff = diff_sum / 1024.0
            return avg_diff < threshold
    except Exception:
        return False

def extract_representative_frames(video_path: Path, output_dir: Path, num_frames: int = 7) -> List[Path]:
    """
    Extract representative frames distributed throughout the video.
    Removes duplicate/similar keyframes.
    """
    ffmpeg_bin = get_ffmpeg_path()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    duration = get_video_duration(video_path)
    
    # We extract more frames initially to filter out duplicates
    candidate_count = max(20, num_frames * 3)
    saved_candidates: List[Path] = []
    
    for idx in range(1, candidate_count + 1):
        frac = idx / (candidate_count + 1)
        timestamp = max(0.1, duration * frac)
        frame_filename = output_dir / f"cand_{idx:02d}.jpg"
        
        # -ss before -i for fast seek
        cmd = [
            ffmpeg_bin,
            "-y",
            "-ss", f"{timestamp:.2f}",
            "-i", str(video_path),
            "-frames:v", "1",
            "-q:v", "2",
            "-vf", "scale='min(720,iw)':-2",
            str(frame_filename)
        ]
        
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
        if res.returncode == 0 and frame_filename.exists() and frame_filename.stat().st_size > 0:
            saved_candidates.append(frame_filename)
            
    # Filter duplicates
    unique_frames: List[Path] = []
    
    for cand_path in saved_candidates:
        if not unique_frames:
            unique_frames.append(cand_path)
            continue
            
        # Compare with the most recently accepted unique frame
        if not is_duplicate_frame(unique_frames[-1], cand_path):
            unique_frames.append(cand_path)
            
        if len(unique_frames) == num_frames:
            break
            
    # Cleanup unused candidates
    for cand_path in saved_candidates:
        if cand_path not in unique_frames:
            try:
                cand_path.unlink()
            except Exception:
                pass
                
    # Rename unique frames sequentially
    final_frames: List[Path] = []
    for idx, u_path in enumerate(unique_frames, start=1):
        final_path = output_dir / f"frame_{idx:02d}.jpg"
        if u_path != final_path:
            u_path.rename(final_path)
        final_frames.append(final_path)
            
    # If keyframe seeking produced no frames, capture at least the initial frame
    if not final_frames:
        frame_fallback = output_dir / "frame_01.jpg"
        cmd = [
            ffmpeg_bin,
            "-y",
            "-i", str(video_path),
            "-frames:v", "1",
            "-q:v", "2",
            str(frame_fallback)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
        if frame_fallback.exists():
            final_frames.append(frame_fallback)

    return final_frames
