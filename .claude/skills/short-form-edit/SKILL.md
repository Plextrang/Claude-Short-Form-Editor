---
name: short-form-edit
description: Fully autonomous edit of a raw talking-head recording (dropped into input/) into a premium 1080x1920 short in a client's own style (clients/<client>/<style>/) - Whisper word-level transcription, bad-take and silence cutting, camera punch-ins, styled captions, procedural Remotion motion-graphics scenes, sound design from the client's sound pack, music, a phone-ready mix, QA and deliverables in deliverables/. Also onboards a new client style from its creative direction and sound pack. Use when the user asks to edit a video / the raw footage / "run the short-form edit" in this repo, to set up a client or style, or to redo any stage of an edit (cut, captions, scenes, sound, mix, QA).
---

# Short-form edit (zero-intervention)

Every edit is made in ONE client style: `clients/<client>/<style>/`. Its `style/STYLE_GUIDE.md` (the client's look, motion and
sound rules) overrides the engine's general rules in `work/plan/CRAFT_DEFAULTS.md`. If the style has `examples/` (approved past
edits: scene code, plan, cue sheet, notes), copy their patterns. The engine, scripts and rules are already built. Your job is
the per-video creative work plus disciplined QA.
Below, `<S>` means the active style folder `clients/<client>/<style>` and `<P>` the active sound pack (printed by `use_style.py`).
**Target:** about 3 h and at most ~60M weighted tokens (the first build of this pipeline took ~143M; see `references/LESSONS.md`).

## 0. Operating rules (read first; this is where tokens go)
- **The user is away.** Don't ask questions. Approve your own decisions, finish end to end, report once at the end.
- **Stay inside this repo folder.** First-run setup may also install packages (step 0). After the scene workflow, after review stills
  and after every full render, run `python work/scripts/clean_temp.py`: Remotion leaves several GB of temp copies per render.
- **Effort: High.** This skill authorises exactly ONE workflow (step 6). Never run:
  - plan panels or judges;
  - per-scene reviewer agents;
  - multi-reviewer QA rounds or skeptic-verifier fan-outs.

  They cost ~60% of all tokens on the first project.
- **Keep the main loop lean:**
  - inspect frames as contact sheets or strips, each image ≤ ~2000 px on its long side;
  - open a full-res still only to check one specific defect;
  - pipe logs through `tail`/`grep`;
  - batch shell steps;
  - never re-read files you just wrote.
- **Every fix loop is ONE pass.** Fix only checklist items, spec violations and reported `knownIssues`. Log anything left over under
  "not verified" in the final report.
- A full render takes ~5 min on an idle CPU but times out while agents render stills. Never full-render during the scene workflow.
- Write files with LF and ASCII where possible. For anything with regexes use the Write/Edit tools or a `.py` file, not heredocs.
- **The mix settings in `work/scripts/mix.py` are tuned for phones; don't retune them.** They are: voice anchored and
  untouched, music +6 dB with a presence shelf, SFX +4 dB capped under the voice.
- **Never edit engine files to fit a client.** Client-specific things live in `<S>` (style guide, `style/theme.ts`).

## 1. Repo map
| Engine (don't rewrite) | Client style (per client, git-ignored) | Per video (you author) |
|---|---|---|
| `remotion/src/components/*`: `ARoll` (camera, BlurBand, LogoVeil, `camAt`, `bandAt`), `Captions`, `ARollInset`, `PaperBG`, `Primitives`, `Devices`; `lib/anim.ts`, `theme.ts` (re-exports the style's theme), `Main.tsx`, `Root.tsx` | `<S>/style/STYLE_GUIDE.md`: the client's look, motion and sound rules | `remotion/src/data/edit.ts`: CAMERA, JUMP_CUTS, CAPTIONS, SHADE, FLASHES |
| `remotion/scripts/stills.mjs`: many stills, one bundle, `--entry=` for scene previews | `<S>/style/theme.ts`: fonts + colours (copied to `remotion/src/data/style_theme.ts` by `use_style.py`) | `remotion/src/scenes/*.tsx` + `src/preview/*.entry.tsx` |
| `work/scripts/*` (see the steps); `finalize.sh` (style sync → integrate → tsc → render → cues → mix → mux → loudness → strips) | `<S>/source/`: the creative direction; `<S>/style/board/`: its rendered pages | `work/plan/keep.json` (cut list), `work/plan/vocabulary.txt` (names for Whisper) |
| `work/plan/CRAFT_DEFAULTS.md` (general rules), `work/plan/ENGINE.md` (scene contract) | `<S>/examples/` (optional): approved past edits | `work/plan/MASTER_PLAN.md`, `work/plan/cue_sheet.json` |
| `clients/_template/` (how to add a client); `references/ONBOARDING.md` | `<P>` = `clients/<client>/sound-pack/` (or `<S>/sound-pack/`) + its catalogue `<P>/_catalogue/sfx_*.json`; `clients/<client>/client.md`, `docs/` | `remotion/public/music.wav` |
| `archive/<video>/`: your previous videos (each records its style in `work/active_style.json`) | | Generated: `words.json`, `scenes.ts`, `video.json`, `sound_cues.json` |

Inputs: the raw recording in `input/` (exactly one video file); optionally a music track in `input/music/`.
Every client file and every per-video file is git-ignored, so editing never changes what this repo publishes. Never put client
material or personal data in tracked files.
Outputs: `deliverables/`.

## 2. Pipeline

### Step 0: setup and reset (~5 min; setup only on a new machine)
1. **Setup:** run `python work/scripts/setup_check.py`.
   - It creates the per-video data files from `work/templates/` and installs any missing Python/Node packages.
   - If it reports a MISSING program (Node.js or ffmpeg), install it with the command it prints (winget / brew / apt), then re-run.
     If `python` itself is missing, install Python 3.10+ the same way first.
   - If an install fails or the program still isn't found (a new PATH may need a Claude Code restart), stop and report the exact
     command for the user to run.
2. **Previous video.** If the previous video's files are still in place (anything in `remotion/src/scenes/`, or `work/transcript/edl.json`):
   - run `python work/scripts/new_video.py <slug-of-previous-video> --dry-run`, then run it again without `--dry-run`;
   - it archives every per-video file to `archive/<slug>/`, including the previous raw video, which it detects by duration.
     A new recording already in `input/` is kept.
3. **Input.** `input/` must contain exactly ONE video file: that's the new recording. If there are none, or several, stop and report.
4. **Client style.** Run `python work/scripts/use_style.py <client>/<style>` with the style the user named
   (e.g. "for acme-media/talking-head"). If they named none, run it without arguments: it picks the only style
   there is. With several styles and none named, stop and report the list (`--list`) before doing any work.
   - It prints the paths of `<S>` and `<P>`. Read `<S>/style/STYLE_GUIDE.md` now, plus `clients/<client>/client.md` if it exists.
   - If it prints NEEDS ONBOARDING, follow `references/ONBOARDING.md` first (once per style, ~20-30 min), then continue.

### Step 1: ingest (~5 min)
1. Run `python work/scripts/prep_audio.py` (it finds the video in `input/`), then Read `work/frames/contact.png`. Note:
   - the face centre and the zones: headroom, face, mic, hands, desk;
   - any static brand logo on the set: set `LOGO` in `remotion/src/data/edit.ts` to its centre in source px. It's `null` (off) by default;
   - the background colour.
2. **Sound effects.** Run `python work/scripts/sfx_catalog.py`: it checks the active sound pack `<P>` and rebuilds its catalogue
   if the files changed (about a minute). If the pack has no `.mp3`/`.wav`, edit without sound effects (music and voice only)
   and say so in the final report.
3. Run `python work/scripts/transcribe.py small.en`. The first run downloads the model to `work/hf_cache`.

### Step 2: cut (~15 min)
1. From `work/transcript/whisper_small.en.json`, choose keeper sentences:
   - the best COMPLETE take of each sentence (usually the last);
   - drop false starts, repeats, "let me do that again", the opening breath and getting up at the end.
2. Write them to `work/plan/keep.json` as `[["S01", src_start_s, src_end_s, "text"], ...]` with rough bounds.
   - Ranges must not overlap; merge touching sentences, or audio duplicates.
   - The script refines the bounds on a 5 ms energy envelope, keeps 45/85 ms handles, and trims pauses over 240 ms to 140 ms.
3. Run `build_edl.py`, then `render_cut.py`, then `voice_process.py` (voice at −16 LUFS), then `integrate.py`.
   - Run them all from the repo root as `python work/scripts/<name>`.
   - The early `integrate.py` run sets TOTAL_FRAMES and writes `video.json`, which lists the jump cuts: every EDL piece boundary.
4. Put this video's names, brand words and jargon on one line in `work/plan/vocabulary.txt`.
   Then run `python work/scripts/transcribe_cut.py small.en` and `python work/scripts/transcribe_cut.py medium.en`.
5. Run `python work/scripts/words_consensus.py` → `remotion/src/data/words.json`. Check that the printed text reads clean.

### Step 3: plan (solo, ~30 min). Write `work/plan/MASTER_PLAN.md`
Design every scene from `<S>/style/STYLE_GUIDE.md` and the board pages in `<S>/style/board/` (or the images in `<S>/source/`).
If `<S>/examples/` has a `MASTER_PLAN.md`, follow its format. Each scene needs:
- `## <ID>  [from-to)  type: FULL-SCREEN|ON-SCREEN`, family, background and focal point;
- design: every element with exact size, colour and position;
- choreography keyed to word frames: pops start 3-4 frames before the word;
- transitionIn / transitionOut. **They are implemented inside the scene**, so say so. Include the planned opaque frames;
- emotional job;
- a required line `- **refs**: <S>/style/board/<tile>.png (or <S>/source/<image>); <S>/examples/<video>/scenes/<Scene>.tsx`
  (paths from the repo root; name example scenes only if the style has examples);
- `- **handoff**: ...` whenever a full-screen scene starts where another ends: what each side shows on the seam frames.

IDs: `FS<n>_<Name>` for full-screen, `OS<n>_<Name>` for on-screen. Density: follow the style guide. If it is silent, use what
worked for 60 s on the reference edit:
- About 10 full-screen scenes of 2-4 s each (~45% of runtime) plus 3-4 lower-third cards.
- The hook (~first 3-5 s) shows the speaker; the first full-screen scene lands right after the hook.
- Never the same family twice in a row. Show the concept, don't echo the words.
- Plant one payoff callback: an object or idea from an early scene that pays off in a later one.

### Step 4: music (~10 min, can run alongside step 3)
- **If the Epidemic Sound connector is available** (ToolSearch "SearchRecordings" finds it):
  1. `SearchRecordings`: no vocals, 90-128 BPM, moods such as elegant / hopeful / laid-back.
  2. Curl the `lqmp3` preview URLs into `work/music_audition/`, then run `python ../scripts/music_audition.py` inside that folder.
  3. **Pick for phones:** a full-energy start (`intro_s` ≈ 0), moderate `voiceband`, real energy in `air` / upper mids.
     Reject tracks dominated by `low`; bass-heavy beds vanish on phone speakers.
  4. `EditRecording` with:
     `{targetDurationMs: round(total_frames/30*1000), forceDuration: true, downloadAudioFormat: "WAV", loopable: false, skipStems: true, requiredRegionsAtOffsets: [{startMs: 0, endMs: 14000, offsetMsInEdit: 0}]}`
  5. `PollEditRecordingJob` → `DownloadRecordingEdit`.
- **Otherwise,** use the track in `input/music/` if there is one: trim it to the video length with a 1.5 s fade-out.
- **If neither exists,** skip music. `mix.py` runs without it; say so in the report.
- Write the result to `remotion/public/music.wav` (48 kHz stereo, via ffmpeg). Credit the track in the notes.

### Step 5: talking-head layer in `remotion/src/data/edit.ts` (~25 min). FINISH IT BEFORE STEP 6
Scene agents match their seams against CAMERA and SHADE, so both must be final before the workflow starts. Run
`npx tsc --noEmit -p .` from `remotion/` when done. If the style has examples, `<S>/examples/<video>/edit.ts` is a full example.

**Camera** (`{f,s,x,y,ease,dur}`, origin ≈ the face centre, e.g. (540, 600)):
- Open on motion: 1.2 → 1.08 `snap` over 9 frames.
- Punch-in (~1.3) on the hook's key word.
- **Every jump cut not covered by a full-screen scene** gets a `cut` key changing scale by ≥0.18, or by ≥0.12 plus a ≥100 px y shift.
- Punches use `cut` or `snap`, never `smooth`.
- Slow `linear` pushes (+0.04-0.06) in between. Never rotate.

**Captions:** `cap(from,to,i0,i1,'tier3'|'line'|'stack2',{accent,bold,y,accentSize})`, with `stack2` taking `split`.
Use the layouts and `y` the style guide names; colours and fonts come from the style's theme automatically.
- `tier3` = small sans / BIG accent-colour serif / small sans. At most one accent phrase per group: the hook word, numbers, key concepts.
- At most ~8 words per group, and the spoken span from first to last pop ≤ ~1.5 s. Groups longer than 5 words use `stack2` or `tier3`.
- Back-to-back groups share the boundary frame (`to == next.from`), or the caption blinks.
- A group followed by a gap ends ≥10 frames after its last word's `f`.
- A group before a full-screen scene ends exactly at that scene's `from`; captions draw on top of scenes.
- Omit captions where a scene shows the words.
- `y`: default 1250; 1060-1180 above on-screen cards; never on the face.

**SHADE** (band + logo veil):
- On whenever captions or cards are over the talking head. Defaults: top 840, blur 13. Card ranges: top 840-950, blur 16, dark 1.15.
- Extend each range to the covering scene's planned opaque frame +1. Re-check against `video.json` after step 6.
- Adjacent ranges cross-fade over 8 frames; others switch hard at cuts.

**FLASHES:** a white flash (up 1, down 5, max 0.9) on 1-2 money-line cuts.

### Step 6: scenes (the ONE workflow, ~45-60 min)
1. Launch the workflow:
   `Workflow({scriptPath: "<abs repo root>/.claude/skills/short-form-edit/scene_build.workflow.js", args: {root: "<abs repo root>", style: "clients/<client>/<style>", ids: [...all scene IDs]}})`
   - One agent per scene, 5 at a time. Each follows ENGINE.md's self-check (max 3 rounds) and returns `{events, opaqueFrom, opaqueUntil, knownIssues}`.
   - Meanwhile only steps 4 and 7 (drafting) may run. Don't render.
   - If the Workflow tool is unavailable, send the same per-scene prompt with the Agent tool, 5 per message.
2. Save the reports to `work/plan/scene_reports.json` as `{id: report}`.
3. Run `integrate.py`, then `npx tsc --noEmit -p .`. Align the SHADE ends with the `opaqueFrom` values in `video.json`, then run `clean_temp.py`.
4. Review it yourself, in one pass:
   - For each batch of 4 scenes: `node scripts/stills.mjs Main out/review/b<n> <3 frames per scene> --scale=0.2`, then
     `python ../work/scripts/sheet.py out/review/b<n> out/review/b<n>.png 6`.
   - Fix by direct edits, or one `Agent` call with a precise list.

### Step 7: sound design (~20 min). Write `work/plan/cue_sheet.json`
1. The format is in the `build_cues.py` docstring (an example is `<S>/examples/<video>/cue_sheet.json` if the style has one):
   `{"musicNoDip": [...], "cues": [{"frame","family","file","peak","gainDb","note"}]}`. `file` is a path inside `<P>`.
2. Variations (`s`/`pk`/`e` in seconds) come from `<P>/_catalogue/sfx_events.json`. Use the style guide's sound section and its
   event-to-file mapping first, then CRAFT_DEFAULTS §3. Default numbers:
   - **Whooshes −11 to −15 dB**, peak on the fastest frame of the move; camera-punch whooshes −14/−15.
   - **Textures −6 to −11 dB** on the event frame; accent-word pops ≈ −9.
   - **Risers −5 to −7 dB**, ending exactly on a transition frame with a hit under it.
   - One loudest moment per scene. Sync to the reports' `events`.
   - The reference edit used 126 cues in 60 s.
3. Music automation, the mobile boosts and the SFX-under-voice cap are all automatic.
4. Empty sound pack: write `{"musicNoDip": [], "cues": []}` and skip the rest of this step.

### Step 8: render and QA (~30 min)
1. `bash work/scripts/finalize.sh draft1` (full scale). Check:
   - `FINALIZE OK`;
   - −13.6 ± 0.5 LUFS and true peak ≤ −1.0;
   - no "hot spots" above 0 dB.
2. Read `remotion/out/strips_draft1/strip_*.png`: every seam, 11 consecutive frames including the one before the cut.
3. Render each full-screen scene's `from-1`, `from`, `to-1` and `to` with `stills.mjs Main ... --scale=0.5`. Compare the pairs.
4. Spot-check the ~10 loudest cues against the picture:
   `python work/scripts/strips.py remotion/out/draft1_video.mp4 remotion/out/cuecheck 1 --points=<frames>`.
5. Checklist:
   - a caption across a cut, or blinking;
   - the band popping or changing height at a seam;
   - reveal framing that differs from Main;
   - a set logo readable next to captions;
   - text clipped or outside the safe zone;
   - a static first frame;
   - a frozen or ghosted exit;
   - a blank frame between two full-screen scenes;
   - an SFX off its visible motion by more than one frame.
6. One fix pass, then:
   - for visual fixes, re-render as `final`;
   - for sound-only fixes, `SKIP_RENDER=draft1 bash work/scripts/finalize.sh final`;
   - if nothing failed, deliver `draft1`.

   Run `clean_temp.py` after each render.

### Step 9: deliver (~10 min)
1. Copy the final mp4 to `deliverables/FINAL - <Title>.mp4`. `mix.py` already wrote `deliverables/audio_stems/`.
2. Run `python work/scripts/make_srt.py`.
3. Write `deliverables/EDIT_NOTES.md`: the client style used, then 1 Cut (raw → final length, what was removed), 2 Look (what
   came from the style guide, any defaults used), 3 Animation map (absolute frames), 4 Sound design, 5 Music (with credit),
   6 Quality control, 7 Files. If the style has examples, match their `EDIT_NOTES.md`.
4. Phone preview < 30 MB: `ffmpeg -i <final> -vf scale=720:1280 -c:v libx264 -b:v 2800k -c:a aac -b:a 160k deliverables/<title>_phone.mp4`.
   If the SendUserFile tool exists, send it (status `proactive`).
5. Report: what was made, the paths, the music credit, anything not verified.

## 3. Rules that prevent real defects
- **Never use CSS `backdrop-filter`.** Over video, the headless renderer turns it into a mirrored kaleidoscope.
  Glass = semi-opaque fill; blur = `filter: blur()` on a real copy of the footage.
- **Scenes own their transitions.** `integrate.py` mounts everything with plain cuts.
- **Seams cause most defects.** Scenes derive the camera and band with `camAt`/`bandAt`. They paint the band layers with
  separate opacities, and full-screen neighbours hand off without a blank frame. Details are in ENGINE.md.
- Scene exports `_FROM`, `_TO` and `_OPAQUE_*` must be plain integer literals.
- Composition IDs: letters, digits and `-` only.
- `OffthreadVideo` in a `Sequence` needs `trimBefore` (ARollInset `seqFrom`). No `Math.random` or `Date`.
- Use the client's local files in `<S>` (rendered pages in `style/board/`, originals in `source/`); no Figma access is needed.
- Reuse scenes from `archive/` only if that video used the same client style (its `work/active_style.json` says which).
