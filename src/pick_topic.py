"""Pick the next topic to produce and mark it in flight.

topics.csv columns:
    id, status, priority, category, title_hint, angle, keywords, published_url

status: pending | building | done | skip
Highest priority pending row wins; ties break on id.
"""
from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

from common import CONFIG_DIR, log

TOPICS = CONFIG_DIR / "topics.csv"
FIELDS = ["id", "status", "priority", "category", "title_hint", "angle",
          "keywords", "published_url"]


def read_rows() -> list[dict]:
    with TOPICS.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_rows(rows: list[dict]) -> None:
    with TOPICS.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def pick(rows: list[dict]) -> dict | None:
    pending = [r for r in rows if r["status"].strip() == "pending"]
    if not pending:
        return None
    pending.sort(key=lambda r: (-int(r["priority"] or 0), int(r["id"])))
    return pending[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mark", action="store_true",
                    help="set the chosen row to 'building'")
    ap.add_argument("--id", type=int, help="force a specific topic id")
    args = ap.parse_args()

    rows = read_rows()
    if args.id:
        row = next((r for r in rows if int(r["id"]) == args.id), None)
        if row is None:
            raise SystemExit(f"no topic with id {args.id}")
    else:
        row = pick(rows)

    if row is None:
        raise SystemExit(
            "No pending topics left. Add rows to config/topics.csv "
            "or run src/suggest_topics.py to generate more."
        )

    slug = f"{date.today():%Y-%m-%d}-{row['id']}"
    if args.mark:
        row["status"] = "building"
        write_rows(rows)

    log("topic", f"#{row['id']} [{row['category']}] {row['title_hint']}")
    # run_daily.py reads these from stdout; GitHub Actions reads them from the file.
    print(f"SLUG={slug}")
    print(f"TOPIC_ID={row['id']}")

    remaining = sum(1 for r in rows if r["status"].strip() == "pending")
    log("topic", f"{remaining} topics still pending")


if __name__ == "__main__":
    main()
