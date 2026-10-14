---
name: pga-prompt
description: "Improve any PixelLab prompt with the pixellab-game-art house style and show the better prompt, tool, size and cost - without generating anything. Detects the asset type. Use when the user types /pga-prompt."
argument-hint: "<any PixelLab prompt or idea>"
disable-model-invocation: true
model: haiku
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-prompt

User's prompt: **$ARGUMENTS**

Read `R/references/prompt_improver.md` §1-5, `R/references/library/house_rules.md` and the one
library file for the detected type (`characters`, `backgrounds`, `scenes`, `buildings`, `icons`,
`animation` + `pose_edits`, `vfx`). Use `pixellab.json` if present.

1. Detect the asset type → the command that would make it. If two fit, pick one and say why.
2. Check (§3) and rewrite (§4) with that category's template; cost from `R/references/costs.md`.
3. Show the §5 block and one line with the command to run it, e.g.
   `/pga-char <improved prompt> --ref <anchor>`.

Never call a PixelLab tool here (not even get_balance).
