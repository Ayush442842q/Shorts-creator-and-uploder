"""
tts.py — Uses a user-provided audio file instead of generating TTS.
Place your audio file at: audio/voiceover.mp3 (or .wav)
"""

import os, subprocess
from config import OUTPUT_DIR

# ── Put your audio file here ─────────────────────────────────
AUDIO_INPUT_DIR  = "audio"
AUDIO_FILENAME   = "voiceover"   # without extension, checks mp3/wav/m4a/ogg
SUPPORTED_EXTS   = [".mp3", ".wav", ".m4a", ".ogg", ".aac"]


def generate_voiceover(script: str, topic_index: int = 0) -> str:
    """
    Finds the user-provided audio file and returns its path.
    Converts to WAV if needed for FFmpeg compatibility.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Find the audio file
    audio_path = _find_audio()
    if not audio_path:
        raise FileNotFoundError(
            f"\n\n❌ No audio file found!\n"
            f"Please create an '{AUDIO_INPUT_DIR}/' folder in your project root\n"
            f"and place your audio file there as 'voiceover.mp3' (or .wav/.m4a)\n"
            f"Example: ece-shorts-v2/audio/voiceover.mp3\n"
        )

    print(f"  [TTS] Using audio file: {audio_path}")

    # Convert to wav if not already wav
    out_path = os.path.join(OUTPUT_DIR, f"voiceover_{topic_index}.wav")
    if audio_path.endswith(".wav"):
        import shutil
        shutil.copy(audio_path, out_path)
    else:
        _convert_to_wav(audio_path, out_path)

    duration = _get_duration(out_path)
    print(f"  [TTS] Audio duration: {duration:.1f}s")
    return out_path


def _find_audio() -> str:
    """Search for audio file in audio/ folder"""
    for ext in SUPPORTED_EXTS:
        path = os.path.join(AUDIO_INPUT_DIR, AUDIO_FILENAME + ext)
        if os.path.exists(path):
            return path
    # Also check project root
    for ext in SUPPORTED_EXTS:
        path = AUDIO_FILENAME + ext
        if os.path.exists(path):
            return path
    return None


def _convert_to_wav(input_path: str, output_path: str):
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", input_path, output_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Audio conversion failed: {result.stderr[-300:]}")


def _get_duration(path: str) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True
    )
    try:    return float(r.stdout.strip())
    except: return 0.0
