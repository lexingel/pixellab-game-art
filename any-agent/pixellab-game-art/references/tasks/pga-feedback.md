# Task pga-feedback

Run when the user asks for `pga-feedback` (with or without a slash) or describes this job in plain words.
Input: status | on stats|prompts | off | preview | send | forget

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's input: **(the user's request)**

No PixelLab calls here. `<out>` = `pixellab.json` → `out` (default `pixellab_out`).

- `status` (or nothing): `python <skill>/scripts/share.py status`, then one line on what that level sends.
- `on stats` / `on prompts`: `python <skill>/scripts/share.py set stats|prompts`.
- `off`: `python <skill>/scripts/share.py set off` - nothing more is sent (already-sent records stay until `forget`).
- `preview`: `python <skill>/scripts/share.py send --log <out>/log.jsonl --preview` - print it as is.
- `send`: `python <skill>/scripts/share.py send --log <out>/log.jsonl --agent <your agent's name>`.
- `forget`: `python <skill>/scripts/share.py forget` - deletes every record this machine sent, switches
  sharing off here and makes a new id for any later opt-in.

What each level sends (say it in plain words when asked):
- `stats`: task, tool, numeric/enum settings (size, seed, frames, mode…), style summary (setting,
  density, view, outline, shading, colours), cost vs estimate, time, QA flags, keep/re-roll/reject.
- `prompts`: stats + the prompt text as typed (it can contain names the user wrote) and their reason
  for rejecting or re-rolling.
- Never, at any level: the PixelLab token, file paths, URLs, uploads, images, the game's name, job ids
  (sent as a one-way hash). Only jobs made after the opt-in. `forget` also switches sharing off and
  starts a new id; `PIXELLAB_SKILL_NO_TELEMETRY=1` blocks sending on the machine.
