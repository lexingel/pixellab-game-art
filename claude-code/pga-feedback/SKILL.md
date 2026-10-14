---
name: pga-feedback
description: "The user's choice about sharing generation outcomes (opt-in) with the skill's authors: see the status, switch it on (stats / prompts) or off, preview exactly what would be sent, send now, or delete everything this install sent. Use when the user types /pga-feedback."
argument-hint: "status | on stats|prompts | off | preview | send | forget"
disable-model-invocation: true
model: haiku
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). This command makes nothing, so it doesn't need the
shared generation loop - read only the files named below.

# /pga-feedback

User's input: **$ARGUMENTS**

No PixelLab calls here. `<out>` = `pixellab.json` → `out` (default `pixellab_out`).

- `status` (or nothing): `python R/scripts/share.py status`, then one line on what that level sends.
- `on stats` / `on prompts`: `python R/scripts/share.py set stats|prompts`.
- `off`: `python R/scripts/share.py set off` - nothing more is sent (already-sent records stay until `forget`).
- `preview`: `python R/scripts/share.py send --log <out>/log.jsonl --preview` - print it as is.
- `send`: `python R/scripts/share.py send --log <out>/log.jsonl --agent <your agent's name>`.
- `forget`: `python R/scripts/share.py forget` - deletes every record this machine sent, switches
  sharing off here and makes a new id for any later opt-in.

What each level sends (say it in plain words when asked):
- `stats`: task, tool, numeric/enum settings (size, seed, frames, mode…), style summary (setting,
  density, view, outline, shading, colours), cost vs estimate, time, QA flags, keep/re-roll/reject.
- `prompts`: stats + the prompt text as typed (it can contain names the user wrote) and their reason
  for rejecting or re-rolling.
- Never, at any level: the PixelLab token, file paths, URLs, uploads, images, the game's name, job ids
  (sent as a one-way hash). Only jobs made after the opt-in. `forget` also switches sharing off and
  starts a new id; `PIXELLAB_SKILL_NO_TELEMETRY=1` blocks sending on the machine.
