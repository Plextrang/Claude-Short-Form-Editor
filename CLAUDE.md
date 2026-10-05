# Claude Short Form Editing

This repo turns a raw talking-head recording into a finished 1080x1920 short in a client's own style, fully autonomously.

- **Whenever the user asks to edit a video** (or drops one into `input/`, or says "run the edit"), use the `short-form-edit` skill
  (`.claude/skills/short-form-edit/SKILL.md`) and follow it exactly. It covers setup, client style, cut, plan, scenes, sound, music,
  QA and delivery. Also use it when the user asks to set up a new client or style.
- Every edit uses one client style: `clients/<client>/<style>/` (creative direction + generated style guide and theme), with the
  client's sound pack in `clients/<client>/sound-pack/`. The user names it in the prompt (e.g. "for acme/talking-head").
  How to add a client: `clients/_template/README.md`.
- The user is usually away during the edit: do not ask questions. Make and approve your own decisions, then report at the end.
- Raw video goes in `input/` (exactly one file); an optional music track goes in `input/music/`. Results go to `deliverables/`.
- Work only inside this folder (first-run package installs and Remotion temp cleanup excepted).
- Never copy client material (anything in `clients/` except `_template/`) into tracked files.
