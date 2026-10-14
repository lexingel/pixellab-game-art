---
name: pga-analyze
description: "Analyse a user's own pixel art (PNG, GIF or a folder) - pixel scale, density, palette, colour count, outline, shading tones, dithering, light, and for GIFs frame count, timing, holds and motion - then turn it into style rules saved in pixellab.json so every /pga-* command replicates that style. Use when the user types /pga-analyze."
argument-hint: "<image.png | anim.gif | folder> [--save <name>] [--as heroes|monsters|backgrounds|scenes|buildings|icons|ui] [--anim-only | --style-only]"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-analyze

User's input: **$ARGUMENTS**

No PixelLab generation here (free). If no file/folder was given, ask for one (the only question).

1. **Measure** (no image reading yet):
   `python R/scripts/analyze_style.py <path> --out <out>/style_analysis`
   It prints scale, density, colours, outline, dithering, light and, for GIFs, frames/timing/holds/
   motion/ground drift; it writes `analysis.json`, `palette.png`, `native/` (1 px = 1 pixel) and `look.png`.
2. **Look once** at `look.png` (and `palette.png` if colours matter). Read only what numbers can't
   tell: setting/genre, mood, materials, proportions (chibi / heroic / realistic), view and facing,
   outline colour, how effects are drawn, what the animation does on its holds.
3. **Write the rules** - map the measurements with `R/references/parameters.md`:
   - `setting` (nearest preset, or free words), `density` (from subject height), `view`, `facing`
   - `colors` = significant colour count (round up to 8/16/24/32/48/64), `palette_hex` = the measured palette
     (only if the user wants their exact colours - ask once if unsure), `outline`, `shading`
     (tones per ramp ≤2 flat, 3 soft, ≥4 detailed), `dither`, `light`
   - `sizes` scaled from the measured subject size (keep the user's own proportions)
   - GIF: `anim.frames` = frame count; `anim.timing` = `custom` with `durations_ms` when holds exist,
     else `even` with `fps`; `anim.loop`; note ground drift > 2 px as "feet stay on one line" if the
     user's art keeps them steady
   - 3-8 plain-language `rules` that a prompt can follow, each specific and checkable, e.g.
     "1 px near-black outline", "max 16 colours", "3 tones per colour, no dithering",
     "light from top-left", "chunky proportions, head ~1/3 of the height",
     "attacks: 7 frames, 300 ms hold on the hit, 80 ms elsewhere"
   - `anchors.<family>` = a `native/` frame (≤256 px) when `--as` is given or it is clearly one family
4. **Show** a table: rule | measured from | value, then `Reply: save <name> · change <field> <value>`.
   `--save <name>` (or the user's "save <name>") writes the rules (with `"analysed_from": "<path>"`)
   to `<out>/style_draft.json` and runs `python R/scripts/style.py save <name> --from <out>/style_draft.json`
   (add `--use` if they want it active) - a named style, next to any others. To update an existing
   style, save under its name (it is replaced). `--anim-only` / `--style-only` limit what is written.
5. **Prove it** (optional, offer it): `/pga-prompt <a subject in their game>` shows how the new rules
   change a prompt (free); a `--draft` of one sprite costs 1.

Upscaled art (scale > 1) is measured at its native size; tell the user their art is drawn at N×.
Photos or painted (non-pixel) art: say the colour count is very high and the result is an
approximation - suggest `colors` 32 and `outline dark` as a starting point.
