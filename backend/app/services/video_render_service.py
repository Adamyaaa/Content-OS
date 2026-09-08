import os
import re
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont

from backend.app.services.video_service import get_ffmpeg_path

def get_media_duration(media_path: Path) -> float:
    """Returns exact duration of audio or video in seconds via FFmpeg."""
    ffmpeg_bin = get_ffmpeg_path()
    cmd = [ffmpeg_bin, "-i", str(media_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", res.stderr)
    if match:
        hours = float(match.group(1))
        minutes = float(match.group(2))
        seconds = float(match.group(3))
        return hours * 3600 + minutes * 60 + seconds
    return 0.0

def parse_scene_duration(timestamp_str: str, default_duration: float = 6.0) -> float:
    """Parse string like '0-3s', '3-10s', or '10-18s' to seconds duration."""
    match = re.search(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*s?", timestamp_str.lower())
    if match:
        start = float(match.group(1))
        end = float(match.group(2))
        dur = end - start
        if dur > 1.0:
            return dur
    return default_duration

def fetch_scene_image(prompt: str, output_path: Path, local_frame_fallback: Optional[Path] = None) -> Path:
    """
    Acquires high-resolution vertical 9:16 imagery:
    1. Attempts online photorealistic AI generation (Pollinations FLUX 0-OPEX).
    2. If online fetch is slow/fails, uses high-definition extracted video frame if available.
    3. Falls back to generating a beautiful procedural organic agriculture background.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean_prompt = re.sub(r"[^\w\s,.-]", " ", prompt).strip()[:180]
    enhanced_prompt = (
        f"8k macro vertical reel photo of {clean_prompt}, "
        f"organic agriculture, fertile soil microbiology, golden hour lighting, 9:16 vertical ratio, photorealistic"
    )
    
    encoded = urllib.parse.quote(enhanced_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1920&nologo=true&model=flux"
    
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp, open(output_path, "wb") as f:
            f.write(resp.read())
        with Image.open(output_path) as img:
            img.verify()
        return output_path
    except Exception as e:
        print(f"Warning: FLUX image fetch unavailable ({e}). Employing high-res local visual asset...")

    # Fallback 1: Use extracted local video frame if available
    if local_frame_fallback and local_frame_fallback.exists():
        try:
            with Image.open(local_frame_fallback) as img:
                w, h = img.size
                target_ratio = 1080 / 1920
                current_ratio = w / h
                if current_ratio > target_ratio:
                    new_w = int(h * target_ratio)
                    offset = (w - new_w) // 2
                    cropped = img.crop((offset, 0, offset + new_w, h))
                else:
                    new_h = int(w / target_ratio)
                    offset = (h - new_h) // 2
                    cropped = img.crop((0, offset, w, offset + new_h))
                resized = cropped.resize((1080, 1920), Image.Resampling.LANCZOS)
                resized.save(output_path, "JPEG", quality=92)
                return output_path
        except Exception as frame_err:
            print(f"Notice: local frame resize error: {frame_err}")

    # Fallback 2: High-aesthetic dark organic gardening backdrop
    img = Image.new("RGB", (1080, 1920), color=(18, 28, 20))
    draw = ImageDraw.Draw(img)
    for y in range(0, 1920, 4):
        g = min(255, 32 + int((y / 1920) * 35))
        draw.line([(0, y), (1080, y)], fill=(14, g, 22))
    draw.rectangle([60, 60, 1020, 1860], outline=(46, 125, 90), width=6)
    img.save(output_path, "JPEG", quality=90)
    return output_path

def render_scene_clip(
    image_path: Path,
    duration: float,
    on_screen_text: str,
    output_clip_path: Path,
    scene_number: int = 1
) -> Path:
    """
    Renders a dynamic 1080x1920 9:16 vertical video clip with:
    - High-bitrate H.264 encode (2.8 Mbps)
    - Ken Burns motion zoom/pan (alternating zoom-in & zoom-out)
    - Modern TikTok/Instagram Reels bold headline card overlay
    """
    ffmpeg_bin = get_ffmpeg_path()
    output_clip_path.parent.mkdir(parents=True, exist_ok=True)
    
    clean_text = on_screen_text.replace("'", "").replace(":", "-").replace('"', "").strip()
    if not clean_text:
        clean_text = "ORGANIC REELS"
    clean_text = clean_text.upper()
    
    frames = max(int(duration * 25), 25)
    
    if scene_number % 2 == 1:
        zoom_expr = "min(zoom+0.0010,1.14)"
    else:
        zoom_expr = "max(1.14-0.0010*on,1.01)"
        
    vf_filter = (
        f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"zoompan=z='{zoom_expr}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920,"
        f"drawtext=text='{clean_text}':fontcolor=white:fontsize=52:x=(w-text_w)/2:y=h*0.74:"
        f"box=1:boxcolor=black@0.75:boxborderw=20"
    )
    
    cmd = [
        ffmpeg_bin, "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-vf", vf_filter,
        "-t", f"{duration:.2f}",
        "-r", "25",
        "-c:v", "libx264",
        "-preset", "fast",
        "-b:v", "2800k",
        "-pix_fmt", "yuv420p",
        str(output_clip_path)
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        cmd_fallback = [
            ffmpeg_bin, "-y",
            "-loop", "1",
            "-i", str(image_path),
            "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,drawtext=text='{clean_text}':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=h*0.74:box=1:boxcolor=black@0.75:boxborderw=18",
            "-t", f"{duration:.2f}",
            "-r", "25",
            "-c:v", "libx264",
            "-preset", "fast",
            "-b:v", "2500k",
            "-pix_fmt", "yuv420p",
            str(output_clip_path)
        ]
        subprocess.run(cmd_fallback, check=True)
        
    return output_clip_path

def render_complete_reel(
    analysis_id: str,
    scene_breakdown: List[Dict[str, Any]],
    voiceover_audio_path: Path,
    output_video_path: Path,
    source_frames_dir: Optional[Path] = None
) -> Path:
    """
    Renders an end-to-end 9:16 vertical short-form video reel:
    1. Accurately determines voiceover duration to match visual pacing
    2. Downloads or assembles crisp 1080x1920 scene visuals
    3. Renders cinematic Ken Burns video clips with bold subtitles
    4. Stitches scenes and mixes crystal-clear neural voiceover into MP4
    """
    ffmpeg_bin = get_ffmpeg_path()
    output_video_path.parent.mkdir(parents=True, exist_ok=True)
    
    temp_dir = output_video_path.parent / f"render_tmp_{analysis_id}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    num_scenes = max(len(scene_breakdown), 1)
    
    audio_duration = 0.0
    if voiceover_audio_path.exists():
        audio_duration = get_media_duration(voiceover_audio_path)
        
    if audio_duration > 5.0:
        duration_per_scene = audio_duration / num_scenes
    else:
        duration_per_scene = 5.5

    extracted_frames = []
    if source_frames_dir and source_frames_dir.exists():
        extracted_frames = sorted(list(source_frames_dir.glob("*.jpg")))
    elif (output_video_path.parent.parent / "frames" / analysis_id).exists():
        extracted_frames = sorted(list((output_video_path.parent.parent / "frames" / analysis_id).glob("*.jpg")))
        
    clips: List[Path] = []
    
    for idx, scene in enumerate(scene_breakdown, start=1):
        visual_prompt = scene.get("visual", "lush organic agriculture fertile garden soil")
        on_screen_text = scene.get("on_screen_text", f"SCENE {idx}")
        
        local_fallback = None
        if extracted_frames:
            local_fallback = extracted_frames[(idx - 1) % len(extracted_frames)]
            
        img_path = temp_dir / f"scene_{idx:02d}.jpg"
        fetch_scene_image(visual_prompt, img_path, local_frame_fallback=local_fallback)
        
        clip_path = temp_dir / f"clip_{idx:02d}.mp4"
        render_scene_clip(img_path, duration_per_scene, on_screen_text, clip_path, scene_number=idx)
        clips.append(clip_path)
        
    # Write concat list
    concat_list_file = temp_dir / "concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c.resolve().as_posix()}'\n")
            
    stitched_video_no_audio = temp_dir / "stitched.mp4"
    concat_cmd = [
        ffmpeg_bin, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(stitched_video_no_audio)
    ]
    subprocess.run(concat_cmd, check=True)
    
    # Mux with voiceover audio
    if voiceover_audio_path.exists() and audio_duration > 0.5:
        mux_cmd = [
            ffmpeg_bin, "-y",
            "-i", str(stitched_video_no_audio),
            "-i", str(voiceover_audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_video_path)
        ]
        subprocess.run(mux_cmd, check=True)
    else:
        import shutil
        shutil.copyfile(stitched_video_no_audio, output_video_path)
        
    # Cleanup temp clips
    try:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass
        
    return output_video_path
