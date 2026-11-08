"""Turn a topic row into script.md.

A 20-minute episode is ~15,600 Kannada characters across 100 scenes. Asking
for that in one call gives a model that drifts, loses count and thins out
badly after the first third. So the script is built in stages: one outline
call that fixes the acts and the title, then one call per act that only has
to write ten or so scenes well, each given the previous act's last line so
the narration still joins up.

The prompts encode what the competitor research showed works: a question hook
in the first ten seconds, a myth-versus-evidence twist, concrete named detail,
a then-and-now beat, and a cliffhanger. They also force the hedging that keeps
the comments section friendly — legends must be marked as legends.

Providers: gemini (free tier) | anthropic
"""
from __future__ import annotations

import argparse
import csv
import json
import re

from common import CONFIG_DIR, cfg, env, episode_dir, log

SYSTEM = """You are the head writer for a Kannada YouTube history channel.
You write narration that a single male narrator reads over cinematic visuals.
You write in natural spoken Kannada, not textbook Kannada. Short sentences.
You never invent facts, and you mark every legend as a legend."""

ACCURACY = """ACCURACY RULES — not optional

- State as fact only what is well documented. Hedge everything else in the
  Kannada itself: "ಐತಿಹ್ಯದ ಪ್ರಕಾರ", "ಅಂತ ಹೇಳುತ್ತಾರೆ", "...ಅಂತೆ",
  "ಕೆಲವು ದಾಖಲೆಗಳು ಹೇಳುತ್ತವೆ".
- Never present a disputed date as settled. Never invent a quotation.
- Nothing that reads as an attack on a living person, a community, a caste or
  a religion. Describe what happened; pass no judgement on groups.
- Where the topic is religious, describe belief respectfully as belief."""

OUTLINE_PROMPT = """Plan one episode. Return ONLY valid JSON, no code fence.

TOPIC: {title_hint}
ANGLE: {angle}
CATEGORY: {category}
KEYWORDS: {keywords}

The finished episode runs about {minutes} minutes: {total_chars} characters of
Kannada narration across {scenes} scenes, in {acts} acts.

Shape it like this:
- Act 1 is the hook, 6 scenes. Scene 1 states something the viewer already
  knows or can see. Scene 2 or 3 asks the question the whole episode answers.
  The last hook scene promises a specific payoff and says "ಕೊನೆಯವರೆಗೂ ನೋಡಿ".
- The middle acts each open on a concrete named detail — a year, a place, a
  number, a name — never a generalisation. At this length each act needs real
  substance: people, decisions, numbers, consequences. If the topic cannot
  carry {minutes} minutes honestly, widen it to its context rather than
  repeating yourself.
- At least one act carries a MYTH-VS-EVIDENCE beat: the popular story, then
  what the inscription or record actually shows.
- At least one act carries a THEN-AND-NOW beat: what stood there once, what
  stands there today.
- The final act closes the loop and teases the next episode specifically.

{accuracy}

JSON shape:
{{
  "title": "Kannada title, a question or a surprising claim, one 😱, then a pipe, then English keywords. Under 100 characters.",
  "thumbnail_text": "3 to 5 Kannada words, the biggest claim",
  "thumbnail_image": "English image prompt for the thumbnail, one frame",
  "description": "3 short Kannada paragraphs",
  "tags": ["14 tags mixing Kannada and English"],
  "next_episode": "one line on what the teaser promised",
  "acts": [
    {{"n": 1, "name": "short English label", "scenes": 6,
      "covers": "2-3 sentences on exactly what this act narrates, in English,
                 specific enough that a writer could not drift off it"}}
  ]
}}

The "scenes" values must add up to exactly {scenes}."""

ACT_PROMPT = """Write act {n} of {acts} — "{name}".

EPISODE TOPIC: {title_hint}
THIS ACT COVERS: {covers}
FULL OUTLINE, so you do not repeat other acts:
{outline_summary}

{previous}

Write exactly {scenes} scenes, numbered {first} to {last}.
Total Kannada narration in this act: between {min_chars} and {max_chars}
characters — roughly {per_scene} per scene. Count as you go.

Format, repeated for each scene, nothing between scenes:

**N.**
[K] <Kannada narration>
[V] <the visual, in ENGLISH, as an image-generation prompt>
[S] <sound effect, or a single em dash if none>

- [K] is spoken Kannada. No English except proper nouns and years Kannada
  speakers actually say in English. No headings or bullets inside [K].
- [V] is one English sentence for a single still frame: subject, setting,
  light, camera distance. No camera movement, no text in frame, no named
  living people. Prefer wide and medium shots — close-up faces render badly.

{accuracy}

Output the scenes only. No preamble, no act heading, no closing remarks."""


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
        timeout=900,
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

    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": env("ANTHROPIC_API_KEY"),
                 "anthropic-version": "2023-06-01",
                 "Content-Type": "application/json"},
        json={
            "model": env("ANTHROPIC_MODEL", required=False,
                         default="claude-sonnet-5-5"),
            "max_tokens": 32000, "temperature": 0.8,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=900,
    )
    r.raise_for_status()
    return "".join(b.get("text", "") for b in r.json()["content"])


def narration_chars(text: str) -> int:
    return sum(len(m) for m in re.findall(r"^\[K\]\s*(.+)$", text, re.M))


def scene_count(text: str) -> int:
    return len(re.findall(r"^\*\*\d+\.\*\*", text, re.M))


def last_line(text: str) -> str:
    found = re.findall(r"^\[K\]\s*(.+)$", text, re.M)
    return found[-1] if found else ""


def renumber(text: str, first: int) -> str:
    """Force sequential numbering — models drift on long counts."""
    counter = [first - 1]

    def bump(_m):
        counter[0] += 1
        return f"**{counter[0]}.**"

    return re.sub(r"^\*\*\d+\.\*\*", bump, text, flags=re.M)


def parse_outline(raw: str) -> dict:
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.M).strip()
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start < 0 or end < 0:
        raise SystemExit(f"outline was not JSON:\n{raw[:800]}")
    return json.loads(cleaned[start:end + 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--topic-id", type=int, required=True)
    ap.add_argument("--provider", choices=["gemini", "anthropic"],
                    default="gemini")
    ap.add_argument("--retries", type=int, default=2)
    args = ap.parse_args()

    c = cfg()["channel"]
    scenes_total, acts_total = c["scenes"], c["acts"]
    cps = c["chars_per_second"]
    total_chars = int(c["target_minutes"] * 60 * cps)
    floor = int(c["min_minutes"] * 60 * cps)
    ceiling = int(c["max_minutes"] * 60 * cps)

    with (CONFIG_DIR / "topics.csv").open(encoding="utf-8", newline="") as fh:
        row = next(r for r in csv.DictReader(fh) if int(r["id"]) == args.topic_id)

    call = gemini if args.provider == "gemini" else anthropic

    # --- stage 1: outline -------------------------------------------------
    outline = parse_outline(call(SYSTEM, OUTLINE_PROMPT.format(
        title_hint=row["title_hint"], angle=row["angle"],
        category=row["category"], keywords=row["keywords"],
        minutes=c["target_minutes"], total_chars=total_chars,
        scenes=scenes_total, acts=acts_total, accuracy=ACCURACY,
    )))

    plan = outline.get("acts", [])
    planned = sum(int(a["scenes"]) for a in plan)
    if planned != scenes_total and planned > 0:
        # Scale the act sizes to hit the real total rather than failing.
        for a in plan:
            a["scenes"] = max(3, round(int(a["scenes"]) * scenes_total / planned))
        drift = scenes_total - sum(int(a["scenes"]) for a in plan)
        plan[-1]["scenes"] = int(plan[-1]["scenes"]) + drift
    log("script", f"outline: {len(plan)} acts, "
                  f"{sum(int(a['scenes']) for a in plan)} scenes")

    summary = "\n".join(f"  Act {a['n']}: {a['name']} — {a['covers']}"
                        for a in plan)

    # --- stage 2: one call per act ---------------------------------------
    pieces, cursor, tail = [], 1, ""
    for a in plan:
        n_scenes = int(a["scenes"])
        budget = int(total_chars * n_scenes / scenes_total)
        prev = (f'The previous act ended on this line, so do not repeat it '
                f'and do not re-introduce the subject:\n  "{tail}"'
                if tail else "This is the opening act.")

        prompt = ACT_PROMPT.format(
            n=a["n"], acts=len(plan), name=a["name"],
            title_hint=row["title_hint"], covers=a["covers"],
            outline_summary=summary, previous=prev,
            scenes=n_scenes, first=cursor, last=cursor + n_scenes - 1,
            min_chars=int(budget * 0.85), max_chars=int(budget * 1.2),
            per_scene=int(budget / n_scenes), accuracy=ACCURACY,
        )

        text = ""
        for attempt in range(args.retries + 1):
            text = call(SYSTEM, prompt)
            got, n = narration_chars(text), scene_count(text)
            if n == n_scenes and budget * 0.8 <= got <= budget * 1.3:
                break
            prompt += (f"\n\nYour last attempt had {n} scenes and {got} "
                       f"characters. Rewrite with exactly {n_scenes} scenes "
                       f"and about {budget} characters.")
        text = renumber(text.strip(), cursor)
        pieces.append(text)
        cursor += scene_count(text)
        tail = last_line(text)
        log("script", f"act {a['n']} '{a['name']}': {scene_count(text)} scenes, "
                      f"{narration_chars(text)} chars")

    script = "\n\n".join(pieces)
    chars = narration_chars(script)
    minutes = chars / cps / 60
    log("script", f"total {scene_count(script)} scenes, {chars} chars, "
                  f"~{minutes:.1f} min")
    if not floor <= chars <= ceiling:
        log("script", f"WARNING: {minutes:.1f} min is outside the "
                      f"{c['min_minutes']}–{c['max_minutes']} min range")

    meta_block = "\n".join([
        "---META---",
        f"title: {outline.get('title', row['title_hint'])}",
        f"description: {outline.get('description', '')}",
        f"tags: {', '.join(outline.get('tags', []))}",
        f"thumbnail_text: {outline.get('thumbnail_text', '')}",
        f"thumbnail_image: {outline.get('thumbnail_image', '')}",
        f"next_episode: {outline.get('next_episode', '')}",
        "---END---",
    ])

    ep = episode_dir(args.slug)
    (ep / "script.md").write_text(f"{script}\n\n{meta_block}\n", encoding="utf-8")
    (ep / "outline.json").write_text(
        json.dumps(outline, ensure_ascii=False, indent=2), encoding="utf-8")
    log("script", f"wrote {ep / 'script.md'}")


if __name__ == "__main__":
    main()
