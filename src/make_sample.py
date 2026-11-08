"""Build a short sample episode using only the keyless providers.

Needs no secrets at all: Pollinations for the images, edge-tts for the voice.
Run it to see what the finished product actually looks and sounds like before
setting up any API keys.

    python src/make_sample.py
"""
from __future__ import annotations

import json
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


def main() -> None:
    c = cfg()
    suffix = " ".join(c["visual"]["style_suffix"].split())

    ep = episode_dir(SLUG)
    scenes = []
    for i, s in enumerate(SCENES, start=1):
        scenes.append({
            "id": i,
            "slug": f"scene_{i:02d}",
            "narration": s["narration"],
            "visual": s["visual"],
            "sfx": "",
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

    log("sample", f"{len(scenes)} scenes — keyless providers only")
    call("gen_voice.py", "--slug", SLUG, "--provider", "edge")
    call("gen_images.py", "--slug", SLUG, "--provider", "pollinations",
         "--budget", 0)
    call("make_captions.py", "--slug", SLUG)
    call("make_thumbnail.py", "--slug", SLUG)
    call("assemble.py", "--slug", SLUG)
    log("sample", f"done: {ep / 'final.mp4'}")


if __name__ == "__main__":
    main()
