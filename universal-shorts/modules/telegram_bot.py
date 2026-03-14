"""
telegram_bot.py — Sends script and video to Telegram bots (plain text, no markdown)
Universal version: uses CHANNEL_NAME from config instead of hardcoded ECE strings.
"""

import requests, os
from config import (TELEGRAM_BOT_A_TOKEN, TELEGRAM_BOT_A_CHAT_ID,
                    TELEGRAM_BOT_B_TOKEN, TELEGRAM_BOT_B_CHAT_ID,
                    CHANNEL_NAME)


def send_script_to_bot_a(script_data: dict) -> bool:
    print("[TelegramA] Sending script...")
    message = (
        f"{CHANNEL_NAME.upper()} — NEW SHORT SCRIPT\n"
        f"{'='*30}\n"
        f"Topic: {script_data.get('topic','')}\n\n"
        f"Title: {script_data.get('title','')}\n\n"
        f"Script:\n{script_data.get('script','')}\n\n"
        f"Description:\n{script_data.get('description','')}\n\n"
        f"Tags: {', '.join(script_data.get('tags',[])[:10])}\n"
        f"{'='*30}\n"
        f"Auto-proceeding to video generation..."
    )
    return _send_message(TELEGRAM_BOT_A_TOKEN, TELEGRAM_BOT_A_CHAT_ID, message)


def send_video_to_bot_b(video_path: str, script_data: dict) -> bool:
    print("[TelegramB] Sending video...")
    caption = (
        f"{CHANNEL_NAME.upper()} — SHORT READY\n"
        f"{'='*30}\n"
        f"Topic: {script_data.get('topic','')}\n"
        f"Title: {script_data.get('title','')}\n"
        f"{'='*30}\n"
        f"Auto-uploading to YouTube..."
    )
    return _send_video(TELEGRAM_BOT_B_TOKEN, TELEGRAM_BOT_B_CHAT_ID, video_path, caption)


def send_error_notification(error_msg: str) -> bool:
    message = f"{CHANNEL_NAME.upper()} — Bot ERROR\n{'='*30}\n{error_msg}"
    return _send_message(TELEGRAM_BOT_A_TOKEN, TELEGRAM_BOT_A_CHAT_ID, message)


def _send_message(token: str, chat_id: str, text: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=30)
        data = r.json()
        if data.get("ok"):
            print("  [Telegram] Message sent successfully")
            return True
        print(f"  [Telegram] Failed: {data.get('description','Unknown')}")
        return False
    except Exception as e:
        print(f"  [Telegram] Error: {e}")
        return False


def _send_video(token: str, chat_id: str, video_path: str, caption: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendVideo"
    try:
        size_mb = os.path.getsize(video_path) / (1024*1024)
        print(f"  [Telegram] Video size: {size_mb:.1f} MB")
        if size_mb > 50:
            return _send_document(token, chat_id, video_path, caption)
        with open(video_path, "rb") as f:
            r = requests.post(url,
                data={"chat_id": chat_id, "caption": caption, "supports_streaming": True},
                files={"video": f}, timeout=120)
            result = r.json()
            if result.get("ok"):
                print("  [Telegram] Video sent successfully")
                return True
            print(f"  [Telegram] Failed: {result.get('description')}")
            return False
    except Exception as e:
        print(f"  [Telegram] Error: {e}")
        return False


def _send_document(token: str, chat_id: str, file_path: str, caption: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    try:
        with open(file_path, "rb") as f:
            r = requests.post(url,
                data={"chat_id": chat_id, "caption": caption},
                files={"document": f}, timeout=120)
            return r.json().get("ok", False)
    except Exception as e:
        print(f"  [Telegram] Document error: {e}")
        return False
