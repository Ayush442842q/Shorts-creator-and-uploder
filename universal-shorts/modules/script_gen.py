"""
script_gen.py — 3-layer pipeline: Generate → Aggressive Clean → Humanize
Universal version: driven by CHANNEL_DESCRIPTION and CHANNEL_CTA from config.
"""

import json, re, time
from openai import OpenAI
from config import HF_API_TOKEN, CHANNEL_DESCRIPTION, CHANNEL_CTA

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_TOKEN,
)
MODEL = "HuggingFaceH4/zephyr-7b-beta:featherless-ai"

CTA = CHANNEL_CTA


def _chat(system: str, user: str, max_tokens: int = 200) -> str:
    for attempt in range(3):
        try:
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"  [HF] Attempt {attempt+1}/3 failed: {e}")
            time.sleep(10)
    raise RuntimeError("HuggingFace API failed after 3 attempts")


# ── Layer 2: Aggressive Cleaner ───────────────────────────────────────────────

def _hard_clean(text: str) -> str:
    """
    Programmatically removes ALL non-spoken content.
    Does not rely on AI — pure regex + rules.
    """
    # 1. Remove everything inside [ ] and ( )
    text = re.sub(r'\[.*?\]', ' ', text, flags=re.DOTALL)
    text = re.sub(r'\(.*?\)', ' ', text, flags=re.DOTALL)

    # 2. Remove label prefixes like "Narrator:", "Host:", "VO:" etc.
    text = re.sub(
        r'\b(Narrator|Host|Speaker|Voiceover|VO|Presenter|Announcer)\s*:\s*',
        ' ', text, flags=re.IGNORECASE
    )

    # 3. Remove scene/direction prefixes
    text = re.sub(
        r'\b(Scene|Camera|Visual|Music|Sound|Cut|Fade|Show|Display)\s*:\s*',
        ' ', text, flags=re.IGNORECASE
    )

    # 4. Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # 5. Filter out sentences that are clearly stage directions
    direction_patterns = [
        r'^\s*(upbeat|music|sound|camera|visual|scene|show|display|cut|fade)',
        r'(lightbulb|turning on|turning off|zoom|pan|close.up)',
        r'^\s*\[', r'^\s*\(',
    ]
    clean_sentences = []
    for s in sentences:
        s = s.strip()
        if not s or len(s) < 15:
            continue
        is_direction = any(re.search(p, s, re.IGNORECASE) for p in direction_patterns)
        if not is_direction:
            clean_sentences.append(s)

    # 6. Remove filler openers from first sentence
    if clean_sentences:
        first = clean_sentences[0]
        first = re.sub(
            r'^(Hey (there|everyone|guys|folks)[,!.]?\s*|'
            r'Hello[,!]?\s*(everyone|there)?[,!.]?\s*|'
            r'Welcome (back|to)[^.]*\.\s*|'
            r'(Alright|Okay|So)[,\s]+|'
            r'(Today|In this video)[,\s]+we[\'re\s]+)',
            '', first, flags=re.IGNORECASE
        ).strip()
        if first:
            first = first[0].upper() + first[1:]
        clean_sentences[0] = first

    # 7. Keep max 4 content sentences + CTA
    content = [s for s in clean_sentences if CTA.lower() not in s.lower()]
    content = content[:4]
    content.append(CTA)

    return ' '.join(content)


# ── Layer 3: Humanizer ────────────────────────────────────────────────────────

def _humanize(text: str, topic: str) -> str:
    system = (
        "You are a script editor. Make the script sound like a real person talking — "
        "natural, confident, conversational. No stage directions. No brackets. "
        "Output ONLY the final spoken words."
    )
    user = (
        f'Rewrite this script about "{topic}" to sound natural and human. '
        f'Keep it under 5 sentences. '
        f'Keep the last line exactly: "{CTA}"\n\n'
        f'Script:\n{text}'
    )
    try:
        raw = _chat(system, user, max_tokens=150)
        return _hard_clean(raw)
    except Exception as e:
        print(f"  [ScriptGen] Humanizer failed: {e}, using cleaned version")
        return text


# ── Public API ────────────────────────────────────────────────────────────────

def generate_script(topic: str) -> str:
    print(f"  [ScriptGen] Writing script for: {topic}")

    # Layer 1 — Generate
    system = "Output ONLY spoken words for a 20-second YouTube Shorts voiceover. No labels, no brackets, no directions."
    user = (
        f'Channel context: {CHANNEL_DESCRIPTION}\n\n'
        f'Write a 20-second voiceover about: {topic}\n\n'
        f'Keep it engaging, educational, and relevant to the channel context above.\n'
        f'End with exactly: "{CTA}"\n\n'
        f'Output ONLY the spoken script, nothing else.'
    )
    raw = _chat(system, user, max_tokens=150)
    print(f"  [ScriptGen] Raw  : {raw[:80]}...")

    # Layer 2 — Hard clean
    cleaned = _hard_clean(raw)
    print(f"  [ScriptGen] Clean: {cleaned[:80]}...")

    # Layer 3 — Humanize
    final = _humanize(cleaned, topic)
    print(f"  [ScriptGen] Final: {final[:80]}...")

    return final


def generate_metadata(topic: str, script: str) -> dict:
    print(f"  [ScriptGen] Generating metadata...")
    system = "YouTube SEO expert. Output valid JSON only, no extra text."
    user = (
        f'Channel: {CHANNEL_DESCRIPTION}\n'
        f'Topic: {topic}\nScript: {script[:150]}\n\n'
        f'Return ONLY this JSON:\n'
        f'{{"title":"emoji+topic+#Shorts under 60 chars",'
        f'"description":"2 sentences relevant hashtags",'
        f'"tags":["Shorts","Education","{topic}"]}}'
    )
    raw = _chat(system, user, max_tokens=200)
    s, e = raw.find("{"), raw.rfind("}") + 1
    if s != -1 and e > s:
        try:
            return json.loads(raw[s:e])
        except Exception:
            pass
    return {
        "title":       f"{topic} Explained! #Shorts",
        "description": f"Learn about {topic} in 20 seconds! #Shorts",
        "tags":        ["Shorts", "Education", topic]
    }
