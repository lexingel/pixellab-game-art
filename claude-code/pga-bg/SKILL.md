---
name: pga-bg
description: "Make a side-view pixel-art battle background with PixelLab in the pixellab-game-art house style - improves the scene description first (open ground, landmarks, palette, no characters), then generates, QA-checks and logs. Use when the user types /pga-bg."
argument-hint: "<scene idea> [--ref background.png] [--draft] [--cheap] [--dry]"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-bg

User's request: **$ARGUMENTS**

Read: `R/references/library/house_rules.md`, `R/references/library/backgrounds.md`.

- Default `create_image_pro`, profile `sizes.background` (640×256), seed, **`no_background: false`**,
  `style_image_url` = anchor `backgrounds`, `style_copy: ["outline","detail","shading"]`. Cost 25.
- `--cheap`: `create_image_pixflux` 320×200, `color_image_url` = anchor. Cost 1.
- `--draft`: pixflux preview only (1); prints the command for the full Pro job.

Template:
```
<look> battle background, side view, wide landscape, no characters, open flat <ground> along the
bottom third for fighters: <scene>, <2-4 landmarks>, palette of <3-4 colours>
```
Improve: clear flat ground along the bottom third (clutter to the middle/back); 2-4 landmarks;
one light story (moonlight, torches, a glowing portal…); muted palette so sprites read on top;
negatives `no characters, no people, no text, no UI`. Several regions = one call each, same anchor + seed.

QA: `qa.py <file> --opaque --anchor <anchor>`. Review: ground clear, horizon not too high, no
figures/text, edges don't cut a landmark.
