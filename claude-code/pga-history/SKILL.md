---
name: pga-history
description: "Show past generations from the job log - newest first, with cost, verdict and files - and what was spent (per command, tool and day). Free. Use when the user types /pga-history."
argument-hint: "[N] [--cmd pga-char] [--find <text>] [--cost]"
disable-model-invocation: true
model: haiku
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). This command makes nothing, so it doesn't need the
shared generation loop - read only the files named below.

# /pga-history

User's input: **$ARGUMENTS**

No PixelLab calls. `<out>` = `pixellab.json` → `out` (default `pixellab_out`).
1. `python R/scripts/history.py <out>/log.jsonl --n <N or 15> [--cmd …] [--find …]` - print its lines as a table.
2. `--cost` (or the user asks what they spent): also `python R/scripts/cost_report.py <out>/log.jsonl`
   and call `get_balance` (free) for the balance left and the reset date.
3. End with the two next steps that fit: `/pga-reroll <name>` for a result they didn't like,
   `/pga-style anchor <family> <file>` for one they want every later job to match.
