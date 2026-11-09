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


def move_filter(kind: str, frames: int, zps: float, w: int, h: int, fps: int,
                trim: float = 0.0) -> str:
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

    # Blur out the bottom-right corner before anything else. Generated images
    # sometimes carry a provider watermark there — Pollinations does, even
    # with nologo=true. Cropping it away would cost over 10% of every frame;
    # blurring a small patch costs nothing visible once the shot is moving.
    # Anchored top-left, so only the right and bottom edges are lost — the
    # two the mark sits on. Blurring the corner instead was tried and left a
    # visible rectangle edge; cropping leaves nothing behind. Aspect ratio is
    # unchanged, so nothing downstream has to care.
    keep = max(0.80, 1.0 - trim)
    edge = f"crop=iw*{keep:.4f}:ih*{keep:.4f}:0:0," if trim > 0 else ""

    # Scale-and-crop to cover 16:9, so a square image from a provider that
    # ignores width/height still fills the frame instead of pillarboxing.
    # Grain and vignette are deliberately NOT here — they go in the single
    # final encode, so each scene costs one cheap pass instead of two dear ones.
    return (
        f"{edge}"
        f"scale={PRESCALE}:{PRESCALE * h // w}:force_original_aspect_ratio=increase,"
        f"crop={PRESCALE}:{PRESCALE * h // w},setsar=1,"
        f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={w}x{h}:fps={fps},"
        f"format=yuv420p"
    )


def parallax_graph(kind: str, dur: float, w: int, h: int, trim: float,
                   near_gain: float) -> str:
    """A 2.5D camera move: foreground and background travel at different rates.

    This is what separates a moving photograph from a slideshow. The image is
    split into a near layer (masked by its depth map) and a far layer (the
    whole picture). Both crop-zoom and pan over the shot, the near one further
    and faster, so the frame gains real depth. Where the near layer moves
    away, the far layer shows through — with modest displacement the seam is
    not noticeable, and no inpainting is needed.

    Expressed entirely in crop expressions rather than zoompan, because
    zoompan does not carry an alpha channel and the near layer needs one.
    """
    keep = max(0.80, 1.0 - trim)
    bw, bh = int(w * 1.30), int(h * 1.30)

    frames = max(int(round(dur * 30)), 2)

    def layer(z0: float, z1: float, pan_x: float) -> str:
        """zoompan from z0 to z1 while drifting pan_x pixels across the shot.

        crop cannot do this: it evaluates w and h once at configure time, so
        only x and y animate. zoompan animates the zoom but discards alpha —
        hence running it on the picture and on the mask separately with
        identical parameters, and merging the alpha afterwards.
        """
        z = f"{z0:.4f}+({z1 - z0:.4f})*on/{frames}"
        x = f"iw/2-(iw/zoom/2)+({pan_x:.1f})*on/{frames}"
        y = "ih/2-(ih/zoom/2)"
        return (f"zoompan=z='{z}':x='{x}':y='{y}':"
                f"d={frames}:s={w}x{h}:fps=30")

    g = near_gain
    # The near layer always moves further than the far one — that difference
    # is the entire effect. Direction varies per shot so consecutive scenes
    # do not feel identical.
    if kind == "push_in":
        far, near = layer(1.00, 1.05, 0), layer(1.00, 1.14 * g, 0)
    elif kind == "pull_out":
        far, near = layer(1.05, 1.00, 0), layer(1.14 * g, 1.00, 0)
    elif kind == "pan_right":
        far, near = layer(1.02, 1.04, 14), layer(1.05, 1.09, 46 * g)
    else:  # pan_left
        far, near = layer(1.02, 1.04, -14), layer(1.05, 1.09, -46 * g)

    prep = (f"crop=iw*{keep:.4f}:ih*{keep:.4f}:0:0,"
            f"scale={bw}:{bh}:force_original_aspect_ratio=increase,"
            f"crop={bw}:{bh},setsar=1")

    graph = (
        f"[0:v]{prep}[big];"
        f"[1:v]crop=iw*{keep:.4f}:ih*{keep:.4f}:0:0,"
        f"scale={bw}:{bh}:force_original_aspect_ratio=increase,"
        f"crop={bw}:{bh},setsar=1[maskbig];"
        f"[big]split[farsrc][nearsrc];"
        f"[farsrc]{far}[far];"
        # The mask rides the SAME move as the near picture, so the cut-out
        # stays locked to the object it was cut from.
        f"[nearsrc]{near}[nearpix];"
        f"[maskbig]{near},format=gray[nearmask];"
        f"[nearpix]format=rgba[nearrgba];"
        f"[nearrgba][nearmask]alphamerge[near];"
        f"[far][near]overlay=0:0:format=auto,format=yuv420p[v]"
    )
    return graph


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--keep-temp", action="store_true")
    ap.add_argument("--preview", action="store_true",
                    help="also write a small 720p preview.mp4 for review")
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

        depth = ep / "depth" / f"{s.get('image', s['slug'])}.png"
        use_parallax = depth.exists() and vis.get("parallax", True)

        piece_paths = []
        for p in range(parts):
            kind = moves[(i * 2 + p) % len(moves)]
            frames = max(int(round(part_dur * fps)), 2)
            out = tmp / f"{s['slug']}_{p}.mp4"
            trim = float(vis.get("edge_trim", 0.0))

            if use_parallax:
                cmd = [
                    "ffmpeg", "-y",
                    "-loop", "1", "-framerate", fps, "-i", str(img),
                    "-loop", "1", "-framerate", fps, "-i", str(depth),
                    "-t", f"{part_dur:.3f}",
                    "-filter_complex",
                    parallax_graph(kind, part_dur, w, h, trim,
                                   float(vis.get("near_gain", 1.0))),
                    "-map", "[v]",
                ]
            else:
                cmd = [
                    "ffmpeg", "-y", "-loop", "1", "-framerate", fps,
                    "-i", str(img), "-t", f"{part_dur:.3f}",
                    "-vf", move_filter(kind, frames, zps, w, h, fps, trim),
                ]
            run(cmd + [
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
    grain = int(vis.get("grain", 2))
    treatment = f"noise=alls={grain}:allf=t," if grain > 0 else ""
    vfilter = f"{treatment}vignette=PI/5,subtitles='{ass}'"
    crf = str(vis.get("crf", 21))
    final = ep / "final.mp4"
    bed = next((p for p in sorted((ep.parent.parent / "assets" / "music").glob("*.mp3"))), None)

    if bed is None and aud.get("synth_bed"):
        # Bare voice over silence is a large part of why a stills episode
        # feels cheap. A sustained low drone with a slow swell sits under the
        # narration and reads as atmosphere rather than as music. Royalty
        # free by construction — it is generated, not sampled.
        bed = tmp.parent / "_bed.mp3"
        run([
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "sine=frequency=55:duration=120",
            "-f", "lavfi", "-i", "sine=frequency=82.5:duration=120",
            "-f", "lavfi", "-i", "sine=frequency=110:duration=120",
            "-f", "lavfi", "-i", "anoisesrc=d=120:c=brown:a=0.06",
            "-filter_complex",
            "[0:a]volume=0.5[a0];[1:a]volume=0.26[a1];[2:a]volume=0.15[a2];"
            "[3:a]lowpass=f=320,volume=0.5[a3];"
            "[a0][a1][a2][a3]amix=inputs=4:normalize=0,"
            "lowpass=f=900,"
            # Slow breathing swell, ~25s cycle, so it never sits still.
            # apulsator rather than tremolo: tremolo refuses below 0.1 Hz.
            "apulsator=hz=0.04:amount=0.35,"
            "aecho=0.8:0.9:180|420:0.35|0.22,"
            "volume=0.8",
            "-c:a", "libmp3lame", "-b:a", "160k", str(bed),
        ])
        log("assemble", "synthesised an ambient bed (no assets/music/*.mp3)")

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
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", crf,
            # A hard ceiling: random grain can otherwise push a long episode
            # into the gigabytes, which is slow to upload and buys nothing.
            "-maxrate", "9M", "-bufsize", "18M",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", str(final)]
    run(cmd)

    if not args.keep_temp:
        shutil.rmtree(tmp, ignore_errors=True)

    total = probe_duration(final)
    size_mb = final.stat().st_size / 1_000_000
    log("assemble", f"{final}  {int(total // 60)}:{int(total % 60):02d}  "
                    f"{size_mb:.0f}MB")

    if args.preview:
        prev = ep / "preview.mp4"
        run(["ffmpeg", "-y", "-i", str(final),
             "-vf", "scale=1280:720", "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "30", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
             "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2",
             str(prev)])
        log("assemble", f"{prev}  {prev.stat().st_size / 1_000_000:.0f}MB "
                        f"(720p review copy)")


if __name__ == "__main__":
    main()
