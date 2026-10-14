---
name: pga-reroll
description: "Re-run a past generation - the last one, or one named by file, name or words - with a new seed or the user's wording change, same tool and settings otherwise. Use when the user types /pga-reroll."
argument-hint: "[last | <name or file or words>] [<what to change: \"no cape\", \"brighter\", \"seed 11\">]"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-reroll

User's input: **$ARGUMENTS**

Follows the shared loop's §5-§8 (call block, no permission prompt, results table).
1. Find the job: `python R/scripts/history.py <out>/log.jsonl --n 1 --json` for `last` (or no target),
   else `--find <words> --n 3 --json` - more than one match → list them (one line each) and ask which (the only question).
2. Same tool, size, style anchor and parameters as that job. Change exactly one thing:
   - the user said what to change → apply it to the prompt (keep everything else word for word);
   - nothing said → the seed (previous seed + 1, or 11 if it was 7), and say so.
   Animation jobs: re-run only the step that failed (a key pose, or the in-between) - see `/pga-anim`.
3. Print the call block and the cost; submit; fetch; QA and look as in §7.
4. `python R/scripts/outcome.py <out>/log.jsonl <old job> --verdict reroll --reason "<what changed>"`, then
   the new job's outcome as usual. Results table: old file → new file, and which one to keep.
