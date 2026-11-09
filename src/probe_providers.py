"""Probe keyless image sources from wherever this runs, and report what works.

Throwaway diagnostic: the sandbox this was developed in cannot reach any of
these hosts, so the only honest way to know which are usable is to ask a
GitHub runner.
"""
from __future__ import annotations

import json
from urllib.parse import quote

import requests

PROMPT = ("cinematic film still of a 16th century south indian mud fort gate "
          "at golden hour, two spearmen, dust, photorealistic")


def check(name: str, fn) -> dict:
    try:
        size, note = fn()
        ok = size > 15_000
        return {"source": name, "ok": ok, "bytes": size, "note": note}
    except Exception as exc:                              # noqa: BLE001
        return {"source": name, "ok": False, "bytes": 0,
                "note": f"{type(exc).__name__}: {str(exc)[:160]}"}


def poll(params: str) -> tuple[int, str]:
    r = requests.get(
        f"https://image.pollinations.ai/prompt/{quote(PROMPT)}?{params}",
        timeout=180)
    return (len(r.content) if r.ok else 0,
            f"HTTP {r.status_code} {r.headers.get('content-type', '')}")


def openverse() -> tuple[int, str]:
    r = requests.get("https://api.openverse.org/v1/images/",
                     params={"q": "Mysore Palace", "license_type": "all-cc",
                             "page_size": 3},
                     headers={"User-Agent": "youtube-automation/1.0"},
                     timeout=60)
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        return 0, "no results"
    img = requests.get(results[0]["url"], timeout=120,
                       headers={"User-Agent": "youtube-automation/1.0"})
    return len(img.content), f"{len(results)} results, first is {results[0].get('license')}"


def commons() -> tuple[int, str]:
    r = requests.get("https://commons.wikimedia.org/w/api.php",
                     params={"action": "query", "generator": "search",
                             "gsrsearch": "Mysore Palace", "gsrlimit": 3,
                             "gsrnamespace": 6, "prop": "imageinfo",
                             "iiprop": "url", "iiurlwidth": 1920,
                             "format": "json"},
                     headers={"User-Agent": "youtube-automation/1.0 "
                                            "(github actions probe)"},
                     timeout=60)
    r.raise_for_status()
    pages = r.json().get("query", {}).get("pages", {})
    if not pages:
        return 0, "no results"
    first = next(iter(pages.values()))
    url = first["imageinfo"][0]["thumburl"]
    img = requests.get(url, timeout=120,
                       headers={"User-Agent": "youtube-automation/1.0"})
    return len(img.content), f"{len(pages)} results"


CHECKS = [
    ("pollinations (flux)", lambda: poll("width=1280&height=720&nologo=true&model=flux")),
    ("pollinations (turbo)", lambda: poll("width=1280&height=720&model=turbo")),
    ("pollinations (bare)", lambda: poll("width=1280&height=720")),
    ("openverse (real photos, CC)", openverse),
    ("wikimedia commons (real photos)", commons),
]


def main() -> None:
    results = [check(name, fn) for name, fn in CHECKS]
    print(json.dumps(results, indent=2))
    print()
    for r in results:
        mark = "WORKS" if r["ok"] else "no   "
        print(f"  {mark}  {r['source']:<34} {r['bytes']:>9,} bytes  {r['note']}")
    if not any(r["ok"] for r in results):
        print("\nNo keyless source available — a credential is required.")


if __name__ == "__main__":
    main()
