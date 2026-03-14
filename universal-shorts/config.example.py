# ============================================================
#  Universal Shorts Bot — Configuration Template
#  Copy this file to config.py and fill in your values:
#  cp config.example.py config.py
# ============================================================

# ── Your Channel Identity ────────────────────────────────────
CHANNEL_NAME        = "My Channel"
CHANNEL_DESCRIPTION = "A channel about cooking recipes and kitchen tips"
# ^ MOST IMPORTANT: The AI uses this to write scripts. Be specific!
#   Examples:
#     "A channel about Python programming tutorials for beginners"
#     "A fitness channel about home workouts and nutrition"
#     "A history channel about ancient civilizations"

CHANNEL_HASHTAGS    = "#MyChannel #Shorts"
CHANNEL_EMOJI       = "🎬"
CHANNEL_CTA         = "Like and follow for daily shorts!"

# ── API Keys ─────────────────────────────────────────────────
HF_API_TOKEN = "hf_YOUR_TOKEN_HERE"

TELEGRAM_BOT_A_TOKEN   = "YOUR_BOT_A_TOKEN"
TELEGRAM_BOT_A_CHAT_ID = "YOUR_CHAT_ID"

TELEGRAM_BOT_B_TOKEN   = "YOUR_BOT_B_TOKEN"
TELEGRAM_BOT_B_CHAT_ID = "YOUR_CHAT_ID"

YOUTUBE_CLIENT_SECRETS = "client_secrets.json"
YOUTUBE_SCOPES         = ["https://www.googleapis.com/auth/youtube.upload"]

# ── Paths ────────────────────────────────────────────────────
TOPICS_FILE   = "topics.txt"
PROGRESS_FILE = "progress.txt"
OUTPUT_DIR    = "output"

# ── Video Settings ───────────────────────────────────────────
VIDEO_WIDTH  = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS    = 30

BG_COLOR        = (10, 10, 40)
ACCENT_COLOR    = (0, 200, 255)
TEXT_COLOR      = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 200, 0)
