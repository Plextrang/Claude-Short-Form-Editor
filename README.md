# Claude Short Form Editing

Drop in a raw talking-head recording. Claude Code edits it end to end into a premium vertical short (1080x1920, 30 fps),
in **your client's style**, from their creative direction and their sound pack:

- word-level transcription; bad takes, false starts and dead air cut;
- camera punch-ins that hide every jump cut;
- captions designed from the client's creative direction (fonts, colours, emphasis words);
- 10+ custom motion-graphics scenes and on-screen UI cards, built in code (Remotion) in the client's look;
- **colours taken from the footage**: every video gets its own palette from the speaker's clothing, the set and its lights
  (a blue shirt gives blue animations), so no two videos look the same and the graphics feel part of the shot;
- **real logos and real interfaces**: YouTube, Instagram DMs, TikTok, Premiere Pro, CapCut and 60+ other brands appear as
  their official logos and real-looking UIs, never drawn stand-ins;
- sound design placed frame-accurately from the client's sound pack;
- background music, plus a phone-ready mix;
- QA, and deliverables: video, audio stems, subtitles and edit notes.

No human input is needed during the edit. One setup serves every client: each client gets their own folder, and each client can
have several editing styles.

## Quick start
1. Requirements (Claude installs any missing ones on the first run; you can also install them yourself):
   - [Claude Code](https://claude.com/claude-code) (desktop app or CLI), with a plan that can run long sessions;
   - [Node.js](https://nodejs.org) 18+;
   - [Python](https://python.org) 3.10+;
   - [ffmpeg](https://ffmpeg.org) on your PATH (`ffmpeg -version` must work);
   - Windows: Git Bash, which Claude Code installs with Git for Windows.
2. Download or clone this repo.
3. **Add your client** (details in `clients/_template/README.md`):
   - copy `clients/_template/` to `clients/<client>/` and rename `my-style/` (e.g. `talking-head`);
   - put the client's **creative direction** (PDF or PNG/JPG; export Figma boards as PDF/PNG) into `<style>/source/`;
   - put the client's **sound effects** (.mp3/.wav) into `clients/<client>/sound-pack/`.
4. **Put your raw video in `input/`** (one file: .mp4 / .mov / .mkv). Optionally add a music track to `input/music/`.
   Music: if you connect your own [Epidemic Sound](https://www.epidemicsound.com) account in Claude (Settings → Connectors),
   Claude picks a track and fits it to the video's exact length.
5. Open Claude Code **in this folder**:
   - **High** effort (Ultracode isn't needed and costs several times more);
   - a permission mode that won't stop for approvals while you're away (e.g. bypass permissions);
   - about 30 GB of free disk space.
6. Paste (with your client and style):

   > Use the short-form-edit skill to edit the video in input/ for acme-media/talking-head. I'm away and can't approve anything, so make every decision yourself and tell me when the final video is in deliverables/.

7. Come back to `deliverables/`:
   - `FINAL - <title>.mp4`;
   - a phone preview;
   - `audio_stems/` (voice, music, whooshes, textures, risers, hits, master);
   - `captions.srt`;
   - `EDIT_NOTES.md`.

**First edit for a new client style:** Claude first onboards it (~20-30 min): it reads the creative direction, writes the style's
`STYLE_GUIDE.md` and `theme.ts` (colours and fonts), and sorts and catalogues the sound pack. Every later edit in that style starts
straight away.

**First run on a new machine:** Claude installs the Node and Python packages and downloads the Whisper models (~2 GB). If Node.js
or ffmpeg is missing, Claude installs it too (winget / brew / apt); on some machines you then need to restart Claude Code once.
An edit takes roughly 3 hours of unattended work.

**Next video:** drop the new recording into `input/` and paste the prompt again (with the client and style). The previous video's
working files are moved to `archive/<video>/` automatically.

## What's inside
| Path | What |
|---|---|
| `.claude/skills/short-form-edit/` | The skill: the step-by-step pipeline Claude follows, client onboarding, the parallel scene-build workflow, lessons learned |
| `CLAUDE.md` | Tells Claude Code to use the skill |
| `clients/_template/` | How to add a client, and the folder layout to copy. Your clients live next to it (never in git) |
| `remotion/` | The video engine: camera, captions, blurred lower band, logo veil, design primitives, scene mounting |
| `work/scripts/` | Pipeline scripts: client style selection, transcription, cut, voice processing, cue sheet, mix, QA strips, `finalize.sh` (one-command rebuild) |
| `work/plan/CRAFT_DEFAULTS.md` | General editing, motion and sound rules, used wherever a client's style doesn't say otherwise |
| `work/plan/ENGINE.md` | The contract every scene follows |
| `work/templates/` | Fresh per-video data files and the theme template for new styles |
| `work/scripts/palette.py` | Builds each video's colour palette from its footage (`--accent` / `--warm` to steer, `--off` to keep the style's colours) |
| `work/scripts/fetch_brand_assets.py`, `work/brand_assets.json` | Downloads the real logo + UI glyph library into `remotion/public/brand` and `remotion/public/ui` (run automatically by the setup check; `--si`, `--commons`, `--ui` add more) |
| `input/`, `deliverables/`, `archive/` | Your footage, your results, previous videos |

## Notes
- **Privacy:** client folders and everything a video produces (footage, transcript, cut list, plans, renders, deliverables) are
  git-ignored. You can use this in a clone and pull or push engine updates without publishing any client material.
- **Back up `clients/`:** it isn't in git, so it only exists on your machine. Keep a copy on a cloud drive or in a private repo.
- **Quality follows the creative direction:** the more specific the client's direction (examples of captions, scenes, transitions,
  sounds), the closer the edit matches their style.
- **Platform:** built and tested on Windows 10. macOS and Linux should work: all scripts are Python, Node or bash.
- **Licences:**
  - [Remotion](https://www.remotion.dev/license) is free for individuals and small teams; larger companies need a company licence.
  - Fonts are loaded from Google Fonts (open source); a client's paid font is replaced by the closest Google Font.
  - Sound effects and music are subject to their own licences (the client's pack, your Epidemic Sound subscription, ...).
  - Brand assets are downloaded on your machine, never stored in this repo: brand glyphs from
    [simple-icons](https://simpleicons.org) (CC0), UI glyphs from [Material Symbols](https://fonts.google.com/icons)
    (Apache-2.0), official app logos from [Wikimedia Commons](https://commons.wikimedia.org). Logos are trademarks of their
    owners; they are shown to refer to the product the speaker talks about.
