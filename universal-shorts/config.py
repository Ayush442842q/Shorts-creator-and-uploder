# ============================================================
#  Universal Shorts Bot — Configuration
#  This file is gitignored — never commit it
# ============================================================

# ── Your Channel Identity ────────────────────────────────────
CHANNEL_NAME        = "My Channel"                        # Shown on video header
CHANNEL_DESCRIPTION = "A channel about cooking recipes"   # Drives AI script prompts
CHANNEL_HASHTAGS    = "#MyChannel #Shorts"                # Shown at bottom of video
CHANNEL_EMOJI       = "🎬"                                # Emoji used in header & titles
CHANNEL_CTA         = "Like and follow for daily shorts!" # Call to action at end of script

# ── API Keys ─────────────────────────────────────────────────
HF_API_TOKEN = "API_KEY_HERE"

TELEGRAM_BOT_A_TOKEN   = "TOKEN_HERE"
TELEGRAM_BOT_A_CHAT_ID = "CHAT_ID_HERE"

TELEGRAM_BOT_B_TOKEN   = "TOKEN_HERE"
TELEGRAM_BOT_B_CHAT_ID = "CHAT_ID_HERE"

YOUTUBE_CLIENT_SECRETS = "client_secrets.json"
YOUTUBE_SCOPES         = ["https://www.googleapis.com/auth/youtube.upload"]

TOPICS_FILE   = "topics.txt"
PROGRESS_FILE = "progress.txt"
OUTPUT_DIR    = "output"

VIDEO_WIDTH  = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS    = 30

BG_COLOR        = (10, 10, 40)
ACCENT_COLOR    = (0, 200, 255)
TEXT_COLOR      = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 200, 0)
