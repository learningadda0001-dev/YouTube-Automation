"""Shared paths, config loading and small helpers."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
EPISODES = ROOT / "episodes"
ASSETS = ROOT / "assets"


def cfg() -> dict:
    return yaml.safe_load((CONFIG_DIR / "style.yaml").read_text(encoding="utf-8"))


def episode_dir(slug: str) -> Path:
    d = EPISODES / slug
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_scenes(ep: Path) -> list[dict]:
    return json.loads((ep / "scenes.json").read_text(encoding="utf-8"))


def save_scenes(ep: Path, scenes: list[dict]) -> None:
    (ep / "scenes.json").write_text(
        json.dumps(scenes, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def run(cmd: list, quiet: bool = True) -> None:
    """Run a subprocess, surfacing the tail of stderr when it fails."""
    proc = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr[-4000:] + "\n")
        raise SystemExit(f"command failed: {' '.join(str(c) for c in cmd[:5])} ...")
    if not quiet and proc.stdout:
        print(proc.stdout)


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def env(name: str, required: bool = True, default: str = "") -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise SystemExit(f"environment variable {name} is not set")
    return value


def log(stage: str, message: str) -> None:
    print(f"[{stage}] {message}", flush=True)
