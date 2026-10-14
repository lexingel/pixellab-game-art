# Task pga-vfx

Run when the user asks for `pga-vfx` (with or without a slash) or describes this job in plain words.
Input: <effect idea, e.g. "ice spear hits one enemy, blue"> [--face left|right] [--dry]

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's request: **(the user's request)**

Read: `<skill>/references/vfx.md`, and the one template you pick from `<skill>/assets/vfx_templates/`.

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
