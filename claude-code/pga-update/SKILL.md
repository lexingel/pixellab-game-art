---
name: pga-update
description: "Get the latest version of the pixellab-game-art skill (updated weekly with the lessons from shared results) and merge it into this install, keeping files the user changed; check for one, or undo the last update. Use when the user types /pga-update."
argument-hint: "(nothing) | check | undo | from <downloaded zip or folder>"
disable-model-invocation: true
model: haiku
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). This command makes nothing, so it doesn't need the
shared generation loop - read only the files named below.

# /pga-update

User's input: **$ARGUMENTS**

No PixelLab calls. The skill gets an update every week (the lessons from shared results, fixes, new
commands). The user's `pixellab.json`, styles, logs and generated files live outside the skill folder
and are never touched.

- nothing / `now`: `python R/scripts/update.py` - downloads the latest version, backs up this one,
  installs the new one with the same options as before and puts back every skill file the user edited.
- `check`: `python R/scripts/update.py check` - one line: newer version or up to date.
- `undo`: `python R/scripts/update.py rollback` - restores the version from before the last update.
- `from <zip or folder>`: `python R/scripts/update.py --from <path>` - for a ZIP the user downloaded
  from the repository page (green **Code** button → Download ZIP) when the download fails.

After an update, in this order:
1. Print the "Updated A -> B" line and the "What's new" notes as the script printed them.
2. **Merge** every `MERGE` line: the user edited a file the update also changed. Read `<file>` (theirs)
   and `<file>.from-update` (the update's), write `<file>` = the update's version with the user's own
   additions and changes carried over (their wording wins where both changed the same lines), then
   delete `<file>.from-update`. One line per file: what came from the update, what was kept from theirs.
3. Say: restart the assistant so new or changed commands load; `/pga-update undo` reverts.

Errors: "could not check" / download failed → offline, or the repository isn't public yet; give the
`from <zip>` route. "installer failed" → show its output; nothing was lost (`undo` restores).
