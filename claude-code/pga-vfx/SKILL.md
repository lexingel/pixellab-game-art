---
name: pga-vfx
description: "Turn a short effect idea into a painted, outlined pixel-art VFX clip with PixelLab's free vfx_workbench in the pixellab-game-art house style (strike / wave / eruption templates, lit puffs, hold-fast-hold timing), exported with per-frame durations. Use when the user types /pga-vfx."
argument-hint: "<effect idea, e.g. \"ice spear hits one enemy, blue\"> [--face left|right] [--dry]"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-vfx

User's request: **$ARGUMENTS**

Read: `R/references/vfx.md`, and the one template you pick from `R/assets/vfx_templates/`.

## Spec (show it)

| Field | Decide (default) |
|---|---|
| Shape | **strike** (one target, 112×112, 12 f) · **wave** (across a group, 340×130, 14 f) · **eruption** (under each target, 100×136, 12 f) |
| Caster + facing | caster on the right → `mirror: "x"` (templates point right) |
| Beats | anticipation → launch → **peak hold** → break-up into embers / droplets / chunks / sparkles / motes |
| Ramp | one 6-stop `main` ramp near-black → highlight in the **caster's** colours (reuse one from vfx.md or the profile palette); optional accent ramp |
| Durations | the template's per-frame durations from vfx.md |

Shapes must read as the thing: a star = `rays`; something falling = path + ribbon + glow from
above; a stream = three overlapping cartoon `shape` streams, never one.

## Build (free)

1. `vfx_workbench(["start","--fps","12"], notes="<spec in one line>")`
2. `render` the template with the new ramp/layers (`tones 5, detail 0.1, shading lit, outline dark`).
3. Check frames `[2,5,8,10]` (the render returns them - that's the one look per iteration): the peak
   is the biggest, most solid frame; the last frames mostly empty; caster's colours; nothing reads
   as a box or a pipe. Patch and re-render only the frames you changed.
4. `export --name "<Caster> <Effect>"` (add `--game-pack` for an engine ZIP); download the sheet +
   JSON into the output dir with `fetch.py`-style plain downloads or the URLs the export returns.
5. Report: files, frame size × count, per-frame durations (ms at 12 fps) to put in the engine.

`--dry` stops after the spec and the recipe JSON you'd render.
