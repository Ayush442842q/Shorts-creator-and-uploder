# 🎬 Universal YouTube Shorts Bot

An automated pipeline that generates and uploads YouTube Shorts for **any niche** — fully free, no paid APIs.

Just describe your channel in `config.py` and drop your topics in `topics.txt`. The bot handles everything else.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20WSL-lightgrey)

---

## 🚀 Pipeline

```
python3 main.py
       ↓
Read CHANNEL_DESCRIPTION from config.py
       ↓
Zephyr-7B (HuggingFace Free) — generates script for your topic
       ↓
3-Layer Script Cleaner — removes stage directions, labels, filler
       ↓
Telegram Bot A — you receive the clean script
       ↓
Your audio file (voiceover.mp3) + Pillow + FFmpeg — builds the Short
       ↓
Telegram Bot B — you receive the final video
       ↓
YouTube Data API v3 — auto-uploads with title, description, tags
```

---

## 🛠️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/universal-shorts-bot.git
cd universal-shorts-bot
```

### 2. Install dependencies
```bash
pip install openai google-auth google-auth-oauthlib google-api-python-client pillow requests gtts
sudo apt install ffmpeg -y
```

### 3. Configure your channel
```bash
cp config.example.py config.py
```

Edit `config.py` and fill in **your channel identity first**:

```python
CHANNEL_NAME        = "Code With Me"
CHANNEL_DESCRIPTION = "A channel about Python programming tutorials for beginners"
CHANNEL_HASHTAGS    = "#Python #Coding #Shorts"
CHANNEL_EMOJI       = "🐍"
CHANNEL_CTA         = "Like and follow for daily Python tips!"
```

Then fill in your API keys.

### 4. Add your topics
Edit `topics.txt` — one topic per line, matching your niche:
```
Variables in Python
For Loops Explained
What is a Function
List vs Tuple
...
```

### 5. Add your audio
Place your voiceover/background audio as `audio/voiceover.mp3`

### 6. Add YouTube credentials
Place your YouTube OAuth2 file as `client_secrets.json`

### 7. Run
```bash
python3 main.py
```
On first run, a browser opens for YouTube OAuth. After that it's fully automatic.

---

## 🔑 API Keys Needed

| Key | Where to Get |
|-----|-------------|
| HuggingFace Token | huggingface.co → Settings → Access Tokens |
| Telegram Bot A Token | @BotFather on Telegram → /newbot |
| Telegram Bot B Token | @BotFather on Telegram → /newbot |
| Telegram Chat ID | Send /start to your bot → getUpdates API |
| YouTube OAuth JSON | Google Cloud Console → APIs & Services → Credentials |

---

## 📁 Project Structure

```
universal-shorts-bot/
├── main.py                  ← Entry point
├── config.py                ← Your channel config + API keys (gitignored)
├── config.example.py        ← Template — copy this to config.py
├── topics.txt               ← Your topics, one per line
├── client_secrets.json      ← YouTube OAuth (gitignored)
├── audio/
│   └── voiceover.mp3        ← Your background audio
├── modules/
│   ├── script_gen.py        ← 3-layer script generator (uses CHANNEL_DESCRIPTION)
│   ├── tts.py               ← Audio handler
│   ├── video_builder.py     ← FFmpeg video creator (uses CHANNEL_NAME, EMOJI, HASHTAGS)
│   ├── telegram_bot.py      ← Telegram notifications (uses CHANNEL_NAME)
│   └── youtube_upload.py    ← YouTube uploader (uses CHANNEL_NAME, DESCRIPTION)
└── output/                  ← Generated files (gitignored)
```

---

## 🤖 Models Used

| Task | Model | Cost |
|------|-------|------|
| Script Generation | `HuggingFaceH4/zephyr-7b-beta` | Free |
| Video Assembly | FFmpeg + Pillow | Free |
| Audio | User-provided file | Free |

---

## ⏰ Automate Daily Uploads (Cron)

To post one short every day at 9 AM:
```bash
crontab -e
# Add this line:
0 9 * * * cd /path/to/universal-shorts-bot && python3 main.py
```

---

## ⚠️ Important Notes

- Keep `config.py` and `client_secrets.json` out of version control (already in `.gitignore`)
- First YouTube upload requires browser authentication — after that it's automatic
- HuggingFace free tier can be slow — allow 2–5 minutes per run
- YouTube Shorts must be under 60 seconds (this bot targets 20 seconds)
- The bot tracks progress in `progress.txt` — it picks up from where it left off

---

## 💡 Channel Description Tips

The `CHANNEL_DESCRIPTION` is the most important config field. The AI reads it to write every script. Be specific:

| ❌ Too vague | ✅ Better |
|---|---|
| "A cooking channel" | "A channel teaching quick Indian recipes under 30 minutes" |
| "Tech stuff" | "A channel explaining AI and machine learning concepts for beginners" |
| "Fitness" | "A home workout channel focused on no-equipment exercises for busy people" |

---

## 📄 License

MIT License — free to use, modify and distribute.
