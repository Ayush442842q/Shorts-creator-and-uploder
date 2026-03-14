"""
youtube_upload.py — Uploads video to YouTube as a Short using Data API v3
Universal version: description footer built from CHANNEL_DESCRIPTION.
"""

import os, pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import YOUTUBE_CLIENT_SECRETS, YOUTUBE_SCOPES, CHANNEL_NAME, CHANNEL_DESCRIPTION, CHANNEL_EMOJI

TOKEN_FILE = "youtube_token.pickle"


def upload_short(video_path: str, metadata: dict, topic: str) -> str:
    """
    Uploads video to YouTube. Returns the video URL.
    """
    print("[YouTube] Authenticating...")
    youtube = _get_client()

    title       = metadata.get("title", f"{topic} #Shorts")
    description = metadata.get("description", f"Learn about {topic}! #Shorts")
    tags        = metadata.get("tags", ["Shorts", topic])

    if "#Shorts" not in title:
        title += " #Shorts"
    if "#Shorts" not in description:
        description += "\n\n#Shorts"

    # Universal footer built from config
    description += (
        f"\n\n━━━━━━━━━━━━━━━━━━━━\n"
        f"{CHANNEL_EMOJI} {CHANNEL_NAME} — {CHANNEL_DESCRIPTION}\n"
        f"Subscribe for daily shorts.\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )

    print(f"[YouTube] Uploading: {title}")

    body = {
        "snippet": {
            "title":           title[:100],
            "description":     description[:5000],
            "tags":            tags[:500],
            "categoryId":      "22",       # People & Blogs (neutral default)
            "defaultLanguage": "en",
        },
        "status": {
            "privacyStatus":            "public",
            "selfDeclaredMadeForKids":  False,
            "madeForKids":              False,
        }
    }

    media   = MediaFileUpload(video_path, mimetype="video/mp4",
                              resumable=True, chunksize=1024*1024)
    request = youtube.videos().insert(part="snippet,status",
                                      body=body, media_body=media)

    video_id = _execute_upload(request)
    url = f"https://www.youtube.com/shorts/{video_id}"
    print(f"[YouTube] Uploaded: {url}")
    return url


def _execute_upload(request) -> str:
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  [YouTube] Progress: {int(status.progress()*100)}%")
    return response["id"]


def _get_client():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("  [YouTube] Refreshing token...")
            creds.refresh(Request())
        else:
            print("  [YouTube] Opening browser for first-time auth...")
            flow  = InstalledAppFlow.from_client_secrets_file(
                YOUTUBE_CLIENT_SECRETS, YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
        print("  [YouTube] Token saved for future runs")

    return build("youtube", "v3", credentials=creds)
