"""Turn a topic row into script.md.

The prompt below encodes everything the competitor research showed works:
a question hook in the first 10 seconds, a myth-vs-evidence twist, concrete
named detail, a then-and-now beat, and a cliffhanger. It also forces the
hedging language that keeps the comments section friendly — legends must be
marked as legends.

Providers: gemini (free tier) | anthropic
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

from common import CONFIG_DIR, cfg, env, episode_dir, log

SYSTEM = """You are the head writer for a Kannada YouTube history channel.
You write narration that a single male narrator reads over cinematic visuals.
You write in natural spoken Kannada, not textbook Kannada. Short sentences.
You never invent facts, and you mark every legend as a legend."""

TEMPLATE = """Write the full script for one episode.

TOPIC: {title_hint}
ANGLE: {angle}
CATEGORY: {category}
KEYWORDS: {keywords}

HARD REQUIREMENTS

1. Exactly {scenes} scenes, numbered 1..{scenes}.
2. Total Kannada narration across all scenes: between {min_chars} and
   {max_chars} characters. That is the single most important constraint —
   count as you go. Each scene is therefore roughly {per_scene} characters.
3. Output format, repeated for every scene, nothing else between scenes:

**N.**
[K] <the Kannada narration for this scene>
[V] <the visual, in ENGLISH, as an image-generation prompt>
[S] <sound effect, or a single em dash if none>

4. [K] is spoken Kannada. No English words except proper nouns and years that
   Kannada speakers actually say in English. No bullet points, no headings
   inside [K].
5. [V] is one English sentence describing a single still frame: subject,
   setting, light, camera distance. No camera movement (that is added later),
   no text in the image, no named living people.

STRUCTURE

- Scenes 1-5 are the hook. Scene 1 states something the viewer already knows
  or can see. Scene 2 or 3 asks the question the whole video answers. Scene 5
  promises a specific payoff and says "ಕೊನೆಯವರೆಗೂ ನೋಡಿ".
- Then 5 to 7 acts. Each act opens with a concrete named detail — a year, a
  place, a number, a name — not a generalisation.
- Include at least one MYTH-VS-EVIDENCE beat: the popular story, then what the
  inscription or record actually shows.
- Include at least one THEN-AND-NOW beat: what stood there once, what stands
  there today.
- The last 3 scenes close the loop and set up the next episode with a specific
  teaser, ending with "ಚಾನೆಲ್ ಸಬ್‌ಸ್ಕ್ರೈಬ್ ಮಾಡಿ".

ACCURACY RULES — these are not optional

- State as fact only what is well documented. Everything else is hedged in the
  Kannada itself: "ಐತಿಹ್ಯದ ಪ್ರಕಾರ", "ಅಂತ ಹೇಳುತ್ತಾರೆ", "...ಅಂತೆ",
  "ಕೆಲವು ದಾಖಲೆಗಳು ಹೇಳುತ್ತವೆ".
- Never state a disputed date as settled. Never invent a quotation.
- Avoid anything that reads as an attack on a living person, a community, a
  caste or a religion. Describe what happened; do not pass judgement on groups.
- If the topic is religious, describe belief respectfully as belief.

AFTER THE SCENES, output exactly this block:

---META---
title: <Kannada title, a question or a surprising claim, with one 😱, then a
  pipe, then English keywords for search. Under 100 characters total.>
description: <3 short Kannada paragraphs, then a blank line, then the chapter
  list as "MM:SS heading", then a blank line, then 8 hashtags>
tags: <14 comma-separated tags, mixing Kannada and English>
thumbnail_text: <3 to 5 Kannada words, the biggest claim in the video>
thumbnail_image: <English image prompt for the thumbnail, a single frame>
next_episode: <one line on what the teaser promised>
---END---
"""


def gemini(system: str, prompt: str) -> str:
    import requests

    key = env("GEMINI_API_KEY")
    model = env("GEMINI_MODEL", required=False, default="gemini-2.5-pro")
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        json={
            "system_instruction": {"parts": [{"text": system}]},
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.8, "maxOutputTokens": 32000},
        },
        timeout=600,
    )
    r.raise_for_status()
    data = r.json()
    try:
        return "".join(
            p.get("text", "") for p in data["candidates"][0]["content"]["parts"]
        )
    except (KeyError, IndexError):
        raise SystemExit(f"unexpected Gemini response: {json.dumps(data)[:1000]}")


def anthropic(system: str, prompt: str) -> str:
    import requests

    key = env("ANTHROPIC_API_KEY")
    model = env("ANTHROPIC_MODEL", required=False, default="claude-sonnet-5-5")
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "max_tokens": 32000,
            "temperature": 0.8,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=600,
    )
    r.raise_for_status()
    return "".join(b.get("text", "") for b in r.json()["content"])


def narration_chars(text: str) -> int:
    return sum(len(m) for m in re.findall(r"^\[K\]\s*(.+)$", text, re.M))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--topic-id", type=int, required=True)
    ap.add_argument("--provider", choices=["gemini", "anthropic"], default="gemini")
    ap.add_argument("--retries", type=int, default=2)
    args = ap.parse_args()

    c = cfg()
    scenes = c["channel"]["scenes"]
    cps = c["channel"]["chars_per_second"]
    target = c["channel"]["target_minutes"] * 60 * cps
    min_chars, max_chars = int(target * 0.92), int(target * 1.12)

    with (CONFIG_DIR / "topics.csv").open(encoding="utf-8", newline="") as fh:
        row = next(r for r in csv.DictReader(fh) if int(r["id"]) == args.topic_id)

    prompt = TEMPLATE.format(
        title_hint=row["title_hint"], angle=row["angle"],
        category=row["category"], keywords=row["keywords"],
        scenes=scenes, min_chars=min_chars, max_chars=max_chars,
        per_scene=int(target / scenes),
    )

    call = gemini if args.provider == "gemini" else anthropic
    text = ""
    for attempt in range(args.retries + 1):
        text = call(SYSTEM, prompt)
        got = narration_chars(text)
        n = len(re.findall(r"^\*\*\d+\.\*\*", text, re.M))
        log("script", f"attempt {attempt + 1}: {n} scenes, {got} chars "
                      f"(~{got / cps / 60:.1f} min)")
        if min_chars <= got <= max_chars and n == scenes:
            break
        prompt += (
            f"\n\nYour previous attempt had {n} scenes and {got} narration "
            f"characters. Rewrite it with exactly {scenes} scenes and between "
            f"{min_chars} and {max_chars} characters of Kannada narration."
        )
    else:
        log("script", "WARNING: length never landed in range — using last attempt")

    ep = episode_dir(args.slug)
    (ep / "script.md").write_text(text.strip() + "\n", encoding="utf-8")
    log("script", f"wrote {ep / 'script.md'}")


if __name__ == "__main__":
    main()
