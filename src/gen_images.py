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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--provider", choices=list(PROVIDERS), default="cloudflare")
    ap.add_argument("--fallback", choices=list(PROVIDERS) + ["none"],
                    default="pollinations")
    ap.add_argument("--retries", type=int, default=3)
    args = ap.parse_args()

    c = cfg()
    w, h = c["visual"]["width"], c["visual"]["height"]
    ep = EPISODES / args.slug
    images = ep / "images"
    images.mkdir(exist_ok=True)
    scenes = load_scenes(ep)

    made = skipped = fell_back = 0
    for s in scenes:
        out = images / f"{s['slug']}.png"
        if out.exists() and out.stat().st_size > 10_000:
            skipped += 1
            continue

        prompt = s["image_prompt"]
        last_error = None
        for attempt in range(args.retries):
            try:
                PROVIDERS[args.provider](prompt, out, w, h)
                made += 1
                last_error = None
                break
            except Exception as exc:                      # noqa: BLE001
                last_error = exc
                time.sleep(2 ** attempt * 3)

        if last_error is not None:
            if args.fallback == "none":
                raise SystemExit(f"{s['slug']} failed: {last_error}")
            log("images", f"{s['slug']}: {args.provider} failed "
                          f"({last_error}); trying {args.fallback}")
            PROVIDERS[args.fallback](prompt, out, w, h)
            fell_back += 1

        if (made + fell_back) % 10 == 0:
            log("images", f"{made + fell_back} generated ...")

    log("images", f"{made} generated, {fell_back} via fallback, {skipped} reused")

    missing = [s["slug"] for s in scenes
               if not (images / f"{s['slug']}.png").exists()]
    if missing:
        raise SystemExit("missing images: " + ", ".join(missing))


if __name__ == "__main__":
    main()
