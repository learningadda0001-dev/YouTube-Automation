"""Upload the finished episode to YouTube and mark the topic done.

Auth is a refresh token held in a secret, so this runs unattended. Generate it
once locally with  python src/auth_setup.py  and paste the printed value into
the YT_REFRESH_TOKEN repository secret.
"""
from __future__ import annotations

import argparse
import csv
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from common import CONFIG_DIR, EPISODES, cfg, env, log

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_URI = "https://oauth2.googleapis.com/token"


def service():
    creds = Credentials(
        token=None,
        refresh_token=env("YT_REFRESH_TOKEN"),
        client_id=env("YT_CLIENT_ID"),
        client_secret=env("YT_CLIENT_SECRET"),
        token_uri=TOKEN_URI,
        scopes=SCOPES,
    )
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)


def mark_done(topic_id: int, url: str) -> None:
    path = CONFIG_DIR / "topics.csv"
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fields, rows = reader.fieldnames, list(reader)
    for r in rows:
        if int(r["id"]) == topic_id:
            r["status"] = "done"
            r["published_url"] = url
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--topic-id", type=int, required=True)
    ap.add_argument("--privacy", help="override style.yaml")
    ap.add_argument("--publish-at", help="RFC3339, schedules instead of publishing")
    args = ap.parse_args()

    c = cfg()
    ep = EPISODES / args.slug
    video = ep / "final.mp4"
    if not video.exists():
        raise SystemExit("final.mp4 not found — run assemble.py first")

    meta = json.loads((ep / "meta.json").read_text(encoding="utf-8"))
    privacy = args.privacy or c["upload"]["privacy"]

    body = {
        "snippet": {
            "title": meta["title"][:100],
            "description": meta.get("description", "")[:5000],
            "tags": meta.get("tags", [])[:60],
            "categoryId": c["upload"]["category_id"],
            "defaultLanguage": c["channel"]["language"],
            "defaultAudioLanguage": c["channel"]["language"],
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": c["upload"]["made_for_kids"],
        },
    }
    if args.publish_at:
        body["status"]["privacyStatus"] = "private"
        body["status"]["publishAt"] = args.publish_at

    yt = service()
    req = yt.videos().insert(
        part="snippet,status", body=body,
        media_body=MediaFileUpload(str(video), chunksize=8 * 1024 * 1024,
                                   resumable=True),
    )
    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            log("upload", f"{int(status.progress() * 100)}%")

    vid = response["id"]
    url = f"https://youtu.be/{vid}"
    log("upload", url)

    thumb = ep / "thumbnail.jpg"
    if thumb.exists():
        yt.thumbnails().set(videoId=vid,
                            media_body=MediaFileUpload(str(thumb))).execute()
        log("upload", "thumbnail set")

    mark_done(args.topic_id, url)


if __name__ == "__main__":
    main()
