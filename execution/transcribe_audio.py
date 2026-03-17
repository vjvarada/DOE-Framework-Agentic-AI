#!/usr/bin/env python3
"""
Transcribe audio/video files using OpenAI Whisper (local or API).

Supports: .mp3, .wav, .m4a, .ogg, .flac, .mp4, .webm, .mkv, .avi, .mov

Usage:
    # Local Whisper (free, requires torch + whisper installed)
    python transcribe_audio.py --input recording.mp4 --method local --model medium

    # OpenAI Whisper API (fast, ~$0.006/min, requires OPENAI_API_KEY)
    python transcribe_audio.py --input recording.mp4 --method api

    # Specify output path
    python transcribe_audio.py --input recording.mp4 --method local --output .tmp/transcript.txt

    # Force language
    python transcribe_audio.py --input recording.mp4 --method local --language en
"""

import os
import sys
import json
import argparse
import tempfile
import subprocess
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

# Supported file extensions
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".wma"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mkv", ".avi", ".mov", ".wmv"}
ALL_EXTENSIONS = AUDIO_EXTENSIONS | VIDEO_EXTENSIONS

# Whisper API max file size (25MB)
API_MAX_BYTES = 25 * 1024 * 1024

# Tmp directory
TMP_DIR = Path(".tmp")


def ensure_tmp_dir():
    """Create .tmp directory if it doesn't exist."""
    TMP_DIR.mkdir(exist_ok=True)


def extract_audio_from_video(video_path: str, output_path: str = None) -> str:
    """
    Extract audio track from a video file using ffmpeg.
    Returns path to the extracted audio file.
    """
    if output_path is None:
        ensure_tmp_dir()
        output_path = str(TMP_DIR / "extracted_audio.mp3")

    print(f"Extracting audio from video: {video_path}")
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vn",              # no video
        "-acodec", "libmp3lame",
        "-ar", "16000",     # 16kHz sample rate (Whisper optimal)
        "-ac", "1",         # mono
        "-q:a", "4",        # decent quality, small file
        "-y",               # overwrite
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            print(f"ffmpeg error: {result.stderr}")
            raise RuntimeError(f"ffmpeg failed: {result.stderr[-500:]}")
    except FileNotFoundError:
        print("ERROR: ffmpeg not found. Install it:")
        print("  Windows: winget install ffmpeg  OR  choco install ffmpeg")
        print("  Mac: brew install ffmpeg")
        print("  Linux: sudo apt install ffmpeg")
        sys.exit(1)
    
    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  Extracted audio: {output_path} ({file_size:.1f} MB)")
    return output_path


def split_audio_for_api(audio_path: str, max_size_bytes: int = API_MAX_BYTES) -> list:
    """
    Split audio file into chunks under 25MB for Whisper API.
    Returns list of chunk file paths.
    """
    file_size = os.path.getsize(audio_path)
    if file_size <= max_size_bytes:
        return [audio_path]
    
    print(f"File is {file_size / (1024*1024):.1f} MB — splitting into chunks...")
    ensure_tmp_dir()
    
    # Get duration using ffprobe
    cmd = [
        "ffprobe", "-v", "quiet", "-show_entries",
        "format=duration", "-of", "csv=p=0", audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    total_duration = float(result.stdout.strip())
    
    # Calculate chunk duration to stay under 25MB
    # Aim for ~20MB chunks to be safe
    target_chunk_size = 20 * 1024 * 1024
    num_chunks = max(2, int(file_size / target_chunk_size) + 1)
    chunk_duration = total_duration / num_chunks
    
    chunks = []
    for i in range(num_chunks):
        start = i * chunk_duration
        chunk_path = str(TMP_DIR / f"chunk_{i:03d}.mp3")
        
        cmd = [
            "ffmpeg", "-i", audio_path,
            "-ss", str(start),
            "-t", str(chunk_duration),
            "-acodec", "libmp3lame",
            "-ar", "16000",
            "-ac", "1",
            "-q:a", "4",
            "-y",
            chunk_path
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        
        if os.path.exists(chunk_path) and os.path.getsize(chunk_path) > 0:
            chunks.append(chunk_path)
    
    print(f"  Split into {len(chunks)} chunks")
    return chunks


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format."""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def transcribe_local(audio_path: str, model_name: str = "medium", language: str = None) -> dict:
    """
    Transcribe using local OpenAI Whisper model.
    Free, runs on CPU/GPU. Requires: pip install openai-whisper torch
    
    Returns dict with 'text' (full transcript) and 'segments' (timestamped).
    """
    try:
        import whisper
    except ImportError:
        print("ERROR: openai-whisper not installed.")
        print("  Install: pip install openai-whisper torch")
        print("  Note: This is different from the 'openai' package.")
        sys.exit(1)
    
    print(f"Loading Whisper model '{model_name}'...")
    print("  (First run downloads the model — may take a few minutes)")
    
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"  Using device: {device}")
    
    model = whisper.load_model(model_name, device=device)
    
    print(f"Transcribing: {audio_path}")
    print("  This may take a while depending on file length and model size...")
    
    options = {}
    if language:
        options["language"] = language
    
    result = model.transcribe(audio_path, **options)
    
    # Format output
    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "start_formatted": format_timestamp(seg["start"]),
            "end_formatted": format_timestamp(seg["end"]),
            "text": seg["text"].strip()
        })
    
    output = {
        "method": "local_whisper",
        "model": model_name,
        "language": result.get("language", language or "auto"),
        "text": result["text"].strip(),
        "segments": segments,
        "segment_count": len(segments)
    }
    
    duration_sec = segments[-1]["end"] if segments else 0
    print(f"\n  Transcription complete!")
    print(f"  Duration: {format_timestamp(duration_sec)}")
    print(f"  Segments: {len(segments)}")
    print(f"  Language: {output['language']}")
    
    return output


def transcribe_api(audio_path: str, language: str = None) -> dict:
    """
    Transcribe using OpenAI Whisper API.
    Fast, ~$0.006/min. Requires OPENAI_API_KEY.
    Auto-splits files > 25MB.
    
    Returns dict with 'text' (full transcript) and 'segments' (timestamped).
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set in .env")
        print("  Get one at: https://platform.openai.com/api-keys")
        sys.exit(1)
    
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    
    # Split if needed
    chunks = split_audio_for_api(audio_path)
    
    all_text = []
    all_segments = []
    time_offset = 0.0
    
    for i, chunk_path in enumerate(chunks):
        if len(chunks) > 1:
            print(f"  Transcribing chunk {i+1}/{len(chunks)}: {chunk_path}")
        else:
            print(f"Transcribing via API: {chunk_path}")
        
        with open(chunk_path, "rb") as f:
            kwargs = {
                "model": "whisper-1",
                "file": f,
                "response_format": "verbose_json",
                "timestamp_granularities": ["segment"]
            }
            if language:
                kwargs["language"] = language
            
            response = client.audio.transcriptions.create(**kwargs)
        
        all_text.append(response.text)
        
        for seg in getattr(response, "segments", []) or []:
            all_segments.append({
                "start": seg.get("start", 0) + time_offset,
                "end": seg.get("end", 0) + time_offset,
                "start_formatted": format_timestamp(seg.get("start", 0) + time_offset),
                "end_formatted": format_timestamp(seg.get("end", 0) + time_offset),
                "text": seg.get("text", "").strip()
            })
        
        # Update time offset for next chunk
        if all_segments:
            time_offset = all_segments[-1]["end"]
    
    full_text = " ".join(all_text)
    
    output = {
        "method": "whisper_api",
        "model": "whisper-1",
        "language": language or "auto",
        "text": full_text,
        "segments": all_segments,
        "segment_count": len(all_segments)
    }
    
    duration_sec = all_segments[-1]["end"] if all_segments else 0
    cost_estimate = (duration_sec / 60) * 0.006
    
    print(f"\n  Transcription complete!")
    print(f"  Duration: {format_timestamp(duration_sec)}")
    print(f"  Segments: {len(all_segments)}")
    print(f"  Estimated cost: ${cost_estimate:.3f}")
    
    # Clean up chunks
    if len(chunks) > 1:
        for chunk in chunks:
            if "chunk_" in str(chunk):
                try:
                    os.remove(chunk)
                except OSError:
                    pass
    
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio/video files using OpenAI Whisper (local or API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Free local transcription (medium model, good accuracy)
  python transcribe_audio.py --input meeting.mp4 --method local --model medium

  # Fast API transcription (~$0.006/min)
  python transcribe_audio.py --input meeting.mp4 --method api

  # Quick local transcription (lower accuracy, fast)
  python transcribe_audio.py --input meeting.mp4 --method local --model base

  # Force English language
  python transcribe_audio.py --input meeting.mp4 --method local --language en
        """
    )
    
    parser.add_argument("--input", "-i", required=True, help="Path to audio/video file")
    parser.add_argument("--method", "-m", choices=["local", "api"], default="local",
                        help="Transcription method: 'local' (free) or 'api' (paid, fast)")
    parser.add_argument("--model", default="medium",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size (local only). Default: medium")
    parser.add_argument("--language", "-l", default=None,
                        help="Language code (e.g., 'en', 'es', 'fr'). Auto-detected if not set")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file path. Default: .tmp/transcript.txt + .tmp/transcript.json")
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: File not found: {args.input}")
        sys.exit(1)
    
    ext = input_path.suffix.lower()
    if ext not in ALL_EXTENSIONS:
        print(f"ERROR: Unsupported file type: {ext}")
        print(f"  Supported: {', '.join(sorted(ALL_EXTENSIONS))}")
        sys.exit(1)
    
    ensure_tmp_dir()
    
    # Extract audio from video if needed
    audio_path = str(input_path)
    if ext in VIDEO_EXTENSIONS:
        audio_path = extract_audio_from_video(str(input_path))
    
    # Transcribe
    if args.method == "local":
        result = transcribe_local(audio_path, model_name=args.model, language=args.language)
    else:
        result = transcribe_api(audio_path, language=args.language)
    
    # Save outputs
    if args.output:
        txt_path = args.output
        json_path = str(Path(args.output).with_suffix(".json"))
    else:
        txt_path = str(TMP_DIR / "transcript.txt")
        json_path = str(TMP_DIR / "transcript.json")
    
    # Save plain text transcript
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"\n  Plain text saved: {txt_path}")
    
    # Save full JSON with segments
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"  JSON (with timestamps) saved: {json_path}")
    
    # Save timestamped text version (easier to read)
    ts_path = str(Path(txt_path).with_suffix(".timestamped.txt"))
    with open(ts_path, "w", encoding="utf-8") as f:
        for seg in result.get("segments", []):
            f.write(f"[{seg['start_formatted']} - {seg['end_formatted']}] {seg['text']}\n")
    print(f"  Timestamped text saved: {ts_path}")
    
    return result


if __name__ == "__main__":
    main()
