---
name: pga-batch
description: "Make many pixel-art assets in one go with PixelLab (icons, monsters, props, backgrounds…): improves every prompt, shows one cost table, submits all jobs together, downloads, QA-checks and logs them, and returns one review sheet. Use when the user types /pga-batch."
argument-hint: "<type>: item, item, item…  |  <file.csv or .txt, one item per line>  [--dry] [--draft]"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-batch

User's request: **$ARGUMENTS**

Read: `R/references/library/house_rules.md` and the library file for each type in the batch.

1. **Items**: from the list in the arguments, or a CSV/TXT file (`type,prompt[,size][,ref]` or one
   prompt per line). Mixed types are fine - group them by command type (char / bg / scene /
   building / icon). Animations and VFX are not batched - use `/pga-anim` / `/pga-vfx`.
2. **Improve every prompt** with that type's rules (prompt_improver §3-4). Keep one anchor and one
   seed per type so the set matches.
3. **One table**: `# | type | improved prompt (short) | tool | size | cost` + total, and balance.
   Then the call block for every job (prompt_improver §5). `--dry` stops here; otherwise submit
   without asking (a `max_cost` cap stops before submitting and prints the override flag).
4. **Submit every job in the same turn** up to the tier's limit (`R/references/pixellab_api.md` → Subscription tiers); send the rest when
   the first finish. Write `jobs.txt` (`name job_id [frames] {meta}`), then one
   `python R/scripts/fetch.py --jobs <out>/jobs.txt --out <out> --log <out>/log.jsonl`.
   FAILED lines are refunded - resubmit them once, in one go.
5. **QA everything at once**: `qa.py <out>/*.png [--anchor …] --sheet <out>/flagged.png`; then one
   half-size contact sheet of the whole batch (`contact_sheet.py … --scale 0.5`, 6-8 per row).
   Look at the sheet once and the flagged sheet if any.
6. **Report**: the prompt_improver §8 results table (one row per job: tool, job id, generations,
   status OK / flagged + why, file), total vs estimate, balance before → after, the sheet, and a
   ready-to-run `/pga-batch` line for the items worth re-rolling (with the wording change).
