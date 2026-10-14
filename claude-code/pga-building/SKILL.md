---
name: pga-building
description: "Make a pixel-art building or prop (and upgrade tiers) with PixelLab in the pixellab-game-art house style - improves the description first (single building, side elevation, night light, no people), then generates, QA-checks and logs. Use when the user types /pga-building."
argument-hint: "<building or prop idea> [--tiers 3] [--ref building.png] [--draft] [--dry]"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-building

User's request: **$ARGUMENTS**

Read: `R/references/library/house_rules.md`, `R/references/library/buildings.md`.

- `create_image_pro` small (≤ profile `building_max`, 170): returns 4-16 candidates - pick the best.
  Profile seed, `no_background: true`, style ref = anchor `buildings`. Cost 10-15.
- Template: `single <building>, flat side elevation, not isometric, <materials>, <2-3 details>,
  night, warm light from the windows, no people, no text, whole building fits inside the canvas
  with a small margin, <look>`
- `--tiers N`: tier 1, then each next tier with `edit_image_pro_flash` on the previous:
  `grow this <tier n> into <tier n+1>: <changes>, same pixel art style and palette` (seed 1 or 3).
  Cost 5-6 each at ≤200 px.

Improve: one building per call; materials + one signature feature (forge glow for a smithy, a
sign shape without letters for a tavern). Cropped roof → edit "zoom out: draw this same building a
little smaller so it fits with ~4 px transparent margin; keep design, colours, bottom position".

QA: `qa.py <candidates> --anchor <anchor>` (edge contact = cropped); pick from the half-size sheet.
