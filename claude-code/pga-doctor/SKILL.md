---
name: pga-doctor
description: "Check that everything the pixellab-game-art skill needs works - PixelLab connection and token, plan tier and balance, Python and packages, the project profile, the output folder, sharing - and print the exact fix for anything that doesn't. Free. Use when the user types /pga-doctor."
argument-hint: "(no arguments)"
disable-model-invocation: true
model: haiku
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). This command makes nothing, so it doesn't need the
shared generation loop - read only the files named below.

# /pga-doctor

No generation (only the free `get_balance` call). Run every check, then print one checklist.

1. **PixelLab connection:** call `get_balance`.
   - No PixelLab tools available → `✗ PixelLab not connected` + the connect steps from
     `R/references/prompt_improver.md` §0 (for this agent).
   - Auth error → `✗ token rejected` + "get a new token at https://api.pixellab.ai/mcp and re-add the server".
   - OK → `✓ PixelLab: Tier N (name), balance B generations, resets <date>, M jobs at once`.
2. **Python + packages:** `python R/scripts/check_setup.py pga-anim` (try `python3`, then `py` on
   Windows, if `python` isn't found) - it checks Python and Pillow / numpy / scipy and prints fixes.
   Report which python command works; the other commands will use that one.
3. **Project** (current folder):
   - `pixellab.json` missing → `• no project setup yet - run /pga-init` (not an error).
   - Present → `python R/scripts/style.py list` (styles, active one), `tier` vs what `get_balance`
     showed (differs → say so and that the next command will update it), `engine`, `out` (exists?
     can be created?), `max_cost`.
4. **Sharing:** `python R/scripts/share.py status` (level, since when, install id or none).
5. **Version:** read `R/VERSION` (and `R/../CHANGELOG.md`'s top entry if present) - say which version is installed.

Print:
```
pixellab doctor
✓/✗ PixelLab   …
✓/✗ Python     …   (use: python3)
✓/✗ Packages   …
•   Project    …
•   Sharing    …
•   Skill      version …
Fix first: <the single most important fix, as an exact command - or "nothing, you're ready: try /pga-char <idea> --dry">
```
