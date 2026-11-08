"""One image per scene, via Cloudflare Workers AI (FLUX-1-schnell).

The Workers AI free tier is 10,000 neurons a day, resetting 00:00 UTC. A
default FLUX-1-schnell image costs roughly 173 neurons, so about 57 images a
day — enough for one episode with headroom, and nothing else should share the
account or the episode will fail halfway.

Existing files are skipped, so a re-run after a failure only generates what is
missing. Set --provider pollinations as a keyless fallback.
"""
from __future__ import annotations

import argparse
import base64
import json
import time
from pathlib import Path

import requests

from common import EPISODES, cfg, env, load_scenes, log

CF_MODEL = "@cf/black-forest-labs/flux-1-schnell"


def cloudflare(prompt: str, out: Path, width: int, height: int) -> None:
    account = env("CF_ACCOUNT_ID")
    token = env("CF_API_TOKEN")
    url = f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/{CF_MODEL}"
    headers = {"Authorization": f"Bearer {token}"}
    body = {"prompt": prompt[:2000], "steps": 8, "width": width, "height": height}

    r = requests.post(url, headers=headers, json=body, timeout=180)
    if r.status_code in (400, 422):
        # Older Workers AI builds reject width/height and only emit squares.
        # assemble.py scales-and-crops to cover, so a square still works.
        r = requests.post(url, headers=headers,
                          json={"prompt": prompt[:2000], "steps": 8}, timeout=180)
    if r.status_code == 429:
        raise RuntimeError("rate limited — daily neuron budget may be spent")
    r.raise_for_status()
    payload = r.json()
    if not payload.get("success", True):
        raise RuntimeError(str(payload.get("errors"))[:300])
    b64 = payload["result"]["image"]
    out.write_bytes(base64.b64decode(b64))


def pollinations(prompt: str, out: Path, width: int, height: int) -> None:
    from urllib.parse import quote

    url = (f"https://image.pollinations.ai/prompt/{quote(prompt[:1500])}"
           f"?width={width}&height={height}&nologo=true&model=flux")
    r = requests.get(url, timeout=240)
    r.raise_for_status()
    out.write_bytes(r.content)


PROVIDERS = {"cloudflare": cloudflare, "pollinations": pollinations}


def generate(prompt: str, out: Path, w: int, h: int, provider: str,
             secondary: str, retries: int) -> str:
    """Try `provider`, fall back to `secondary`. Returns what actually made it."""
    last_error = None
    for attempt in range(retries):
        try:
            PROVIDERS[provider](prompt, out, w, h)
            return provider
        except Exception as exc:                          # noqa: BLE001
            last_error = exc
            time.sleep(2 ** attempt * 3)

    if secondary == "none" or secondary == provider:
        raise SystemExit(f"{out.stem} failed: {last_error}")
    log("images", f"{out.stem}: {provider} failed ({last_error}); "
                  f"falling back to {secondary}")
    PROVIDERS[secondary](prompt, out, w, h)
    return secondary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--provider", choices=list(PROVIDERS),
                    help="override the primary from style.yaml")
    ap.add_argument("--budget", type=int,
                    help="override how many images the primary provider makes")
    ap.add_argument("--retries", type=int, default=3)
    args = ap.parse_args()

    c = cfg()
    w, h = c["visual"]["width"], c["visual"]["height"]
    prov = c["visual"].get("providers", {})
    primary = args.provider or prov.get("primary", "cloudflare")
    secondary = prov.get("secondary", "pollinations")
    budget = args.budget if args.budget is not None else prov.get(
        "primary_budget", 50)

    ep = EPISODES / args.slug
    images = ep / "images"
    images.mkdir(exist_ok=True)
    scenes = load_scenes(ep)

    # A 20-minute episode needs ~100 images; Cloudflare's free tier is ~57 a
    # day. The first `budget` go to the primary, the rest to the secondary.
    if len(scenes) > budget:
        log("images", f"{len(scenes)} images needed: first {budget} from "
                      f"{primary}, remaining {len(scenes) - budget} from "
                      f"{secondary}")

    counts: dict[str, int] = {}
    skipped = 0
    spent = 0
    for s in scenes:
        out = images / f"{s['slug']}.png"
        if out.exists() and out.stat().st_size > 10_000:
            skipped += 1
            continue

        which = primary if spent < budget else secondary
        used = generate(s["image_prompt"], out, w, h, which, secondary,
                        args.retries)
        counts[used] = counts.get(used, 0) + 1
        if used == primary:
            spent += 1

        done = sum(counts.values())
        if done % 20 == 0:
            log("images", f"{done} generated ...")

    # The thumbnail gets its own frame when the outline described one.
    meta_path = ep / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        thumb_prompt = meta.get("thumbnail_image", "").strip()
        thumb = images / "thumbnail_src.png"
        if thumb_prompt and not thumb.exists():
            suffix = " ".join(c["visual"]["style_suffix"].split())
            try:
                generate(f"{thumb_prompt}, {suffix}", thumb, w, h,
                         secondary, secondary, args.retries)
                log("images", "thumbnail frame generated")
            except SystemExit:
                log("images", "thumbnail frame failed — will reuse a scene")

    summary = ", ".join(f"{n} via {p}" for p, n in counts.items()) or "none"
    log("images", f"{summary}; {skipped} reused")

    missing = [s["slug"] for s in scenes
               if not (images / f"{s['slug']}.png").exists()]
    if missing:
        raise SystemExit("missing images: " + ", ".join(missing))


if __name__ == "__main__":
    main()
