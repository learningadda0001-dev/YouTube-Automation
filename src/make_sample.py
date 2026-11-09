"""Build a short sample episode to judge quality before full setup.

The voice is free and keyless (edge-tts). Images need one credential — either
CF_ACCOUNT_ID + CF_API_TOKEN, or a free HF_TOKEN. With neither, the sample
still renders with plain placeholder frames so you can at least hear the
narration and check the caption timing.

    python src/make_sample.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from common import cfg, episode_dir, log

SRC = Path(__file__).resolve().parent
SLUG = "sample"

# The opening of the hand-written Bengaluru script, which is the quality bar
# the generated scripts are aiming at. See docs/example-script.md.
SCENES = [
    {
        "narration": "ಪ್ರತಿದಿನ ಒಂದೂವರೆ ಕೋಟಿ ಜನ ಓಡಾಡುವ ನಗರ ಇದು. "
                     "ಭಾರತದ ಸಿಲಿಕಾನ್ ವ್ಯಾಲಿ ಅಂತ ಜಗತ್ತೇ ಕರೆಯುವ ಊರು.",
        "visual": "Aerial at dusk over a dense modern South Indian megacity, "
                  "endless lights, rivers of traffic",
    },
    {
        "narration": "ಆದರೆ ಈ ಮಹಾನಗರ ಹುಟ್ಟಿದ್ದು ಒಂದು ಮೊಲದ ಧೈರ್ಯದಿಂದ ಅಂತ "
                     "ನಿಮಗೆ ಗೊತ್ತಾ?",
        "visual": "Extreme close-up of a hare in dry golden grass, ears "
                  "twitching, turning sharply toward camera",
    },
    {
        "narration": "ಕ್ರಿ.ಶ. 1537. ಒಬ್ಬ ಪಾಳೇಗಾರ ಈ ಬಂಜರು ನೆಲದಲ್ಲಿ ನಾಲ್ಕು "
                     "ಜೋಡಿ ಎತ್ತುಗಳನ್ನು ಕಟ್ಟಿ ನೇಗಿಲು ಹೊಡೆದ. ಆ ನಾಲ್ಕು ಗೆರೆಗಳೇ "
                     "ಇವತ್ತಿನ ಬೆಂಗಳೂರಿನ ಮೊದಲ ನಕ್ಷೆ.",
        "visual": "Four white bullocks dragging a wooden plough across bare "
                  "red earth, a 16th century chieftain walking behind, huge "
                  "dust cloud, wide shot",
    },
    {
        "narration": "ಬೆಂಗಳೂರಿನಿಂದ ಕೇವಲ ಹದಿನೈದು ಕಿಲೋಮೀಟರ್ ದೂರದ ಬೇಗೂರಿನ ಒಂದು "
                     "ಕಲ್ಲಿನ ಮೇಲೆ, ಕ್ರಿ.ಶ. 890ರಲ್ಲೇ 'ಬೆಂಗಳೂರು' ಅನ್ನೋ ಹೆಸರು "
                     "ಕೆತ್ತಲಾಗಿದೆ.",
        "visual": "Extreme close-up of ancient Kannada script carved into a "
                  "weathered granite hero-stone, moss in the grooves, raking "
                  "sunlight, floating dust",
    },
    {
        "narration": "ಹಾಗಾದರೆ ಬೆಂಗಳೂರನ್ನು ಕಟ್ಟಿದವರು ಯಾರು? ಈ ನಗರದ ನಿಜವಾದ ಕಥೆ "
                     "ಏನು? ಕೊನೆಯವರೆಗೂ ನೋಡಿ.",
        "visual": "Silhouette of a 16th century South Indian chieftain on a "
                  "rocky outcrop overlooking empty scrubland at sunrise, "
                  "cape moving in the wind",
    },
]


def call(script: str, *args) -> None:
    cmd = [sys.executable, str(SRC / script), *[str(a) for a in args]]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    sys.stdout.write(proc.stdout)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr[-4000:])
        raise SystemExit(f"stage failed: {script}")


def pick_provider() -> str:
    """Prefer a keyed provider if one is configured, else the keyless one."""
    if os.getenv("CF_ACCOUNT_ID") and os.getenv("CF_API_TOKEN"):
        return "cloudflare"
    if os.getenv("HF_TOKEN"):
        return "huggingface"
    return "pollinations"


def placeholders(ep: Path, leaders: list[dict], w: int, h: int) -> None:
    """Plain gradient frames, so the sample still renders with no credentials."""
    images = ep / "images"
    images.mkdir(exist_ok=True)
    shades = ["0x6b5744", "0x4a5a63", "0x7a6048", "0x3f4a52", "0x8a7152"]
    for i, s in enumerate(leaders):
        out = images / f"{s['image']}.png"
        if out.exists():
            continue
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi",
             "-i", f"color=c={shades[i % len(shades)]}:size={w}x{h}:d=1",
             "-frames:v", "1", str(out)],
            capture_output=True, check=True,
        )
    log("sample", f"{len(leaders)} placeholder frames — no image credential "
                  f"found, so the visuals are blank. Add CF_ACCOUNT_ID + "
                  f"CF_API_TOKEN or a free HF_TOKEN to see real stills.")


def main() -> None:
    c = cfg()
    suffix = " ".join(c["visual"]["style_suffix"].split())
    group = max(1, int(c["visual"].get("scenes_per_image", 1)))
    w, h = c["visual"]["width"], c["visual"]["height"]

    ep = episode_dir(SLUG)
    scenes = []
    for i, s in enumerate(SCENES, start=1):
        leader = ((i - 1) // group) * group + 1
        scenes.append({
            "id": i,
            "slug": f"scene_{i:02d}",
            "narration": s["narration"],
            "visual": s["visual"],
            "sfx": "",
            "image": f"scene_{leader:02d}",
            "is_image_leader": i == leader,
            "image_prompt": f"{s['visual']}, {suffix}",
        })
    (ep / "scenes.json").write_text(
        json.dumps(scenes, ensure_ascii=False, indent=2), encoding="utf-8")
    (ep / "meta.json").write_text(json.dumps({
        "title": "Sample — ಬೆಂಗಳೂರು ಹುಟ್ಟಿದ ನಿಜವಾದ ಕಥೆ",
        "thumbnail_text": "890 ರಲ್ಲೇ ಬೆಂಗಳೂರು?",
        "thumbnail_image": "A 16th century South Indian mud fort gate at "
                           "golden hour with a lone spearman",
        "description": "Sample render. Not for upload.",
        "tags": ["sample"],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    provider = pick_provider()
    leaders = [s for s in scenes if s["is_image_leader"]]
    log("sample", f"{len(scenes)} scenes, {len(leaders)} images, "
                  f"image provider: {provider}")

    call("gen_voice.py", "--slug", SLUG, "--provider", "edge")
    try:
        call("gen_images.py", "--slug", SLUG, "--provider", provider,
             "--budget", 999)
    except SystemExit:
        # Never let the sample fail outright over images — a render with
        # placeholder frames still shows the voice, captions and pacing.
        log("sample", f"{provider} could not deliver; using placeholders")
        placeholders(ep, leaders, w, h)
    call("make_captions.py", "--slug", SLUG)
    call("make_thumbnail.py", "--slug", SLUG)
    call("assemble.py", "--slug", SLUG, "--preview")
    log("sample", f"done: {ep / 'final.mp4'}")


if __name__ == "__main__":
    main()
