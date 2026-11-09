"""Depth maps for the 2.5D parallax move. White = near, black = far.

Tries Depth-Anything-V2-Small through onnxruntime, which is small enough to
run on a CPU runner in a couple of seconds an image. If the model cannot be
fetched or run for any reason, falls back to a gradient heuristic — the
bottom of a landscape or architecture frame is nearly always nearer than the
top, and even that crude map produces convincing parallax. The fallback
matters: a failure here must never cost the episode its motion.

    python src/gen_depth.py --slug 2026-11-09-1
"""
from __future__ import annotations

import argparse

import numpy as np
from PIL import Image, ImageFilter

from common import EPISODES, cfg, load_scenes, log

REPO = "onnx-community/depth-anything-v2-small"
CANDIDATE_FILES = ["onnx/model.onnx", "onnx/model_quantized.onnx", "model.onnx"]
SIZE = 518
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def load_session():
    """Return an onnxruntime session, or None if anything is unavailable."""
    try:
        import onnxruntime as ort
        from huggingface_hub import hf_hub_download
    except ImportError as exc:
        log("depth", f"onnxruntime/huggingface_hub unavailable ({exc})")
        return None

    for name in CANDIDATE_FILES:
        try:
            path = hf_hub_download(repo_id=REPO, filename=name)
        except Exception:                                 # noqa: BLE001
            continue
        try:
            sess = ort.InferenceSession(path, providers=["CPUExecutionProvider"])
            log("depth", f"using {REPO}/{name}")
            return sess
        except Exception as exc:                          # noqa: BLE001
            log("depth", f"could not open {name}: {exc}")
    log("depth", "model unavailable — falling back to the gradient heuristic")
    return None


def depth_from_model(sess, img: Image.Image) -> np.ndarray:
    arr = np.asarray(img.convert("RGB").resize((SIZE, SIZE), Image.BILINEAR),
                     dtype=np.float32) / 255.0
    arr = (arr - MEAN) / STD
    tensor = np.transpose(arr, (2, 0, 1))[None].astype(np.float32)
    name = sess.get_inputs()[0].name
    out = sess.run(None, {name: tensor})[0]
    d = np.squeeze(out).astype(np.float32)
    lo, hi = float(d.min()), float(d.max())
    if hi - lo < 1e-6:
        raise ValueError("flat depth output")
    return (d - lo) / (hi - lo)


def depth_from_gradient(img: Image.Image) -> np.ndarray:
    """Bottom-is-near, with a nudge from local contrast.

    Crude, but for wide landscape and architecture frames — which is most of
    what this channel generates — it is close enough to produce real depth
    separation rather than a flat pan.
    """
    g = np.asarray(img.convert("L").resize((SIZE, SIZE), Image.BILINEAR),
                   dtype=np.float32) / 255.0
    rows = np.linspace(0.0, 1.0, SIZE, dtype=np.float32)[:, None]
    vertical = rows ** 1.4
    detail = np.asarray(
        img.convert("L").resize((SIZE, SIZE), Image.BILINEAR)
        .filter(ImageFilter.FIND_EDGES), dtype=np.float32) / 255.0
    detail = np.clip(detail * 3.0, 0, 1)
    d = 0.78 * vertical + 0.22 * detail * (0.4 + 0.6 * g)
    return (d - d.min()) / max(d.max() - d.min(), 1e-6)


def to_mask(d: np.ndarray, w: int, h: int, cut: float, feather: int) -> Image.Image:
    """Soft near/far mask. Feathering is what stops the cut-out looking cut."""
    m = np.clip((d - cut) / max(1.0 - cut, 1e-6), 0, 1)
    img = Image.fromarray((m * 255).astype(np.uint8), mode="L")
    img = img.resize((w, h), Image.BILINEAR)
    return img.filter(ImageFilter.GaussianBlur(feather))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--cut", type=float, default=0.45,
                    help="depth above this counts as near")
    ap.add_argument("--feather", type=int, default=28)
    ap.add_argument("--method", choices=["auto", "model", "gradient"],
                    default="auto")
    args = ap.parse_args()

    c = cfg()["visual"]
    w, h = c["width"], c["height"]
    ep = EPISODES / args.slug
    out_dir = ep / "depth"
    out_dir.mkdir(exist_ok=True)

    sess = None if args.method == "gradient" else load_session()
    if sess is None and args.method == "model":
        raise SystemExit("depth model requested but unavailable")

    names = sorted({s.get("image", s["slug"]) for s in load_scenes(ep)})
    extra = ep / "images" / "thumbnail_src.png"
    if extra.exists():
        names.append("thumbnail_src")

    made = reused = by_model = by_gradient = 0
    for name in names:
        src = ep / "images" / f"{name}.png"
        dst = out_dir / f"{name}.png"
        if not src.exists():
            continue
        if dst.exists() and dst.stat().st_size > 2000:
            reused += 1
            continue

        img = Image.open(src)
        d = None
        if sess is not None:
            try:
                d = depth_from_model(sess, img)
                by_model += 1
            except Exception as exc:                      # noqa: BLE001
                log("depth", f"{name}: model failed ({exc}); using gradient")
        if d is None:
            d = depth_from_gradient(img)
            by_gradient += 1

        to_mask(d, w, h, args.cut, args.feather).save(dst)
        made += 1
        if made % 20 == 0:
            log("depth", f"{made}/{len(names)} ...")

    log("depth", f"{made} maps ({by_model} model, {by_gradient} gradient), "
                 f"{reused} reused")


if __name__ == "__main__":
    main()
