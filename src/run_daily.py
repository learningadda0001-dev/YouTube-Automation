"""One episode, start to finish.

    python src/run_daily.py                 # next pending topic, full run
    python src/run_daily.py --id 12         # a specific topic
    python src/run_daily.py --stop-before upload
    python src/run_daily.py --slug 2026-11-09-1 --from images   # resume

Every stage is skippable and resumable, because a daily job that cannot resume
after one flaky API call is a daily job that breaks within a week.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path

from common import EPISODES, log

SRC = Path(__file__).resolve().parent
STAGES = ["script", "parse", "voice", "images", "captions",
          "thumbnail", "assemble", "upload"]


def call(script: str, *a) -> str:
    cmd = [sys.executable, str(SRC / script), *[str(x) for x in a]]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    sys.stdout.write(proc.stdout)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr[-6000:])
        raise SystemExit(f"stage failed: {script}")
    return proc.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", type=int, help="force a topic id")
    ap.add_argument("--slug", help="resume an existing episode folder")
    ap.add_argument("--from", dest="start", choices=STAGES, default="script")
    ap.add_argument("--stop-before", choices=STAGES)
    ap.add_argument("--provider", default="gemini",
                    choices=["gemini", "anthropic"])
    ap.add_argument("--privacy", help="override style.yaml for this run")
    args = ap.parse_args()

    if args.slug:
        slug = args.slug
        topic_id = args.id or int(slug.rsplit("-", 1)[1])
    else:
        out = call("pick_topic.py", "--mark", *(["--id", args.id] if args.id else []))
        info = dict(
            line.split("=", 1) for line in out.splitlines() if "=" in line
            and line.split("=", 1)[0] in {"SLUG", "TOPIC_ID"}
        )
        slug, topic_id = info["SLUG"].strip(), int(info["TOPIC_ID"])

    start = STAGES.index(args.start)
    stop = STAGES.index(args.stop_before) if args.stop_before else len(STAGES)

    def active(name: str) -> bool:
        i = STAGES.index(name)
        return start <= i < stop

    log("run", f"episode {slug} (topic {topic_id}), "
               f"stages {STAGES[start]}..{STAGES[stop - 1]}")

    if active("script"):
        call("write_script.py", "--slug", slug, "--topic-id", topic_id,
             "--provider", args.provider)
    if active("parse"):
        call("parse_script.py", "--slug", slug)
    if active("voice"):
        call("gen_voice.py", "--slug", slug)
    if active("images"):
        call("gen_images.py", "--slug", slug)
    if active("captions"):
        call("make_captions.py", "--slug", slug)
    if active("thumbnail"):
        call("make_thumbnail.py", "--slug", slug)
    if active("assemble"):
        call("assemble.py", "--slug", slug)
    if active("upload"):
        call("upload.py", "--slug", slug, "--topic-id", topic_id,
             *(["--privacy", args.privacy] if args.privacy else []))

    log("run", f"done: {EPISODES / slug}")
    print(f"SLUG={slug}")


if __name__ == "__main__":
    main()
