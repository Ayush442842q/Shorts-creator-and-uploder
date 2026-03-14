"""
video_builder.py — Attractive YouTube Short (1080x1920)
Universal version: channel name, emoji, hashtags pulled from config.
"""

import os, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont
from config import VIDEO_WIDTH, VIDEO_HEIGHT, OUTPUT_DIR, CHANNEL_NAME, CHANNEL_EMOJI, CHANNEL_HASHTAGS

MAX_DURATION = 20.0

# Color palette
BG_TOP       = (5,   8,  35)
BG_BOTTOM    = (10, 20,  60)
CYAN         = (0,  210, 255)
YELLOW       = (255, 210,  0)
WHITE        = (255, 255, 255)
SOFT_WHITE   = (210, 220, 240)
DARK_CARD    = (15,  25,  70)
ACCENT_LINE  = (0,  180, 220)


def build_video(topic: str, script: str, audio_path: str, topic_index: int = 0) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    bg_path    = os.path.join(OUTPUT_DIR, "background.png")
    video_path = os.path.join(OUTPUT_DIR, f"short_{topic_index}.mp4")
    _create_frame(topic, script, bg_path)
    _encode(bg_path, audio_path, video_path)
    duration = _get_duration(video_path)
    print(f"  [VideoBuilder] Done: {video_path} ({duration:.1f}s)")
    return video_path


def _create_frame(topic: str, script: str, path: str):
    W, H = VIDEO_WIDTH, VIDEO_HEIGHT
    img  = Image.new("RGB", (W, H), BG_TOP)
    draw = ImageDraw.Draw(img)

    # ── Gradient background ───────────────────────────────────
    for y in range(H):
        t = y / H
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # ── Subtle dot grid ───────────────────────────────────────
    for x in range(0, W, 60):
        for y in range(0, H, 60):
            draw.ellipse([(x-2, y-2), (x+2, y+2)], fill=(20, 30, 80))

    # ── Glowing top bar ───────────────────────────────────────
    for i in range(6, 0, -1):
        draw.rectangle([(0, 0), (W, 4+i*6)], fill=(0, int(180*i/6), int(220*i/6)))
    draw.rectangle([(0, 0), (W, 8)], fill=CYAN)

    # ── Channel name (from config) ────────────────────────────
    draw.rectangle([(0, 0), (W, 85)], fill=(8, 12, 45))
    draw.rectangle([(0, 83), (W, 87)], fill=CYAN)
    header_text = f"{CHANNEL_EMOJI} {CHANNEL_NAME.upper()}"
    _text(draw, header_text, W//2, 44, _font(34, bold=True), CYAN, anchor="mm")

    # ── Topic card ────────────────────────────────────────────
    card_y1, card_y2 = 105, 105 + _topic_card_height(topic)
    _rounded_rect_gradient(draw, 35, card_y1, W-35, card_y2,
                           (0, 40, 100), (0, 25, 75), radius=24,
                           outline=CYAN, outline_w=3)
    draw.rectangle([(55, card_y1+15), (62, card_y2-15)], fill=YELLOW)

    topic_font = _font(58, bold=True)
    topic_wrap = textwrap.fill(topic.upper(), width=16)
    _text_shadow(draw, topic_wrap, W//2, (card_y1+card_y2)//2,
                 topic_font, YELLOW, anchor="mm", align="center")

    y_cursor = card_y2 + 22

    # ── Divider ───────────────────────────────────────────────
    draw.rectangle([(60, y_cursor), (W//2-30, y_cursor+3)], fill=CYAN)
    _text(draw, CHANNEL_EMOJI, W//2, y_cursor-4, _font(28), YELLOW, anchor="mm")
    draw.rectangle([(W//2+30, y_cursor), (W-60, y_cursor+3)], fill=CYAN)
    y_cursor += 28

    # ── Script text in styled card ────────────────────────────
    cta_zone   = 175
    avail_h    = H - y_cursor - cta_zone - 20
    font_size  = 36
    line_h     = font_size + 16
    line_width = 32

    font_body  = _font(font_size)
    wrapped    = textwrap.fill(script, width=line_width)
    lines      = wrapped.split('\n')
    max_lines  = max(1, int(avail_h // line_h))

    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip() + "..."

    total_text_h = len(lines) * line_h
    text_start_y = y_cursor + (avail_h - total_text_h) // 2

    pad = 20
    _rounded_rect_gradient(
        draw,
        40, text_start_y - pad,
        W - 40, text_start_y + total_text_h + pad,
        (12, 22, 62), (8, 15, 50), radius=18,
        outline=ACCENT_LINE, outline_w=1
    )

    for i, line in enumerate(lines):
        y = text_start_y + i * line_h
        color = CYAN if i == 0 else SOFT_WHITE
        _text_shadow(draw, line, W//2, y, font_body, color, anchor="mm")

    # ── Bottom CTA bar ────────────────────────────────────────
    cta_y = H - cta_zone
    _rounded_rect_gradient(draw, 0, cta_y, W, H,
                           (5, 15, 50), (3, 8, 35), radius=0,
                           outline=CYAN, outline_w=0)
    draw.rectangle([(0, cta_y), (W, cta_y+3)], fill=CYAN)

    for i in range(4, 0, -1):
        draw.rectangle([(0, cta_y+3), (W, cta_y+3+i*8)],
                       fill=(0, int(50*i/4), int(80*i/4)))

    cta_font = _font(33, bold=True)
    _text_shadow(draw, "👍 Like & Follow for Daily Shorts!", W//2,
                 cta_y + 52, cta_font, CYAN, anchor="mm")

    # Hashtags from config
    _text(draw, CHANNEL_HASHTAGS, W//2,
          cta_y + 105, _font(25), (120, 140, 190), anchor="mm")
    _text(draw, "▶  New short every day", W//2,
          cta_y + 145, _font(24, bold=True), YELLOW, anchor="mm")

    # ── Bottom bar ────────────────────────────────────────────
    draw.rectangle([(0, H-6), (W, H)], fill=CYAN)

    img.save(path, "PNG")
    print(f"  [VideoBuilder] Frame saved.")


def _topic_card_height(topic: str) -> int:
    lines = textwrap.fill(topic.upper(), width=16).count('\n') + 1
    return max(110, lines * 68 + 50)


def _rounded_rect_gradient(draw, x1, y1, x2, y2, color1, color2,
                            radius=20, outline=None, outline_w=2):
    for y in range(int(y1), int(y2)):
        t = (y - y1) / max(1, y2 - y1)
        r = int(color1[0] + (color2[0]-color1[0])*t)
        g = int(color1[1] + (color2[1]-color1[1])*t)
        b = int(color1[2] + (color2[2]-color1[2])*t)
        draw.line([(x1, y), (x2, y)], fill=(r, g, b))
    if outline:
        draw.rounded_rectangle([(x1, y1), (x2, y2)],
                                radius=radius, outline=outline, width=outline_w)


def _text(draw, text, x, y, font, color, anchor="mm", align="center"):
    draw.text((x, y), text, font=font, fill=color, anchor=anchor, align=align)


def _text_shadow(draw, text, x, y, font, color, anchor="mm", align="center"):
    draw.text((x+3, y+3), text, font=font, fill=(0, 0, 0),   anchor=anchor, align=align)
    draw.text((x+1, y+1), text, font=font, fill=(0, 0, 20),  anchor=anchor, align=align)
    draw.text((x,   y),   text, font=font, fill=color,       anchor=anchor, align=align)


def _font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()


def _encode(bg_path, audio_path, output_path):
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", bg_path,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", str(MAX_DURATION),
        "-shortest",
        "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}",
        output_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {r.stderr[-400:]}")


def _get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True
    )
    try:    return float(r.stdout.strip())
    except Exception: return 0.0
