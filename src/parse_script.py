"""script.md -> scenes.json + meta.json

Also fails loudly on the things that silently ruin an episode: a scene with no
narration, a scene with no visual, or an English sentence that leaked into the
Kannada narration.
"""
from __future__ import annotations

import argparse
import json
import re

from common import EPISODES, cfg, log

SCENE_RE = re.compile(r"^\*\*(\d+)\.\*\*\s*$")
TAG_RE = re.compile(r"^\[([KVS])\]\s*(.*)$")
KANNADA = re.compile(r"[ಀ-೿]")


def parse_scenes(text: str) -> list[dict]:
    scenes, current = [], None
    for raw in text.splitlines():
        line = raw.strip()
        m = SCENE_RE.match(line)
        if m:
            if current:
                scenes.append(current)
            current = {"id": int(m.group(1)), "narration": "", "visual": "", "sfx": ""}
            continue
        if current is None:
            continue
        t = TAG_RE.match(line)
        if not t:
            continue
        tag, value = t.group(1), t.group(2).strip()
        if tag == "K":
            current["narration"] = value
        elif tag == "V":
            current["visual"] = value
        elif tag == "S":
            current["sfx"] = "" if value in {"—", "-", ""} else value
    if current:
        scenes.append(current)
    return scenes


def parse_meta(text: str) -> dict:
    block = re.search(r"---META---(.*?)---END---", text, re.S)
    if not block:
        return {}
    meta, key = {}, None
    for line in block.group(1).splitlines():
        m = re.match(r"^(title|description|tags|thumbnail_text|thumbnail_image|"
                     r"next_episode):\s*(.*)$", line.strip())
        if m:
            key = m.group(1)
            meta[key] = m.group(2)
        elif key and line.strip():
            meta[key] += "\n" + line.rstrip()
    if "tags" in meta:
        meta["tags"] = [t.strip() for t in meta["tags"].split(",") if t.strip()]
    return meta


def validate(scenes: list[dict], expected: int) -> None:
    problems = []
    if len(scenes) != expected:
        problems.append(f"{len(scenes)} scenes, expected {expected}")
    for s in scenes:
        if not s["narration"]:
            problems.append(f"scene {s['id']}: no narration")
        if not s["visual"]:
            problems.append(f"scene {s['id']}: no visual prompt")
        if s["narration"] and not KANNADA.search(s["narration"]):
            problems.append(f"scene {s['id']}: narration has no Kannada text")
        if KANNADA.search(s["visual"]):
            problems.append(f"scene {s['id']}: visual prompt is not in English")
    if problems:
        raise SystemExit("script validation failed:\n  " + "\n  ".join(problems))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    args = ap.parse_args()

    c = cfg()
    ep = EPISODES / args.slug
    text = (ep / "script.md").read_text(encoding="utf-8")

    scenes = parse_scenes(text)
    validate(scenes, c["channel"]["scenes"])

    suffix = " ".join(c["visual"]["style_suffix"].split())
    for s in scenes:
        s["slug"] = f"scene_{s['id']:02d}"
        s["image_prompt"] = f"{s['visual']}, {suffix}"

    (ep / "scenes.json").write_text(
        json.dumps(scenes, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    meta = parse_meta(text)
    if meta:
        (ep / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    chars = sum(len(s["narration"]) for s in scenes)
    est = chars / c["channel"]["chars_per_second"]
    log("parse", f"{len(scenes)} scenes, {chars} chars, "
                 f"~{int(est // 60)}:{int(est % 60):02d} estimated")


if __name__ == "__main__":
    main()
