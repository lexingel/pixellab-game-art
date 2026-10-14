---
name: pga-icon
description: "Make pixel-art item, skill, status or relic icons (and rare/epic variants) with PixelLab in the pixellab-game-art house style - improves the description first, generates at 64 px for a clean downscale, QA-checks and logs. Use when the user types /pga-icon."
argument-hint: "<icon idea> [--size 32|40|64] [--tiers] [--ref icon.png] [--dry]"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-icon

User's request: **$ARGUMENTS**

Read: `R/references/library/house_rules.md`, `R/references/library/icons.md`.

- Generate at profile `icon_gen` (64), box-downscale to `icon_final` (40 items / 32 skills) so
  pixels stay whole. `create_image_pixflux` (1) for sets; `create_image_pro` ~40 px (10-15, many
  candidates) to match a polished set. `no_background: true`, seed, style ref = **one** icon
  (anchor `icons`; a grid of icons makes Pro wrap candidates across corners).
- Template: `pixel art game icon, a single <object>, <material + 1-2 details>, centred, filling the
  frame, thick dark outline, strong highlight and shading, no frame, no square, no backdrop, no text`
- `--tiers`: rare = polished blue steel + silver + blue sapphire; epic = dark steel + ornate gold
  filigree + glowing violet gem, faint violet glow - via `edit_image_pro_flash`
  `Same <item>, same shape, size and position, upgraded to a <rare|epic> version: … Transparent background.` (5 each)
- Many icons → use `/pga-batch` (one sheet, one wait).

Improve: one object, silhouette first; class/school colour family for skill icons; say what it
must NOT be when ambiguous ("a lion-head shield, NOT a lion").

QA at the final size: downscale first (Pillow `Image.BOX`), then `qa.py`, then look.
