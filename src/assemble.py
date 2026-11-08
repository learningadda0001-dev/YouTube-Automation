"""Stills -> finished video.

Each scene is one generated image held for exactly its own narration length,
with a slow camera move applied in ffmpeg (push in, pull out, pan). A scene
longer than style.yaml's split_after is cut into two moves on the same image,
so the framing changes every few seconds even though one image covers the
whole scene — that is what keeps a stills-based video from reading as a
slideshow.

Light grain and a vignette go on top, because a perfectly clean AI still looks
synthetic and a little noise reads as film.
"""
from __future__ import annotations

import argparse
import shutil

from common import EPISODES, cfg, load_scenes, log, probe_duration, run

# Pre-scaling the still before zoompan is what stops the zoom from juddering:
# zoompan rounds crop offsets to whole input pixels, so a big input makes each
# step sub-pixel at output size.
PRESCALE = 2560


def move_filter(kind: str, frames: int, zps: float, w: int, h: int, fps: int) -> str:
    end_zoom = 1.0 + zps * frames / fps
    if kind == "push_in":
        z = f"1.0+{zps / fps:.6f}*on"
        x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif kind == "pull_out":
        z = f"{end_zoom:.4f}-{zps / fps:.6f}*on"
        x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif kind == "pan_right":
        z = "1.14"
        x, y = f"(iw-iw/zoom)*on/{frames}", "ih/2-(ih/zoom/2)"
    else:  # pan_left
        z = "1.14"
        x, y = f"(iw-iw/zoom)*(1-on/{frames})", "ih/2-(ih/zoom/2)"

    # Scale-and-crop to cover 16:9 first, so a square image from a provider
    # that ignores width/height still fills the frame instead of pillarboxing.
    # Grain and vignette are deliberately NOT here — they go in the single
    # final encode, so each scene costs one cheap pass instead of two dear ones.
    return (
        f"scale={PRESCALE}:{PRESCALE * h // w}:force_original_aspect_ratio=increase,"
        f"crop={PRESCALE}:{PRESCALE * h // w},setsar=1,"
        f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={w}x{h}:fps={fps},"
        f"format=yuv420p"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--keep-temp", action="store_true")
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg not found on PATH")

    c = cfg()
    vis, aud = c["visual"], c["audio"]
    w, h, fps = vis["width"], vis["height"], vis["fps"]
    zps = vis["motion"]["zoom_per_second"]
    split_after = vis["motion"]["split_after"]
    moves = vis["motion"]["moves"]

    ep = EPISODES / args.slug
    tmp = ep / "_tmp"
    tmp.mkdir(exist_ok=True)
    scenes = load_scenes(ep)

    segments = []
    for i, s in enumerate(scenes):
        img = ep / "images" / f"{s.get('image', s['slug'])}.png"
        voice = ep / "audio" / f"{s['slug']}.mp3"
        if not img.exists():
            raise SystemExit(f"missing image {img.name} for {s['slug']}")
        if not voice.exists():
            raise SystemExit(f"missing audio for {s['slug']}")

        dur = float(s["audio_duration"]) + aud["scene_pad"]
        # Long scenes get two moves on the same still so the shot changes.
        parts = 2 if dur > split_after else 1
        part_dur = dur / parts

        piece_paths = []
        for p in range(parts):
            kind = moves[(i * 2 + p) % len(moves)]
            frames = max(int(round(part_dur * fps)), 2)
            out = tmp / f"{s['slug']}_{p}.mp4"
            run([
                "ffmpeg", "-y", "-loop", "1", "-framerate", fps, "-i", str(img),
                "-t", f"{part_dur:.3f}",
                "-vf", move_filter(kind, frames, zps, w, h, fps),
                # Visually lossless throwaway intermediate — the final pass
                # does the real compression, so spend no time here.
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "14",
                str(out),
            ])
            piece_paths.append(out)

        # Join the moves, then marry the scene's own voice track to it.
        silent = tmp / f"{s['slug']}_v.mp4"
        if parts == 1:
            piece_paths[0].replace(silent)
        else:
            lst = tmp / f"{s['slug']}_parts.txt"
            lst.write_text("\n".join(f"file '{p.as_posix()}'" for p in piece_paths),
                           encoding="utf-8")
            run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                 "-c", "copy", str(silent)])

        seg = tmp / f"{s['slug']}.mp4"
        run([
            "ffmpeg", "-y", "-i", str(silent), "-i", str(voice),
            "-filter_complex",
            f"[1:a]apad=pad_dur=2,atrim=duration={dur:.3f},asetpts=PTS-STARTPTS[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-ar", "48000", "-ac", "2", "-shortest", str(seg),
        ])
        segments.append(seg)
        if (i + 1) % 10 == 0:
            log("assemble", f"{i + 1}/{len(scenes)} scenes rendered")

    listfile = tmp / "concat.txt"
    listfile.write_text("\n".join(f"file '{p.as_posix()}'" for p in segments),
                        encoding="utf-8")
    joined = tmp / "joined.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
         "-c", "copy", str(joined)])

    ass = (ep / "captions.ass").as_posix().replace(":", "\\:")
    # Grain then vignette then captions: the captions must stay clean, so they
    # are drawn after the film treatment, not under it.
    vfilter = f"noise=alls=5:allf=t,vignette=PI/5,subtitles='{ass}'"
    final = ep / "final.mp4"
    bed = next((p for p in sorted((ep.parent.parent / "assets" / "music").glob("*.mp3"))), None)

    base = ["ffmpeg", "-y", "-i", str(joined)]
    if bed:
        cmd = base + [
            "-stream_loop", "-1", "-i", str(bed),
            "-filter_complex",
            f"[0:v]{vfilter}[v];"
            f"[1:a]volume={aud['music_db']}dB[m];"
            f"[0:a][m]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=400[duck];"
            f"[0:a][duck]amix=inputs=2:duration=first:dropout_transition=0,"
            f"loudnorm=I={aud['target_lufs']}:TP=-1.5:LRA=11[a]",
            "-map", "[v]", "-map", "[a]", "-shortest",
        ]
    else:
        cmd = base + [
            "-vf", vfilter,
            "-af", f"loudnorm=I={aud['target_lufs']}:TP=-1.5:LRA=11",
        ]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "19",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", str(final)]
    run(cmd)

    if not args.keep_temp:
        shutil.rmtree(tmp, ignore_errors=True)

    total = probe_duration(final)
    log("assemble", f"{final}  {int(total // 60)}:{int(total % 60):02d}")


if __name__ == "__main__":
    main()
