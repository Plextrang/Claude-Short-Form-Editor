# Adding a client

Every client gets its own folder in `clients/`, holding their creative direction and their sound pack. Nothing in `clients/`
is ever pushed to git (only this template is), so client material stays on your machine.

## 1. Copy this template
Copy `clients/_template/` to `clients/<client-name>/`, e.g. `clients/acme-media/`. Use lowercase letters, digits and dashes.
Rename `my-style/` to a name for the editing style, e.g. `talking-head`.

```
clients/acme-media/
  client.md          brand notes (optional): who they are, logo on set, words to spell right, do's and don'ts
  docs/              any extra guides from the client (optional), e.g. their sound-design or editing rules
  sound-pack/        their sound effects (.mp3 / .wav), shared by all their styles
  talking-head/      one editing style
    source/          their creative direction: PDF, PNG/JPG exports, notes
    style/           filled in by Claude (don't add files here)
    examples/        optional: approved past edits in this style
```

## 2. Add their files
- **Creative direction** into `<style>/source/`. A PDF or PNG/JPG images. **Figma:** export the board as PDF or PNG first
  (Claude can't open `.fig` files).
  No creative direction? Ask the client for one, or write one yourself from their best videos (a PDF with frames and notes).
- **Sound effects** into `sound-pack/`. Any folder layout works: Claude sorts them into `whoosh/`, `textures/` and
  `risers and hits/` during onboarding.

## 3. Edit
Put the raw video in `input/` and tell Claude which client and style to use, e.g.:

> Use the short-form-edit skill to edit the video in input/ for **acme-media/talking-head**. ...

The first edit for a new style starts with onboarding: Claude reads the creative direction and writes `style/STYLE_GUIDE.md`
and `style/theme.ts` (colours and fonts), then edits as usual. After that, every edit for that style starts straight away.

## More styles for the same client
Add another folder next to the first (e.g. `clients/acme-media/podcast-clips/source/`) and drop that style's creative
direction in. It uses the client's `sound-pack/` unless you give it its own `sound-pack/` folder.

## Back up your clients
`clients/` is not in git, so it only exists on this computer. Back it up yourself (a cloud drive or a private repository).
