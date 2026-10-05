# CRAFT DEFAULTS: general short-form editing rules (style-independent)

These are the engine's defaults for anything the active client style does not specify. The client's
`clients/<client>/<style>/style/STYLE_GUIDE.md` always wins: where it gives a rule, follow it instead of this file.
Note in `EDIT_NOTES.md` any default you used where the style guide was silent on something that mattered.

## 1. Captions
- Captions sit in the lower half, centre-aligned, never over the face. Smaller text reads as higher quality; scale up only
  the emphasised words.
- Words pop in one by one as they are spoken: a short rise from slightly below, a fade and a light blur-in, fast then slow
  (ease-out). A caption group's pops span at most ~1.5 s; at most ~8 words per group.
- One emphasised phrase per group at most (the hook word, a number, the key concept), in the style's accent colour/font.
- Darken or blur the footage behind captions just enough to keep them readable on any background (the engine's SHADE band).
- The hook (first ~3-5 s) shows the speaker; its caption highlights the ONE phrase that makes people stay: a fear or gap,
  the topic, the desire, or an attractive number.

## 2. Motion
- Motion starts on frame 1 of every scene: no dead openings. Entrances are fast then slow (ease-out).
- Build each scene from a blank frame: background, then the hero element, then the text.
- After the entrance, keep a constant subtle drift (slow push-in or float, about 1.00 to 1.04): never fully static.
- Camera moves stay simple: gentle zoom-ins and steady pushes. No twists, swoops, spins or orbits.
- One idea, one hero and one main motion per scene. Vary the scene types; never the same kind of animation twice in a row.
- Each item in a spoken list appears exactly when it is said (start 2-4 frames before the word).
- Animations show the concept; they don't just repeat the words on screen.
- Hard cuts are confident. Transitions into full-screen scenes stay clean: a reveal shape, a quick push or zoom-through,
  or a cut with a short white flash.
- Every jump cut is hidden: a full-screen scene covers it, or the camera changes scale on it (see the skill, step 5).

## 3. Sound design
- Sound emphasises what the viewer can see. If nothing moves on screen, nothing happens in the sound.
- Every effect does one of three jobs:
  - **Whooshes = movement** (slides, zooms, pans, camera moves, scene transitions). Align the whoosh's loudest point with the
    fastest frame of the motion.
  - **Textures = events that don't slide** (pops, clicks, reveals, write-ons, UI changes). Place them on the event frame.
  - **Risers and hits = anticipation.** A riser ends exactly on a transition frame, with a hit under it.
- If something on screen would make a sound in real life (a camera shutter, typing, a click), that sound is the first choice.
- The voice is always on top. Starting levels (cue `gainDb`): whooshes -11 to -15 dB, textures -6 to -11 dB,
  risers/hits -5 to -7 dB. One loudest moment per scene; everything else sits under it.
- Bigger on-screen moments get bigger sounds; small details get small sounds.
- Music sits under the talking head and ducks out under full-screen scenes (automatic in `build_cues.py`).
- Pick phone-friendly music: energy in the mids and highs, a full-energy start, no vocals. Bass-heavy beds vanish on phones.
- Use only the client's sound pack. Before placing a sound, compare the variations in its file/folder and pick the one whose
  length, pace and weight fit the moment.

## 4. Technical constraints (how scenes are built)
- Everything is built procedurally in Remotion 4 (React + TSX, SVG, CSS, canvas) at 1080x1920@30fps. No AI image or video
  generation, no stock images, no external files or network. Objects must be drawable with SVG/CSS (gradients, shadows,
  blur, masks, SVG feTurbulence noise, layered gradients and CSS 3D transforms for depth).
- The talking head can be transformed per frame (punch-ins, pushes) and reused inside designs (inside a phone, a card, a circle
  mask) with `ARollInset`. Cut-outs of the person are not possible (no segmentation).
- Fonts: whatever the style's `theme.ts` loads (any Google Font via @remotion/google-fonts). A client's paid/custom font is
  replaced by the closest Google Font unless its font file is added to the style.
- Captions are a separate layer over the talking head (hidden or restyled during full-screen scenes).
