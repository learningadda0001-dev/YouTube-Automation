# YouTube automation — daily Kannada history episodes

One 15–25 minute narrated Kannada video per day (target 20), written, voiced,
illustrated, assembled and uploaded without anyone at a keyboard. Runs on
GitHub Actions, so your PC does not need to be on.

## What it costs

Nothing for the content. One caveat on compute, below.

| Stage | Service | Free allowance | Used per episode |
|---|---|---|---|
| Script | Gemini API | free tier | 1 outline + 8 act calls |
| Images (first 50) | Cloudflare Workers AI, FLUX-1-schnell | 10,000 neurons/day ≈ 57 images | 50 |
| Images (rest) | Pollinations, keyless | no published cap | ~50 |
| Voice | edge-tts (Microsoft neural Kannada) | unlimited, no key | ~15,600 chars |
| Motion, captions, mixing | ffmpeg on the runner | — | — |
| Upload | YouTube Data API v3 | 10,000 quota units/day | 1,600 |
| Compute | GitHub Actions | 2,000 min/month **private** | ~95 min |

**A 20-minute episode needs ~100 images, and Cloudflare's free tier is ~57 a
day.** So the run is split: the first 50 come from Cloudflare, the rest from
Pollinations. Both are free. Change the split in `config/style.yaml` under
`visual.providers`.

**Compute does not fit the private-repo free tier.** About 95 minutes a run is
~2,900 minutes a month against 2,000 free. Options, cheapest first:

1. **Make the repo public** — Actions minutes are unlimited and free for public
   repos. Secrets stay secret; only the code is visible. This is the
   recommended fix and costs nothing.
2. Pay for the overage, roughly $7 a month.
3. Run a self-hosted runner on your own PC — free, but the PC must be on.
4. Drop `target_minutes` to about 13, which brings a month under 2,000.

## How it works

```
topics.csv ──pick──▶ write_script ──▶ parse ──▶ gen_voice ──▶ gen_images
                                                     │             │
                                                     ▼             ▼
                                              make_captions   make_thumbnail
                                                     └──────┬──────┘
                                                            ▼
                                                        assemble
                                                            ▼
                                                     upload ──▶ YouTube
```

Each scene is one generated still, held for exactly the length of its own
narration line, with a slow camera move applied in ffmpeg. Scenes longer than
nine seconds get two different moves on the same still, so the framing changes
every few seconds. Grain and a vignette go on top — a perfectly clean AI still
looks synthetic, a slightly noisy one reads as film.

The script is **not** written in one call. At 20 minutes that is ~15,600
Kannada characters across 100 scenes, and a single call drifts, loses count
and thins out badly after the first third. Instead `write_script.py` makes one
outline call that fixes the acts and the title, then one call per act, each
given the previous act's closing line so the narration joins up. Scene
numbering is forced sequential afterwards, because models miscount over
long runs.

## Setup

### 1. Secrets

GitHub → Settings → Secrets and variables → Actions:

| Secret | Where to get it |
|---|---|
| `GEMINI_API_KEY` | aistudio.google.com → Get API key |
| `CF_ACCOUNT_ID` | Cloudflare dashboard → Workers & Pages → right sidebar |
| `CF_API_TOKEN` | Cloudflare → My Profile → API Tokens → Workers AI template |
| `YT_CLIENT_ID` · `YT_CLIENT_SECRET` · `YT_REFRESH_TOKEN` | see below |
| `ANTHROPIC_API_KEY` | optional, only for `--provider anthropic` |
| `ELEVENLABS_API_KEY` · `ELEVENLABS_VOICE_ID` | optional, paid voice upgrade |

### 2. YouTube auth, once

In Google Cloud Console: enable **YouTube Data API v3**, create an **OAuth
client ID → Desktop app**, download `client_secret.json`. Then on your own
machine:

```bash
pip install -r requirements.txt
python src/auth_setup.py client_secret.json
```

It opens a browser, you approve, and it prints the three `YT_*` values to
paste into the secrets.

### 3. Music bed (optional but worth it)

Drop one royalty-free instrumental as `assets/music/bed.mp3`. It is ducked
under the voice automatically. Without it the video is voice only.

### 4. Kannada font for thumbnails

The workflow installs Noto on the runner. To render thumbnails locally too,
put `NotoSansKannada-Bold.ttf` in `assets/fonts/`.

## Running it

The schedule is 13:30 UTC — 19:00 IST — daily. To run it by hand, use
**Actions → Daily episode → Run workflow**, where you can force a topic id,
set privacy, or stop before upload to review first.

Locally:

```bash
python src/run_daily.py --stop-before upload     # build, do not publish
python src/run_daily.py --id 3                   # a specific topic
python src/run_daily.py --slug 2026-11-09-1 --from images   # resume
```

**Keep `privacy: private` in `config/style.yaml` for the first week.** Watch a
few finished episodes end to end before letting it publish on its own.

## The topic backlog

`config/topics.csv` is the queue. Highest `priority` among `status: pending`
goes next; the uploader flips it to `done` and writes the URL back.

Priority reflects what the research actually showed: **famous places people
already know outrank obscure history by two orders of magnitude.** On one
competing channel, Hampi took 460K views and Mysore Palace 93K, while the same
channel's Kadamba-dynasty and mythology episodes took 450–1,100 each. The list
is ordered accordingly. Resist the urge to promote a topic because it is
interesting — promote it because people already search for the place.

There are 120 topics here, about four months of daily output. Add more before
you run out, and keep the same bias.

## Changing the look

Everything visual lives in `config/style.yaml`: the style suffix appended to
every image prompt, camera-motion speed, caption font and size, music level,
voice. Change the style suffix and the whole channel changes with the next
episode.

## Known limits

- **edge-tts is unofficial.** It can break without warning. If it does, set
  `voice.provider: elevenlabs` or `google` in `style.yaml` and add that key.
- **FLUX-1-schnell is not Veo.** It is good at landscapes, architecture and
  wide shots, weaker at faces and hands. The prompts lean on wide and medium
  shots for that reason. Avoid prompts that put a face in close-up.
- **Faces drift between scenes.** There is no character reference in this
  stack, so a recurring person will not look identical across shots. Scripts
  should favour places, objects and crowds over one tracked individual.
- **Daily burns topics fast.** See the note above about the backlog.
- **20 minutes is a lot to fill honestly.** Some topics in the backlog cannot
  carry it without padding. The outline prompt is told to widen into context
  rather than repeat itself, but watch the first few: a thin 20-minute episode
  retains worse than a dense 10-minute one. If a topic will not stretch, drop
  `target_minutes` for that run rather than letting it waffle.
