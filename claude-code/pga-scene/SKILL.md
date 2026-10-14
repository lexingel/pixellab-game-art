---
name: pga-scene
description: "Make a hub/menu backdrop, story/cutscene picture or region map in pixel art with PixelLab in the pixellab-game-art house style - improves the description first, then generates, QA-checks and logs. Use when the user types /pga-scene."
argument-hint: "<scene idea> [backdrop|story|map] [--ref image.png] [--draft] [--dry]"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-scene

User's request: **$ARGUMENTS**

Read: `R/references/library/house_rules.md`, `R/references/library/scenes.md`.

| Kind | Tool | Size | Notes |
|---|---|---|---|
| Hub / menu backdrop | `create_image_pro` | 624×392 (Pro max 16:10 ≈ 632×424) | keep UI/button areas calm |
| Story / cutscene picture | `create_image_pro` | 288×120 or 640×272 | one moment, one focal subject |
| Region map | `create_image_pro` | 640×400 | top-down, readable paths, no labels |

Profile seed, `no_background: false`, style ref = anchor `scenes`. Cost 15-25. `--draft` = pixflux first.

Improve: one moment, one focal point, fore/mid/background; light story (warm vs cold); for
backdrops say where empty space must be; negatives `no text, no letters, no UI, no frame` (+`no labels` for maps).
Clean plate for clickable props: generate the scene, then edit "the same room, empty, without <props>".
Panoramas merge buildings - make each with `/pga-building`.

QA: `qa.py <file> --opaque --anchor <anchor>`.
