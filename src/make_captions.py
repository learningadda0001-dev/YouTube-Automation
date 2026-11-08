"""Burned-in Kannada captions as .ass

We already know the exact text, so timings are shared out across each scene's
own audio by character count. That beats transcribing: Kannada ASR is shaky,
and this cannot hallucinate a word that was never said.

Lines are balanced before being grouped into cues, otherwise greedy wrapping
leaves a cue holding one orphan word.
"""
from __future__ import annotations

import argparse
from math import ceil

from common import EPISODES, cfg, load_scenes, log

MIN_CUE = 0.9

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Kan,{font},{size},&H00FFFFFF,&H000000FF,&H00000000,&HB3000000,-1,0,0,0,100,100,0,0,3,8,0,2,120,120,{mv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ts(t: float) -> str:
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def wrap(text: str, width: int) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        candidate = f"{cur} {word}".strip()
        if len(candidate) <= width or not cur:
            cur = candidate
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def chunk(text: str, max_chars: int, max_lines: int) -> list[str]:
    n = max(1, ceil(len(text) / max_chars))
    lines = wrap(text, max_chars)
    for width in range(ceil(len(text) / n), max_chars + 1):
        candidate = wrap(text, width)
        if len(candidate) <= n:
            lines = candidate
            break
    return ["\\N".join(lines[i:i + max_lines])
            for i in range(0, len(lines), max_lines)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    args = ap.parse_args()

    c = cfg()
    cap, vis = c["captions"], c["visual"]
    pad = c["audio"]["scene_pad"]
    ep = EPISODES / args.slug
    scenes = load_scenes(ep)

    events, clock = [], 0.0
    for s in scenes:
        dur = float(s.get("audio_duration") or 0)
        if dur <= 0:
            raise SystemExit(f"{s['slug']} has no audio_duration — run gen_voice first")
        cues = chunk(s["narration"], cap["max_chars"], cap["max_lines"])
        weights = [max(len(x.replace("\\N", " ")), 1) for x in cues]
        span = sum(weights)
        t = clock
        for cue, w in zip(cues, weights):
            length = max(dur * w / span, MIN_CUE)
            events.append((t, min(t + length, clock + dur), cue))
            t += length
        clock += dur + pad

    header = HEADER.format(w=vis["width"], h=vis["height"], font=cap["font"],
                           size=cap["size"], mv=cap["margin_v"])
    body = "\n".join(f"Dialogue: 0,{ts(a)},{ts(b)},Kan,,0,0,0,,{txt}"
                     for a, b, txt in events)
    (ep / "captions.ass").write_text(header + body + "\n", encoding="utf-8")
    log("captions", f"{len(events)} cues over "
                    f"{int(clock // 60)}:{int(clock % 60):02d}")


if __name__ == "__main__":
    main()
