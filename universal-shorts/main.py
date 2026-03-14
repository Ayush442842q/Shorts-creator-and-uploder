"""
main.py — ECE YouTube Shorts Bot
Run: python3 main.py
"""

import os, sys, traceback
from config import TOPICS_FILE, PROGRESS_FILE, OUTPUT_DIR

from modules.script_gen     import generate_script, generate_metadata
from modules.tts            import generate_voiceover
from modules.video_builder  import build_video
from modules.telegram_bot   import send_script_to_bot_a, send_video_to_bot_b, send_error_notification
from modules.youtube_upload import upload_short


def load_topics():
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


def get_next_index():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            try:    return int(f.read().strip())
            except: return 0
    return 0


def save_progress(index):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(index))


def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    from config import CHANNEL_NAME
    print("\n" + "="*60)
    print(f"   Universal Shorts Bot — {CHANNEL_NAME}")
    print("="*60)

    topics = load_topics()
    index  = get_next_index()
    if index >= len(topics):
        index = 0
    topic = topics[index]
    print(f"📚 Topic [{index+1}/{len(topics)}]: {topic}")

    try:
        # Step 1 — Script + metadata
        print("\n📝 Step 1/6: Generating script...")
        script   = generate_script(topic)
        metadata = generate_metadata(topic, script)
        print(f"Script preview: {script[:100]}...")
        print(f"Title: {metadata.get('title')}")

        script_data = {
            "topic":       topic,
            "script":      script,
            "title":       metadata.get("title", f"{topic} #Shorts"),
            "description": metadata.get("description", ""),
            "tags":        metadata.get("tags", []),
        }

        # Step 2 — Telegram Bot A
        print("\n📨 Step 2/6: Sending script to Telegram Bot A...")
        send_script_to_bot_a(script_data)

        # Step 3 — Voiceover
        print("\n🎙️ Step 3/6: Generating voiceover...")
        audio_path = generate_voiceover(script, index)

        # Step 4 — Build video
        print("\n🎬 Step 4/6: Building video...")
        video_path = build_video(topic, script, audio_path, index)

        # Step 5 — Telegram Bot B
        print("\n📤 Step 5/6: Sending video to Telegram Bot B...")
        send_video_to_bot_b(video_path, script_data)

        # Step 6 — YouTube upload
        print("\n🚀 Step 6/6: Uploading to YouTube...")
        url = upload_short(video_path, metadata, topic)

        save_progress(index + 1)

        print("\n" + "="*60)
        print("  ✅ PIPELINE COMPLETE!")
        print(f"  Topic  : {topic}")
        print(f"  YouTube: {url}")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        traceback.print_exc()
        try: send_error_notification(f"Topic: {topic}\nError: {e}")
        except: pass
        sys.exit(1)


if __name__ == "__main__":
    run()
