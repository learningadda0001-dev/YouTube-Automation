"""Kannada voiceover, one file per scene.

Default provider is edge-tts, which is free and needs no key, using Microsoft's
neural Kannada voices. It is an unofficial client, so it can break without
notice — elevenlabs and google are wired up as paid fallbacks. Per-scene audio
is what lets each image be held for exactly as long as its own line.
"""
from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from common import EPISODES, cfg, env, load_scenes, log, probe_duration, save_scenes


async def _edge_one(text: str, out: Path, voice: str, rate: str, pitch: str) -> None:
    import edge_tts

    await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(str(out))


def edge(text: str, out: Path, c: dict) -> None:
    v = c["voice"]
    asyncio.run(_edge_one(text, out, v["edge_voice"], v["edge_rate"], v["edge_pitch"]))


def elevenlabs(text: str, out: Path, c: dict) -> None:
    import requests

    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{env('ELEVENLABS_VOICE_ID')}",
        headers={"xi-api-key": env("ELEVENLABS_API_KEY"),
                 "Content-Type": "application/json"},
        json={
            "text": text,
            "model_id": c["voice"]["elevenlabs_model"],
            "voice_settings": {"stability": 0.45, "similarity_boost": 0.80,
                               "style": 0.35, "use_speaker_boost": True,
                               "speed": 0.95},
        },
        timeout=180,
    )
    r.raise_for_status()
    out.write_bytes(r.content)


def google(text: str, out: Path, c: dict) -> None:
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()
    resp = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=text),
        voice=texttospeech.VoiceSelectionParams(
            language_code="kn-IN", name=c["voice"]["google_voice"]),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=0.95),
    )
    out.write_bytes(resp.audio_content)


PROVIDERS = {"edge": edge, "elevenlabs": elevenlabs, "google": google}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--provider", choices=list(PROVIDERS))
    args = ap.parse_args()

    c = cfg()
    provider = args.provider or c["voice"]["provider"]
    ep = EPISODES / args.slug
    audio = ep / "audio"
    audio.mkdir(exist_ok=True)
    scenes = load_scenes(ep)

    total = 0.0
    for s in scenes:
        out = audio / f"{s['slug']}.mp3"
        if not (out.exists() and out.stat().st_size > 2000):
            PROVIDERS[provider](s["narration"], out, c)
        s["audio_duration"] = probe_duration(out)
        if s["audio_duration"] < 0.5:
            raise SystemExit(f"{s['slug']}: audio is empty — TTS returned nothing")
        total += s["audio_duration"]

    save_scenes(ep, scenes)
    log("voice", f"{len(scenes)} lines via {provider}, "
                 f"total {int(total // 60)}:{int(total % 60):02d}")


if __name__ == "__main__":
    main()
