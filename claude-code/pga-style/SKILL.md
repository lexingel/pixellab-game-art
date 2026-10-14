---
name: pga-style
description: "Manage named art styles saved in pixellab.json: list them, switch the active one, show, rename, delete, or create a new one with the same setup conversation as /pga-init. Use when the user types /pga-style."
argument-hint: "list | use <name> | show <name> | new | anchor <family> <image|last> | rename <old> <new> | delete <name>"
disable-model-invocation: true
model: haiku
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). This command makes nothing, so it doesn't need the
shared generation loop - read only the files named below.

# /pga-style

User's input: **$ARGUMENTS**

No generation here (except an optional 1-generation draft inside `new`).

- `list` (or nothing): `python R/scripts/style.py list` and print it as is (`*` = active).
- `use <name>`: `python R/scripts/style.py use <name>` - every command uses it from now on;
  a single call can still pick another with `--style <name>`.
- `show <name>`: `python R/scripts/style.py show <name>`, then a short table field | value.
- `rename <old> <new>` / `delete <name>`: the same script; confirm the result in one line.
- `anchor <family> <image | last>`: approve an image as the active style's reference art for one asset
  family (heroes, monsters, backgrounds, scenes, buildings, icons, ui) - every later job of that family
  matches it. `last` = the newest kept file from `python R/scripts/history.py --n 1`.
  Run `python R/scripts/style.py anchor <family> <image> [--style <name>]` and print its line.
- `new`: say "run `/pga-init` - with a profile already here it only asks for the new art style
  (send a reference or pick parameters) and saves it next to the others". (Building a style reads
  images and asks questions, so it lives in `/pga-init`; this command only manages saved styles.)
- Unknown name: show `list` and stop.
