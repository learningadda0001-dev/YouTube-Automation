"""Thumbnail: generated frame + the big Kannada claim in yellow.

Thumbnails decide the click in this niche, so this is not decoration. The
layout is deliberately plain — a darkened image, a heavy yellow Kannada line
in the upper left, a red ring bottom-right — because it has to read at phone
size in a crowded sidebar.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from common import ASSETS, EPISODES, cfg, log

W, H = 1280, 720
YELLOW = (255, 214, 10)
RED = (229, 57, 53)


def font_path() -> Path:
    candidates = [
        ASSETS / "fonts" / "NotoSansKannada-Bold.ttf",
        Path("/usr/share/fonts/truetype/noto/NotoSansKannada-Bold.ttf"),
        Path("C:/Windows/Fonts/Nirmala.ttf"),
    ]
    for p in candidates:
        if p.exists():
            return p
    raise SystemExit(
        "No Kannada font found. Put NotoSansKannada-Bold.ttf in assets/fonts/."
    )


def fit(draw, text, font_file, max_w, start=96, min_size=48):
    """Largest size at which the text wraps into at most 3 lines inside max_w."""
    for size in range(start, min_size - 1, -4):
        font = ImageFont.truetype(str(font_file), size)
        words, lines, cur = text.split(), [], ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if draw.textlength(trial, font=font) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        if len(lines) <= 3:
            return font, lines
    return ImageFont.truetype(str(font_file), min_size), [text]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    args = ap.parse_args()

    cfg()
    ep = EPISODES / args.slug
    meta = json.loads((ep / "meta.json").read_text(encoding="utf-8"))

    src = ep / "images" / "thumbnail_src.png"
    if not src.exists():
        # Fall back to the strongest shot we already have.
        src = next(iter(sorted((ep / "images").glob("scene_*.png"))), None)
        if src is None:
            raise SystemExit("no images to build a thumbnail from")

    img = Image.open(src).convert("RGB")
    scale = max(W / img.width, H / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)),
                     Image.LANCZOS)
    left = (img.width - W) // 2
    top = (img.height - H) // 2
    img = img.crop((left, top, left + W, top + H))

    img = ImageEnhance.Color(img).enhance(1.15)
    img = ImageEnhance.Contrast(img).enhance(1.1)

    # Darken the upper-left so the text always has something to sit on.
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle([0, 0, int(W * 0.72), int(H * 0.52)], fill=165)
    shade = shade.filter(ImageFilter.GaussianBlur(70))
    img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, shade)

    draw = ImageDraw.Draw(img)
    text = meta.get("thumbnail_text") or meta.get("title", "")[:28]
    font, lines = fit(draw, text, font_path(), max_w=int(W * 0.62))

    y = 54
    for line in lines:
        for dx, dy in ((-4, 0), (4, 0), (0, -4), (0, 4), (-3, -3), (3, 3)):
            draw.text((56 + dx, y + dy), line, font=font, fill=(0, 0, 0))
        draw.text((56, y), line, font=font, fill=YELLOW)
        y += int(font.size * 1.18)

    draw.ellipse([W - 190, H - 190, W - 50, H - 50], outline=RED, width=12)

    out = ep / "thumbnail.jpg"
    img.save(out, "JPEG", quality=90)
    log("thumbnail", f"{out}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
