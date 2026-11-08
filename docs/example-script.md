# Episode 01 — ಬೆಂಗಳೂರು ಹುಟ್ಟಿದ ನಿಜವಾದ ಕಥೆ

**Target length:** 8:45–9:15 · **Language:** Kannada narration, burned-in Kannada captions
**Format reference:** Namma Savari "ಮೈಸೂರು ಹುಟ್ಟಿದ ಕಥೆ" (343K / 1 month)
**78 scenes · ~7,000 characters of narration**

---

## 1. Publishing metadata

**Title (primary):**
`ಬೆಂಗಳೂರು ಹುಟ್ಟಿದ ನಿಜವಾದ ಕಥೆ! 😱 | ಕೆಂಪೇಗೌಡರಿಗಿಂತ 650 ವರ್ಷ ಹಳೆಯ ರಹಸ್ಯ | Bengaluru History Kannada`

**Alternates for A/B after 48h:**
- `ಬೆಂಗಳೂರನ್ನು ಮೂರು ಲಕ್ಷಕ್ಕೆ ಮಾರಿದ್ದರು! 😱 | ಕೆಂಪೇಗೌಡರ ಕನಸಿನ ನಗರದ ಕಥೆ | Bangalore History`
- `ಒಂದು ಮೊಲ ಹುಟ್ಟಿಸಿದ ಮಹಾನಗರ! 😱 | ನಾಡಪ್ರಭು ಕೆಂಪೇಗೌಡರ ಇತಿಹಾಸ | Kempegowda Real Story`

**Thumbnail:** Left two-thirds — the 1537 mud fort gate at golden hour, a lone spearman. Right third — modern Bengaluru skyline, same camera height. Jagged split down the middle. Kannada text top-left, heavy yellow with black outline: **"890 ರಲ್ಲೇ ಬೆಂಗಳೂರು?"** plus a red-circled 😱. No face.

Description, tags and schedule live in `meta.json`.

---

## 2. Production spec

**Visual style suffix** — appended automatically by `parse_script.py`, so every shot grades alike:

```
cinematic film still, 16:9, shot on 35mm anamorphic, shallow depth of field,
warm earthy desaturated palette, dust motes in volumetric light, soft golden
hour haze, historically accurate 16th century South Indian (Karnataka) setting,
no text, no watermark, photorealistic
```

**Avoid:** modern clothing, Mughal or Rajasthani architecture and turbans, Hindi signage, cartoon or anime rendering, heavy lens flare, extra fingers.

**Motion:** 6–8s image-to-video per shot, slow push-in / slow drift / locked-off with ambient motion only. Fast camera moves expose AI artifacts.

**Character consistency:** keep one reference frame of Kempe Gowda and feed it back for scenes 19, 20, 24, 28, 31, 35, 49, 58, 62, 63, 64 — otherwise his face drifts across the video.

**Voice:** single male Kannada narrator, storyteller pace. ElevenLabs multilingual v2 — stability 0.45, similarity 0.80, style 0.35, speed 0.95. Google Chirp3-HD `kn-IN` as the cheaper fallback.

**Captions:** 2 lines max, centred, bottom 12%, Noto Sans Kannada Bold 54px, white on a 70%-opacity black bar, no outline.

**Audio bed:** tanpura-and-low-strings drone at −22 LUFS under the voice, swelling at scenes 6, 33, 57 and 74.

---

## 3. Script — 78 scenes

> `[K]` Kannada narration — read aloud, also the caption text. `[V]` visual prompt. `[S]` sound.

### HOOK — 0:00

**1.**
[K] ಪ್ರತಿದಿನ ಒಂದೂವರೆ ಕೋಟಿ ಜನ ಓಡಾಡುವ ನಗರ ಇದು. ಭಾರತದ ಸಿಲಿಕಾನ್ ವ್ಯಾಲಿ ಅಂತ ಜಗತ್ತೇ ಕರೆಯುವ ಊರು.
[V] Aerial at dusk over a dense modern South Indian megacity, endless lights, rivers of traffic, slow descent
[S] city hum rising

**2.**
[K] ಆದರೆ ಈ ಮಹಾನಗರ ಹುಟ್ಟಿದ್ದು ಒಂದು ಮೊಲದ ಧೈರ್ಯದಿಂದ ಅಂತ ನಿಮಗೆ ಗೊತ್ತಾ?
[V] Extreme close-up of a hare in dry grass, ears twitching, turning sharply toward camera, golden light
[S] music stops dead

**3.**
[K] ಕ್ರಿ.ಶ. 1537. ಒಬ್ಬ ಪಾಳೇಗಾರ ಈ ಬಂಜರು ನೆಲದಲ್ಲಿ ನಾಲ್ಕು ಜೋಡಿ ಎತ್ತುಗಳನ್ನು ಕಟ್ಟಿ ನೇಗಿಲು ಹೊಡೆದ. ಆ ನಾಲ್ಕು ಗೆರೆಗಳೇ ಇವತ್ತಿನ ಬೆಂಗಳೂರಿನ ಮೊದಲ ನಕ್ಷೆ.
[V] Four white bullocks dragging a wooden plough across bare red earth, 16th century chieftain walking behind, huge dust cloud, wide shot
[S] bullock bells, plough scraping earth

**4.**
[K] ಆದರೆ ಇಲ್ಲಿ ಒಂದು ದೊಡ್ಡ ಪ್ರಶ್ನೆ ಇದೆ. ಬೆಂಗಳೂರಿನಿಂದ ಕೇವಲ ಹದಿನೈದು ಕಿಲೋಮೀಟರ್ ದೂರದಲ್ಲಿರುವ ಬೇಗೂರಿನ ಒಂದು ಕಲ್ಲಿನ ಮೇಲೆ...
[V] Slow push-in on a weathered granite hero-stone set in an old temple wall, moss in the carved grooves, raking sunlight
[S] low drone sting

**5.**
[K] ...ಕ್ರಿ.ಶ. 890ರಲ್ಲೇ 'ಬೆಂಗಳೂರು' ಅನ್ನೋ ಹೆಸರು ಕೆತ್ತಲಾಗಿದೆ. ಅಂದರೆ ಕೆಂಪೇಗೌಡರು ಹುಟ್ಟುವುದಕ್ಕಿಂತ ಆರುನೂರ ಇಪ್ಪತ್ತು ವರ್ಷ ಮೊದಲೇ!
[V] Extreme close-up of ancient Kannada script carved in granite, focus racking across the letters, floating dust
[S] deep stone resonance

**6.**
[K] ಹಾಗಾದರೆ ಬೆಂಗಳೂರನ್ನು ಕಟ್ಟಿದವರು ಯಾರು? ಈ ನಗರದ ಹೆಸರು ಎಲ್ಲಿಂದ ಬಂತು? ಮತ್ತು ಈ ಊರನ್ನು ಒಮ್ಮೆ ಕೇವಲ ಮೂರು ಲಕ್ಷ ರೂಪಾಯಿಗೆ ಮಾರಿದ್ದು ಯಾರು? ಕೊನೆಯವರೆಗೂ ನೋಡಿ.
[V] Montage of the same patch of ground across eras — forest, mud fort, colonial street, glass towers — slow dissolves
[S] music swell

### ACT 1 — Where the name came from · 0:55

**7.**
[K] ಮೊದಲು ಆ ಹೆಸರಿನ ಕಥೆ. ಹನ್ನೆರಡನೇ ಶತಮಾನ. ಹೊಯ್ಸಳ ದೊರೆ ವೀರ ಬಲ್ಲಾಳ ಬೇಟೆಗೆ ಬಂದು ದಟ್ಟ ಕಾಡಿನಲ್ಲಿ ದಾರಿ ತಪ್ಪಿದ.
[V] 12th century Hoysala king alone on horseback in dense moonlit scrub forest, guttering torch, lost
[S] night forest, owl

**8.**
[K] ಹಸಿವು, ಕತ್ತಲೆ, ಯಾವ ದಿಕ್ಕೂ ಗೊತ್ತಿಲ್ಲ. ಗಂಟೆಗಟ್ಟಲೆ ಅಲೆದ ಮೇಲೆ ದೂರದಲ್ಲಿ ಒಂದು ಸಣ್ಣ ಬೆಳಕು ಕಾಣಿಸಿತು.
[V] Point of view through dark branches toward a single faint firelight in a clearing far away
[S] footsteps, wind

**9.**
[K] ಅದು ಒಂದು ಬಡ ಮುದುಕಿಯ ಗುಡಿಸಲು. ಅವಳ ಬಳಿ ಇದ್ದದ್ದು ಬೇಯಿಸಿದ ಅವರೆಕಾಳು ಮಾತ್ರ. ಅದನ್ನೇ ಅವಳು ಆ ಅಪರಿಚಿತನಿಗೆ ಬಡಿಸಿದಳು.
[V] Interior of a tiny thatched hut, old village woman ladling boiled beans onto a leaf plate for a weary nobleman, firelight only
[S] fire crackle

**10.**
[K] ಹಸಿವು ಇಂಗಿದ ದೊರೆ ಕೃತಜ್ಞತೆಯಿಂದ ಆ ಜಾಗಕ್ಕೆ 'ಬೆಂದ ಕಾಳೂರು' ಅಂತ ಹೆಸರಿಟ್ಟನಂತೆ. ಅದೇ ಮುಂದೆ ಬೆಂಗಳೂರು ಆಯಿತು ಅಂತ ಹೇಳುತ್ತಾರೆ.
[V] Close on steaming boiled beans on a leaf plate, hands lifting it, firelight, shallow focus
[S] —

**11.**
[K] ಈ ಕಥೆ ಕೇಳೋಕೆ ಎಷ್ಟು ಚೆನ್ನಾಗಿದೆ ಅಲ್ವಾ? ಆದರೆ ಇತಿಹಾಸಕಾರರು ಹೇಳೋದು ಬೇರೆಯೇ.
[V] The hut scene desaturating and flattening into a faded painted mural on a cracked wall
[S] music drops out

**12.**
[K] ಬೇಗೂರಿನ ನಾಗೇಶ್ವರ ದೇವಾಲಯದ ಆವರಣದಲ್ಲಿ ಒಂದು ವೀರಗಲ್ಲು ಇದೆ. ಅದರ ಮೇಲೆ ಹಳೆಗನ್ನಡದಲ್ಲಿ 'ಬೆಂಗಳೂರು ಕಾಳಗ' ಅನ್ನೋ ಉಲ್ಲೇಖ ಇದೆ.
[V] Old Dravidian stone temple at dawn, low granite walls, a carved hero-stone propped against it, mist
[S] distant temple bell

**13.**
[K] ಗಂಗ ದೊರೆಗಳ ಕಾಲದ ಆ ಶಾಸನ ಹೇಳೋದು ಇಷ್ಟು — ಇಲ್ಲಿ ಒಂದು ಊರು ಇತ್ತು, ಇಲ್ಲಿ ಒಂದು ಯುದ್ಧ ನಡೆದಿತ್ತು, ಮತ್ತು ಆ ಯುದ್ಧದಲ್ಲಿ ಒಬ್ಬ ವೀರ ಪ್ರಾಣ ಕೊಟ್ಟಿದ್ದ.
[V] Carved stone relief of ancient warriors fighting with spears, dramatic side light, slow pan across the carving
[S] low war drum

**14.**
[K] ಅಂದರೆ ಹೊಯ್ಸಳ ದೊರೆ ಹುಟ್ಟುವ ಮೂರು ನೂರು ವರ್ಷ ಮೊದಲೇ ಈ ಹೆಸರು ಇಲ್ಲಿ ಇತ್ತು. ಅವರೆಕಾಳಿನ ಕಥೆ ನಿಜವಾಗಿರೋಕೆ ಸಾಧ್ಯವೇ ಇಲ್ಲ.
[V] Timeline rendered as carved stone milestones receding into mist, closest one glowing
[S] single sustained note

**15.**
[K] ಬಹುಶಃ 'ಬೆಂಗಾವಲೂರು' — ಕಾವಲಿನ ಊರು. ಅಥವಾ 'ಬೆಂಗ' ಅನ್ನೋ ಹೂವಿನ ಮರಗಳ ಊರು. ಭಾಷಾ ತಜ್ಞರ ನಡುವೆ ಇವತ್ತಿಗೂ ಚರ್ಚೆ ಇದೆ.
[V] Dense grove of flowering trees with pale blossoms over an old stone path, wind moving the branches
[S] wind, leaves

**16.**
[K] ಒಂದಂತೂ ಖಚಿತ. ಕೆಂಪೇಗೌಡರು ಬೆಂಗಳೂರನ್ನು ಹುಟ್ಟಿಸಲಿಲ್ಲ. ಅವರು ಮಾಡಿದ್ದು ಇನ್ನೂ ದೊಡ್ಡ ಕೆಲಸ — ಇದ್ದ ಒಂದು ಹಳ್ಳಿಯನ್ನು ಅವರು ನಗರವಾಗಿ ಕಟ್ಟಿದರು.
[V] Silhouette of a 16th century South Indian chieftain on a rocky outcrop overlooking empty scrubland at sunrise, cape moving
[S] music returns, hopeful

### ACT 2 — Who he was · 2:00

**17.**
[K] ಯಲಹಂಕ. ಇವತ್ತು ಬೆಂಗಳೂರಿನ ಒಂದು ಬಡಾವಣೆ. ಆದರೆ ಐನೂರು ವರ್ಷಗಳ ಹಿಂದೆ ಅದು ವಿಜಯನಗರ ಸಾಮ್ರಾಜ್ಯದ ಅಡಿಯಲ್ಲಿದ್ದ ಒಂದು ಸಣ್ಣ ನಾಡು.
[V] Small 16th century fortified settlement on a plateau, mud walls, thatched roofs, wide establishing shot, morning haze
[S] village morning

**18.**
[K] ಅಲ್ಲಿನ ಪಾಳೇಗಾರರನ್ನು 'ಯಲಹಂಕ ನಾಡಪ್ರಭುಗಳು' ಅಂತ ಕರೆಯುತ್ತಿದ್ದರು. ಮೊರಸು ಒಕ್ಕಲಿಗ ಸಮುದಾಯದ ಈ ಮನೆತನ ತಲೆಮಾರುಗಳಿಂದ ಈ ಪ್ರದೇಶವನ್ನು ಆಳುತ್ತಿತ್ತು.
[V] Pillared audience hall of a modest South Indian chieftain's palace, stone floor, oil lamps, attendants waiting
[S] hall ambience

**19.**
[K] ಆ ಮನೆತನದಲ್ಲಿ ಸುಮಾರು 1510ರಲ್ಲಿ ಹುಟ್ಟಿದವನೇ ಹಿರಿಯ ಕೆಂಪೇಗೌಡ. ತಂದೆ ಕೆಂಪನಂಜೇಗೌಡ. ಬಾಲ್ಯದಿಂದಲೇ ಈತ ಕಂಡ ಕನಸು ಸಣ್ಣದಾಗಿರಲಿಲ್ಲ.
[V] Portrait of a dignified middle-aged South Indian chieftain, white dhoti, red-and-gold angavastra, simple turban, thick moustache, in a pillared hall
[S] —

**20.**
[K] ಐಗೊಂಡನಹಳ್ಳಿಯ ಗುರುಕುಲದಲ್ಲಿ ಒಂಬತ್ತು ವರ್ಷ ವಿದ್ಯಾಭ್ಯಾಸ. ಯುದ್ಧ ಕಲೆ, ಆಡಳಿತ, ಮತ್ತು ಮುಖ್ಯವಾಗಿ — ಊರು ಕಟ್ಟುವ ಕಲೆ.
[V] Young man training with a sword in a dusty courtyard at dawn while an older teacher watches, other students seated with palm-leaf manuscripts
[S] sword practice

**21.**
[K] ಅವನ ಕಾಲದಲ್ಲಿ ವಿಜಯನಗರ ಸಾಮ್ರಾಜ್ಯ ತನ್ನ ವೈಭವದ ತುತ್ತತುದಿಯಲ್ಲಿತ್ತು. ಹಂಪಿಯ ಬೀದಿಗಳಲ್ಲಿ ವಜ್ರ ವೈಡೂರ್ಯಗಳನ್ನು ಸೇರಿನಲ್ಲಿ ಅಳೆದು ಮಾರುತ್ತಿದ್ದರಂತೆ.
[V] Grand Vijayanagara bazaar street with stone colonnades, merchants with heaps of gems, elephants, crowds, golden light
[S] grand market, music lift

**22.**
[K] ಆ ವೈಭವವನ್ನು ಕಣ್ಣಾರೆ ಕಂಡ ಯುವಕ ಕೆಂಪೇಗೌಡನಿಗೆ ಒಂದು ಆಸೆ ಹುಟ್ಟಿತು. ತನ್ನ ನಾಡಲ್ಲೂ ಇಂಥದ್ದೇ ಒಂದು ವ್ಯಾಪಾರದ ನಗರ ಕಟ್ಟಬೇಕು ಅಂತ.
[V] Young chieftain standing amazed among the colonnades of a great imperial bazaar, looking up at the architecture
[S] —

**23.**
[K] ಆದರೆ ಯಲಹಂಕ ಸಣ್ಣದಾಗಿತ್ತು. ಬೆಳೆಯಲು ಜಾಗ ಇರಲಿಲ್ಲ. ಹೊಸ ನಗರಕ್ಕೆ ಹೊಸ ನೆಲ ಬೇಕಿತ್ತು.
[V] Aerial of a cramped small settlement hemmed in by rocky hills, limited flat land
[S] —

**24.**
[K] ಒಂದು ದಿನ ಬೇಟೆಗೆ ಹೋದಾಗ, ತನ್ನ ಮಂತ್ರಿ ವೀರಣ್ಣನ ಜೊತೆ ದಕ್ಷಿಣಕ್ಕೆ ಸಾಗಿದಾಗ, ಅವನಿಗೆ ಒಂದು ವಿಚಿತ್ರ ದೃಶ್ಯ ಕಂಡಿತಂತೆ.
[V] Hunting party of 16th century South Indian men with dogs and spears moving through dry scrub, long lens, heat shimmer
[S] dogs, footsteps

**25.**
[K] ಅವನ ಬೇಟೆ ನಾಯಿಯ ಹಿಂದೆ ಒಂದು ಮೊಲ ಓಡಿ ಬರುತ್ತಿತ್ತು! ಬೇಟೆಯಾಡಬೇಕಾದ ನಾಯಿಯೇ ಓಡಿ ಹೋಗುತ್ತಿತ್ತು.
[V] A hare turning and chasing a startled hunting dog across open ground, dust, slow motion, low camera
[S] music stop, then sting

**26.**
[K] ಮೊಲ ನಾಯಿಯನ್ನೇ ಅಟ್ಟಿಸಿಕೊಂಡು ಹೋಗೋದು 'ಗಂಡುಭೂಮಿ'ಯ ಲಕ್ಷಣ ಅನ್ನೋದು ಆಗಿನ ನಂಬಿಕೆ. ಈ ನೆಲದಲ್ಲಿ ಕಟ್ಟಿದ್ದು ಎಂದೂ ಸೋಲುವುದಿಲ್ಲ ಅಂತ.
[V] The chieftain reining in his horse, staring at the ground in astonishment, his men behind him, golden dust
[S] —

### ACT 3 — 1537 · 3:10

**27.**
[K] ಆ ಕ್ಷಣದಲ್ಲೇ ಕೆಂಪೇಗೌಡ ನಿರ್ಧಾರ ಮಾಡಿದ. ತನ್ನ ಕನಸಿನ ನಗರ ಇಲ್ಲೇ ಏಳಬೇಕು.
[V] Wide shot of empty red-earth plateau at sunset, a single figure standing centre, enormous sky
[S] wind, swell

**28.**
[K] ಆದರೆ ಅದು ಅಷ್ಟು ಸುಲಭ ಇರಲಿಲ್ಲ. ಹೊಸ ನಗರ ಕಟ್ಟಬೇಕಾದರೆ ವಿಜಯನಗರದ ಚಕ್ರವರ್ತಿಯ ಅನುಮತಿ ಬೇಕು.
[V] Chieftain kneeling before an imperial throne in a vast pillared hall, courtiers watching, shafts of light
[S] court ambience

**29.**
[K] ಅನುಮತಿ ಸಿಕ್ಕಿತು. ಜೊತೆಗೆ ಬೊಕ್ಕಸದಿಂದ ಹಣವೂ ಸಿಕ್ಕಿತು ಅಂತ ಕೆಲವು ದಾಖಲೆಗಳು ಹೇಳುತ್ತವೆ.
[V] Hands counting gold coins into a cloth bag on a stone table, torchlight, close-up
[S] coins

**30.**
[K] ಕ್ರಿ.ಶ. 1537. ಶುಭ ಮುಹೂರ್ತ ನೋಡಲಾಯಿತು. ನಾಲ್ಕು ಜೋಡಿ ಬಿಳಿ ಎತ್ತುಗಳನ್ನು ಹೂವಿನ ಹಾರ ಹಾಕಿ ಸಿದ್ಧಪಡಿಸಲಾಯಿತು.
[V] Dawn ceremony, priests with brass lamps, garlanded white bullocks yoked to ploughs, crowd of villagers, incense smoke
[S] conch, nadaswaram, chanting

**31.**
[K] ಒಂದೇ ಕೇಂದ್ರ ಬಿಂದುವಿನಿಂದ ನಾಲ್ಕು ದಿಕ್ಕಿಗೂ ನೇಗಿಲು ಹೊಡೆಯಲಾಯಿತು. ಪೂರ್ವ, ಪಶ್ಚಿಮ, ಉತ್ತರ, ದಕ್ಷಿಣ.
[V] Top-down aerial of four plough teams moving outward from one point in four directions, cutting four straight furrows into red earth
[S] music peak

**32.**
[K] ಆ ನಾಲ್ಕು ಗೆರೆಗಳೇ ಹೊಸ ನಗರದ ಎರಡು ಮುಖ್ಯ ರಸ್ತೆಗಳು. ಇವತ್ತಿಗೂ ಅವೇ ರಸ್ತೆಗಳು ಅಲ್ಲಿವೆ — ಚಿಕ್ಕಪೇಟೆ ರಸ್ತೆ ಮತ್ತು ದೊಡ್ಡಪೇಟೆ ರಸ್ತೆ.
[V] Two long straight streets crossing at right angles in a 16th century town, seen from above, bustling with carts
[S] —

**33.**
[K] ಅವು ಸೇರುವ ಜಾಗಕ್ಕೆ 'ದೊಡ್ಡಪೇಟೆ ಚೌಕ' ಅಂತ ಹೆಸರು. ಇವತ್ತು ಅದನ್ನು ನಾವು ಅವೆನ್ಯೂ ರಸ್ತೆ ಅಂತ ಕರೆಯುತ್ತೇವೆ.
[V] Match cut from the 16th century crossroads to the same crossing as a packed modern Indian commercial street
[S] hard cut to modern street noise

**34.**
[K] ಮಧ್ಯದಲ್ಲಿ ಮಣ್ಣಿನ ಕೋಟೆ ಎದ್ದಿತು. ಸುತ್ತಲೂ ಆಳವಾದ ಕಂದಕ. ಮತ್ತು ಒಟ್ಟು ಒಂಬತ್ತು ಬಾಗಿಲುಗಳು.
[V] Construction of a large oval mud-and-stone fort, hundreds of labourers carrying baskets of earth, scaffolding, dust haze
[S] construction, crowd

**35.**
[K] ಆ ಬಾಗಿಲುಗಳಿಗೆ ಹೆಸರಿಟ್ಟಿದ್ದು ಬಹಳ ಜಾಣತನದಿಂದ. ಯಾವ ಊರಿಗೆ ದಾರಿ ಹೋಗುತ್ತೋ ಆ ಊರಿನ ಹೆಸರೇ ಆ ಬಾಗಿಲಿಗೆ.
[V] Heavy timber-and-iron fort gate standing open, two spearmen on guard, bullock cart passing through, warm backlight
[S] cart wheels, crowd

**36.**
[K] ಯಲಹಂಕ ಬಾಗಿಲು, ಹಲಸೂರು ಬಾಗಿಲು, ಆನೇಕಲ್ ಬಾಗಿಲು, ಕೆಂಗೇರಿ ಬಾಗಿಲು, ಸರ್ಜಾಪುರ ಬಾಗಿಲು, ಬೇಗೂರು ಬಾಗಿಲು, ವರ್ತೂರು ಬಾಗಿಲು.
[V] Series of quick shots of different fort gateways in different light, each with guards and travellers
[S] seven soft hits

**37.**
[K] ಈ ಹೆಸರುಗಳನ್ನು ಗಮನಿಸಿ. ಐನೂರು ವರ್ಷ ಕಳೆದರೂ ಅವೆಲ್ಲ ಇವತ್ತಿಗೂ ಬೆಂಗಳೂರಿನ ಬಡಾವಣೆಗಳ ಹೆಸರುಗಳೇ ಆಗಿವೆ.
[V] Modern Bengaluru street-name boards in Kannada at different junctions, traffic blurring past, shallow focus
[S] traffic

**38.**
[K] ಕೋಟೆಯ ಗೋಡೆ ಮಣ್ಣಿನದಾಗಿತ್ತು. ಆದರೆ ಅದರ ಒಳಗಿನ ಯೋಜನೆ ಮಾತ್ರ ಕಲ್ಲಿನಷ್ಟು ಗಟ್ಟಿಯಾಗಿತ್ತು.
[V] Cross-section style wide shot of the completed fort at dusk, walls, moat, gates, lit interior streets
[S] music settles

**39.**
[K] ಕೆಂಪೇಗೌಡ ಕೇವಲ ಒಂದು ಕೋಟೆ ಕಟ್ಟಲಿಲ್ಲ. ಅವನು ಒಂದು ವ್ಯವಸ್ಥೆಯನ್ನು ಕಟ್ಟಿದ.
[V] Unrolled cloth city plan on a stone table, weights at the corners, a hand tracing the streets, lamplight
[S] —

**40.**
[K] ಮತ್ತು ಆ ವ್ಯವಸ್ಥೆಯನ್ನು ನೋಡಿದರೆ ಇವತ್ತಿನ ನಗರ ಯೋಜಕರೂ ತಲೆದೂಗಬೇಕು.
[V] Overhead of a planned 16th century market town — straight intersecting streets, uniform tiled roofs, a central square
[S] —

### ACT 4 — The petes · 4:30

**41.**
[K] ಅವನು ಮಾಡಿದ್ದು ಇಷ್ಟು. ಪ್ರತಿಯೊಂದು ವೃತ್ತಿಗೂ ಒಂದೊಂದು ಪ್ರತ್ಯೇಕ ಬೀದಿ. ಅದಕ್ಕೆ 'ಪೇಟೆ' ಅಂತ ಹೆಸರು.
[V] Busy 16th century bazaar street, bolts of cloth, traders haggling, shafts of sunlight through awnings
[S] market ambience

**42.**
[K] ಚಿಕ್ಕಪೇಟೆ ಬಟ್ಟೆ ವ್ಯಾಪಾರಕ್ಕೆ. ಬಳೇಪೇಟೆ ಬಳೆ ತಯಾರಕರಿಗೆ. ಅಕ್ಕಿಪೇಟೆ ಅಕ್ಕಿಗೆ. ರಾಗಿಪೇಟೆ ರಾಗಿಗೆ.
[V] Four quick shots — stacked cloth bolts, glass bangles glinting, sacks of rice, heaps of millet — all in warm market light
[S] four market stings

**43.**
[K] ಕುಂಬಾರಪೇಟೆ ಮಡಿಕೆಗೆ. ತರಗುಪೇಟೆ ಧಾನ್ಯಕ್ಕೆ. ಕಬ್ಬಣಪೇಟೆ ಕಮ್ಮಾರರಿಗೆ. ಅರಳೇಪೇಟೆ ಹತ್ತಿಗೆ.
[V] Four more — a potter at his wheel, grain sacks, a blacksmith's forge, raw cotton bales
[S] pottery wheel, forge hammer

**44.**
[K] ಒಂದೇ ವೃತ್ತಿಯವರೆಲ್ಲ ಒಂದೇ ಕಡೆ. ಗ್ರಾಹಕನಿಗೆ ಹುಡುಕುವ ಕಷ್ಟವಿಲ್ಲ, ವ್ಯಾಪಾರಿಗೆ ಸ್ಪರ್ಧೆಯಿಂದ ಬೆಲೆ ನಿಯಂತ್ರಣ.
[V] Overhead of a market street where every shop sells the same goods, customers moving between them
[S] crowd

**45.**
[K] ಇವತ್ತು ನಾವು ಇದನ್ನೇ 'ಕ್ಲಸ್ಟರ್ ಎಕಾನಮಿ' ಅಂತ ಕರೆಯುತ್ತೇವೆ. ಕೆಂಪೇಗೌಡ ಇದನ್ನು ಐನೂರು ವರ್ಷಗಳ ಹಿಂದೆಯೇ ಮಾಡಿದ್ದ.
[V] Split-feel shot: a historic trade lane dissolving into a modern wholesale market lane with identical shops
[S] —

**46.**
[K] ಬೇರೆ ಬೇರೆ ಊರುಗಳಿಂದ ವ್ಯಾಪಾರಿಗಳನ್ನು ಕರೆಸಿ ಇಲ್ಲಿ ನೆಲೆಸಲು ಜಾಗ ಕೊಟ್ಟ. ತೆರಿಗೆ ವಿನಾಯಿತಿ ಕೊಟ್ಟ.
[V] Caravan of merchants with loaded bullock carts and camels arriving at a fort gate at dawn
[S] caravan, bells

**47.**
[K] ಕೆಲವೇ ವರ್ಷಗಳಲ್ಲಿ ಬರಿದಾದ ಆ ಬಂಜರು ನೆಲ ದಕ್ಷಿಣ ಭಾರತದ ಒಂದು ಪ್ರಮುಖ ವ್ಯಾಪಾರ ಕೇಂದ್ರವಾಯಿತು.
[V] Thriving fort town at golden hour from above, smoke from kitchens, packed streets, carts at every gate
[S] music lift

**48.**
[K] ಐನೂರು ವರ್ಷ ಕಳೆದಿವೆ. ಇವತ್ತಿಗೂ ಚಿಕ್ಕಪೇಟೆಯಲ್ಲಿ ಬಟ್ಟೆ ಸಿಗುತ್ತೆ, ಬಳೇಪೇಟೆಯಲ್ಲಿ ಬಳೆ ಸಿಗುತ್ತೆ. ಅದೇ ಜಾಗ, ಅದೇ ವ್ಯಾಪಾರ.
[V] Modern crowded Chickpet-style wholesale cloth lane, shop boards in Kannada, scooters, bright fabrics
[S] modern market noise

### ACT 5 — Water · 5:25

**49.**
[K] ಆದರೆ ಕೆಂಪೇಗೌಡನ ಮುಂದೆ ಒಂದು ದೊಡ್ಡ ಸಮಸ್ಯೆ ಇತ್ತು. ಬಹುಶಃ ಅವನು ಎದುರಿಸಿದ ಅತಿ ದೊಡ್ಡ ಸವಾಲು.
[V] The chieftain alone at night on the fort wall, looking out, oil lamp, worried
[S] music drops

**50.**
[K] ಬೆಂಗಳೂರಿಗೆ ನದಿಯೇ ಇಲ್ಲ. ಒಂದೂ ಇಲ್ಲ. ಇದು ಸಮುದ್ರ ಮಟ್ಟದಿಂದ ಮೂರು ಸಾವಿರ ಅಡಿ ಎತ್ತರದ ಒಣ ಬಂಡೆ ನೆಲ.
[V] Vast dry rocky plateau, cracked earth, scattered granite boulders, no water anywhere, harsh noon light
[S] dry wind

**51.**
[K] ಮಳೆ ಬಿದ್ದರೆ ನೀರು ಇಳಿಜಾರಿನಲ್ಲಿ ಹರಿದು ಹೋಗುತ್ತಿತ್ತು. ನೀರಿಲ್ಲದ ಜಾಗದಲ್ಲಿ ನಗರ ಹೇಗೆ ಬದುಕುತ್ತೆ?
[V] Rainwater running fast down bare rock and away into a gully, nothing retaining it
[S] rushing water

**52.**
[K] ಅವನು ಕೊಟ್ಟ ಉತ್ತರ ಇವತ್ತಿಗೂ ಬೆರಗು ಹುಟ್ಟಿಸುತ್ತೆ. ಕೆರೆಗಳು. ಒಂದಲ್ಲ, ಎರಡಲ್ಲ — ನೂರಾರು ಕೆರೆಗಳು.
[V] Aerial of many interconnected man-made tanks across a landscape at golden hour, water catching light like a chain of mirrors
[S] music returns, water

**53.**
[K] ಧರ್ಮಾಂಬುಧಿ, ಕೆಂಪಾಂಬುಧಿ, ಸಂಪಂಗಿ, ಸಿದ್ದಿಕಟ್ಟೆ, ಹಲಸೂರು — ಪ್ರತಿ ಕಣಿವೆಯಲ್ಲೂ ಒಂದು ಕಟ್ಟೆ.
[V] Large stone-edged temple tank at dusk, steps going down into still water, lamps on the far bank
[S] water, birds

**54.**
[K] ಆದರೆ ನಿಜವಾದ ಜಾಣತನ ಇರೋದು ಅವುಗಳ ಜೋಡಣೆಯಲ್ಲಿ. ಒಂದು ಕೆರೆ ತುಂಬಿದರೆ ಅದರ ಹೆಚ್ಚುವರಿ ನೀರು ಕಾಲುವೆಯ ಮೂಲಕ ಮುಂದಿನ ಕೆರೆಗೆ.
[V] Stone sluice gate overflowing, water cascading down a channel toward a lower tank, lotus leaves, evening light
[S] flowing water

**55.**
[K] ಇಳಿಜಾರು ನೋಡಿ ಸರಪಳಿಯಂತೆ ಕಟ್ಟಿದ ಈ ವ್ಯವಸ್ಥೆಯಲ್ಲಿ ಒಂದು ಹನಿ ಮಳೆ ನೀರೂ ವ್ಯರ್ಥವಾಗುತ್ತಿರಲಿಲ್ಲ.
[V] Monsoon rain over the tank chain, aerial, water filling each tank in sequence, dark clouds
[S] heavy rain

**56.**
[K] ಇವತ್ತು ಧರ್ಮಾಂಬುಧಿ ಕೆರೆ ಇದ್ದ ಜಾಗದಲ್ಲಿ ಮೆಜೆಸ್ಟಿಕ್ ಬಸ್ ನಿಲ್ದಾಣ ಇದೆ. ಸಂಪಂಗಿ ಕೆರೆಯ ಮೇಲೆ ಕಂಠೀರವ ಕ್ರೀಡಾಂಗಣ ನಿಂತಿದೆ.
[V] Dissolve from a calm tank at dusk to a vast concrete bus terminus full of buses at the same camera angle
[S] hard cut, horns

**57.**
[K] ಐದು ಶತಮಾನಗಳ ಹಿಂದೆ ಎಲ್ಲರಿಗೂ ನೀರು ಕೊಟ್ಟ ನಗರ, ಇವತ್ತು ಟ್ಯಾಂಕರ್‌ಗಾಗಿ ಸಾಲಿನಲ್ಲಿ ಕಾಯುತ್ತಿದೆ.
[V] Modern Indian street, people queuing with plastic pots beside a water tanker, hot afternoon
[S] street, pots clanging

### ACT 6 — The arrest · 6:15

**58.**
[K] ನೀರು ಬಂತು, ವ್ಯಾಪಾರ ಬಂತು, ಜನ ಬಂದರು. ಕೆಂಪೇಗೌಡ ದೇವಾಲಯಗಳನ್ನೂ ಕಟ್ಟಿಸಿದ.
[V] Stone temple under construction, sculptors carving pillars, pulleys and ropes, morning light
[S] chisel on stone

**59.**
[K] ಗವಿಪುರದ ಗವಿ ಗಂಗಾಧರೇಶ್ವರ ದೇವಾಲಯ. ಬಸವನಗುಡಿಯ ದೊಡ್ಡ ಬಸವಣ್ಣ. ಹಲಸೂರಿನ ಸೋಮೇಶ್ವರ.
[V] Three quick shots — a cave temple entrance in rock, a huge monolithic stone bull in a pillared hall, a Dravidian temple tower
[S] temple bells

**60.**
[K] ಇವತ್ತಿಗೂ ಮಕರ ಸಂಕ್ರಾಂತಿಯಂದು ಗವಿ ಗಂಗಾಧರೇಶ್ವರ ದೇವಾಲಯದ ಒಳಗೆ ಸೂರ್ಯನ ಕಿರಣ ನೇರವಾಗಿ ಲಿಂಗದ ಮೇಲೆ ಬೀಳುತ್ತೆ.
[V] Shaft of sunlight entering a dark rock-cut shrine and striking the stone lingam, dust in the beam
[S] single bell, reverb

**61.**
[K] ನಗರ ಬೆಳೆಯಿತು. ಕೀರ್ತಿ ಬೆಳೆಯಿತು. ಮತ್ತು ಅದೇ ಕೆಂಪೇಗೌಡನಿಗೆ ಮುಳುವಾಯಿತು.
[V] Prosperous fort town from above at dusk, hundreds of lamps lighting up one by one
[S] ominous low note

**62.**
[K] ಐತಿಹ್ಯದ ಪ್ರಕಾರ, ಕೆಂಪೇಗೌಡ ತನ್ನದೇ ಹೆಸರಿನ ನಾಣ್ಯಗಳನ್ನು ಟಂಕಿಸಲು ಶುರು ಮಾಡಿದ.
[V] Close-up of a mint — hammer striking a hot gold coin blank on an anvil, sparks, dark workshop
[S] hammer strikes

**63.**
[K] ಆ ಕಾಲದಲ್ಲಿ ಸ್ವಂತ ನಾಣ್ಯ ಟಂಕಿಸೋದು ಅಂದರೆ ಸ್ವತಂತ್ರ ರಾಜನಾಗುವ ಘೋಷಣೆ. ವಿಜಯನಗರದ ದೊರೆಗೆ ಇದು ದಂಗೆಯಾಗಿ ಕಾಣಿಸಿತು.
[V] Grand Vijayanagara royal court, emperor on throne examining a coin, courtiers, deep shadows, torchlight
[S] court murmur

**64.**
[K] ಆದೇಶ ಬಂತು. ಬೆಂಗಳೂರನ್ನು ಕಟ್ಟಿದ ಆ ಮನುಷ್ಯನನ್ನೇ ಬಂಧಿಸಲಾಯಿತು. ಐದು ವರ್ಷ ಸೆರೆಮನೆ.
[V] Soldiers escorting the chieftain away from his own fort gate, hands bound, villagers watching silently, rain beginning
[S] music sting, rain

**65.**
[K] ತಾನು ಕಟ್ಟಿದ ನಗರವನ್ನು ನೋಡಲಾಗದ ಐದು ವರ್ಷ. ಕೊನೆಗೆ ಕಪ್ಪ ಕೊಟ್ಟು ಬಿಡುಗಡೆ ಸಿಕ್ಕಿತು ಅಂತ ಹೇಳುತ್ತಾರೆ.
[V] Stone cell, a single barred window, aged man sitting against the wall in one shaft of light, dust
[S] silence, dripping

**66.**
[K] ಹಿಂದಿರುಗಿದ ಕೆಂಪೇಗೌಡ ಮೊದಲಿನವನಾಗಿರಲಿಲ್ಲ. 1569ರಲ್ಲಿ ಅವನು ಕಣ್ಮುಚ್ಚಿದ. ಮಾಗಡಿಯ ಬಳಿ ಕೆಂಪಾಪುರದಲ್ಲಿ ಇವತ್ತಿಗೂ ಅವನ ಸಮಾಧಿ ಇದೆ.
[V] Simple old stone memorial structure in a quiet village field at dawn, mist, a lone lamp burning
[S] temple bell

### ACT 7 — The four towers · 7:20

**67.**
[K] ಅವನ ಮಗ ಇಮ್ಮಡಿ ಕೆಂಪೇಗೌಡ ತಂದೆಯ ಕನಸನ್ನು ಮುಂದುವರಿಸಿದ. ಮತ್ತು ಒಂದು ವಿಚಿತ್ರ ಕೆಲಸ ಮಾಡಿದ.
[V] Younger chieftain unrolling a cloth city plan on a stone table, advisors around him, lamplight
[S] music lifts

**68.**
[K] ನಗರದ ನಾಲ್ಕು ದಿಕ್ಕಿನಲ್ಲಿ ನಾಲ್ಕು ಕಲ್ಲಿನ ಗೋಪುರಗಳನ್ನು ಕಟ್ಟಿಸಿದ.
[V] Stone watchtower being built on top of a huge granite boulder, workers hauling blocks, wide shot, blue sky
[S] stone work

**69.**
[K] ಲಾಲ್‌ಬಾಗ್‌ನ ಬಂಡೆಯ ಮೇಲೆ ಒಂದು, ಹಲಸೂರಿನಲ್ಲಿ ಒಂದು, ಕೆಂಪಾಂಬುಧಿ ಕೆರೆಯ ಬಳಿ ಒಂದು, ಮೇಖ್ರಿ ವೃತ್ತದ ಹತ್ತಿರ ಒಂದು.
[V] Four quick shots of the same squat stone tower in four different settings — boulder, lakeside, grove, hilltop — golden hour
[S] four soft hits

**70.**
[K] ಅವು ಕಾವಲು ಗೋಪುರಗಳಲ್ಲ. ಅವು ಗಡಿಗಲ್ಲುಗಳು. "ಬೆಂಗಳೂರು ಇಷ್ಟು ಮಾತ್ರ ಬೆಳೆಯಲಿ" ಅನ್ನೋ ಸಂದೇಶ.
[V] Aerial at dusk showing four tiny towers marking the corners of a compact walled town
[S] —

**71.**
[K] ಇವತ್ತು ಆ ನಾಲ್ಕು ಗೋಪುರಗಳ ನಡುವಿನ ಜಾಗ ಬೆಂಗಳೂರಿನ ಕೇವಲ ಇಪ್ಪತ್ತನೇ ಒಂದು ಭಾಗ ಮಾತ್ರ.
[V] Same aerial dissolving into a vast modern megacity sprawling far past those four points, night lights
[S] big swell

**72.**
[K] ಇನ್ನೊಂದು ಕಥೆಯೂ ಇದೆ. ಕೋಟೆಯ ದಕ್ಷಿಣ ಬಾಗಿಲು ಕಟ್ಟಿದಷ್ಟೂ ಕುಸಿಯುತ್ತಿತ್ತಂತೆ. ಯಾವ ಉಪಾಯವೂ ಫಲಿಸಲಿಲ್ಲ.
[V] Half-built stone gateway collapsing in a cloud of dust, workers scattering, dusk
[S] rumble, collapse

**73.**
[K] ಐತಿಹ್ಯದ ಪ್ರಕಾರ, ಕೆಂಪೇಗೌಡರ ಸೊಸೆ ಲಕ್ಷ್ಮಮ್ಮ ನಗರಕ್ಕಾಗಿ ತನ್ನ ಪ್ರಾಣವನ್ನೇ ಅರ್ಪಿಸಿದಳು. ಆ ನಂತರ ಆ ಬಾಗಿಲು ಮತ್ತೆ ಕುಸಿಯಲಿಲ್ಲ.
[V] Silhouette of a young woman in a traditional sari walking alone toward a dark gateway at night, oil lamp in hand, back to camera
[S] single sustained note

### CLOSE — 8:15

**74.**
[K] ಒಂದು ಮಣ್ಣಿನ ಕೋಟೆ, ಒಂಬತ್ತು ಬಾಗಿಲು, ಹಲವು ಪೇಟೆ, ನೂರಾರು ಕೆರೆ. ಒಬ್ಬ ಪಾಳೇಗಾರನ ಕನಸು.
[V] Slow aerial orbit around the complete 16th century fort town at golden hour, smoke from kitchens, tiny figures
[S] music builds

**75.**
[K] ಅಲ್ಲಿಂದ ಇವತ್ತಿನ ಒಂದೂವರೆ ಕೋಟಿ ಜನರ ಮಹಾನಗರದವರೆಗೆ. ಕೆಂಪೇಗೌಡ ಕಟ್ಟಿದ್ದು ಕೇವಲ ಕೋಟೆಯಲ್ಲ, ಒಂದು ಯೋಜನೆ.
[V] Same orbit dissolving into the modern Bengaluru skyline at golden hour, glass towers, flyovers
[S] peak

**76.**
[K] ಆದರೆ ಈ ಕಥೆ ಇಲ್ಲಿಗೇ ಮುಗಿಯಲ್ಲ. ಕೆಂಪೇಗೌಡರ ಕುಟುಂಬದ ಕೈಯಿಂದ ಈ ನಗರ ಜಾರಿ ಹೋಯಿತು.
[V] Empty throne-like stone seat in a darkened hall, dust, a single shaft of light
[S] music darkens

**77.**
[K] ಮುಂದೆ ಬಿಜಾಪುರದ ಸುಲ್ತಾನರು ಬಂದರು, ಮರಾಠರು ಬಂದರು, ಮೊಘಲರು ಬಂದರು. ಮತ್ತು 1687ರಲ್ಲಿ ಮೈಸೂರಿನ ಒಡೆಯರು ಈ ಇಡೀ ನಗರವನ್ನು ಮೂರು ಲಕ್ಷ ರೂಪಾಯಿಗೆ ಖರೀದಿಸಿದರು.
[V] Hands exchanging a sealed document and heavy bags of coins across a table, two sets of 17th century robes, candlelight
[S] coins, ominous

**78.**
[K] ಆಮೇಲೆ ಬಂದವರು ಹೈದರ್ ಅಲಿ ಮತ್ತು ಟಿಪ್ಪು ಸುಲ್ತಾನ್. ಮತ್ತು 1791ರಲ್ಲಿ ಬ್ರಿಟಿಷರ ಫಿರಂಗಿಗಳು ಈ ಕೋಟೆಯ ಬಾಗಿಲನ್ನು ಒಡೆದವು. ಆ ಕಥೆ ಮುಂದಿನ ಭಾಗದಲ್ಲಿ. ಚಾನೆಲ್ ಸಬ್‌ಸ್ಕ್ರೈಬ್ ಮಾಡಿ.
[V] Cannon firing at a fort wall at night, stone exploding, smoke, freeze on the breach
[S] cannon, cut to silence

---

## 4. Accuracy notes

These framings are what keep the comments section friendly. Do not drop them.

- **Begur inscription (c. 890 CE, Western Ganga period)** genuinely records a "Bengaluru war." This is the factual spine — state it as fact.
- **ಬೆಂದಕಾಳೂರು / Veera Ballala** is folklore. Scenes 11 and 14 explicitly mark it as a story and give the chronological reason it cannot be the origin. Keep both.
- **The hare chasing the dog** is traditional account — scene 24 ends in "ಕಂಡಿತಂತೆ." Keep the ಅಂತೆ.
- **The imprisonment** is from traditional accounts — scene 62 opens with "ಐತಿಹ್ಯದ ಪ್ರಕಾರ," scene 65 ends with "ಅಂತ ಹೇಳುತ್ತಾರೆ." Keep both.
- **Lakshmamma** is legend — scene 73 opens with ಐತಿಹ್ಯದ ಪ್ರಕಾರ. Keep it.
- Dates to hold: Kempe Gowda I c. 1510–1569 · city founded 1537 · four towers under Kempe Gowda II, late 1500s · Bijapur takes Bangalore 1638 · Mysore Wodeyars buy it for three lakh rupees in 1687 · British storm the fort 1791.
- Scene 29 ("money from the treasury") is hedged with "ಕೆಲವು ದಾಖಲೆಗಳು ಹೇಳುತ್ತವೆ" — keep the hedge.
