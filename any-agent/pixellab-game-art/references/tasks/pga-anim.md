# Task pga-anim

Run when the user asks for `pga-anim` (with or without a slash) or describes this job in plain words.
Input: <sprite.png> <move, e.g. "overhead axe chop"> [--frames 11] [--timing light|heavy|even|custom] [--fps 12] [--fx crescent|streak|none|keep] [--hit N] [--loop] [--face left|right] [--canvas WxH] [--dirs 1|8] [--dry]

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's request: **(the user's request)**

Read: `<skill>/references/animation.md`, `<skill>/references/library/pose_edits.md` (§ current house style
only). The sprite file is required - if missing, ask (the only question).

## Parameters (flags > profile `anim` > defaults; `<skill>/references/parameters.md`)

- `--frames N` (11): check it fits - `frame_count` = N-1 must be even 4-16 and W×H×(N-1) ≤ 524,288;
  N even → generate one more and drop the weakest in-between; too many for the canvas → say the max.
  Cost of the swing = ceil(W×H×(N-1) / 65,536). Same N for every move of one character.
- `--timing` light (default) / heavy / even (`--fps`) / custom (`--durations`, e.g. from `/pga-analyze`):
  passed to `make_sheet.py` (`--beat light|swing`, `--fps`, `--durations`) and `preview_gif.py`
  (`--beat light|heavy|even`, `--fps`, `--durations`).
- `--fx` crescent (weapon cuts, default for blades) / streak (`recolor_trail.py --to <element>`) /
  none (scrub everything, default for shots) / keep (leave the generator's effects).
- `--hit N` → `make_sheet.py --hit N`; `--loop` → `first_frame_url` = `last_frame_url` = the sprite, no key poses.
- `density` low/mid: scale the canvases below by the sprite's size (canvas ≈ 2× its width, +28% height for overhead).
- `--dirs 8` (top-down games): follow `<skill>/references/animation.md` → "8 directions" instead of the plan below -
  front-facing edit (whatever the reference faces becomes south) → `create_character` v3 rotations (check all 8)
  → offer the cheap route (`animate_character` v3, one call per direction, aim named in screen terms, never
  "forward"; billed on the generated canvas, ~7/direction for a 96×200 sprite) or the exact route (key poses per
  direction, ~18) with the cost of each → 5 directions + 3 mirrored → `find_muzzle.py` + `dir8_finish.py` → a
  sheet per direction. Recommend 64-128 px characters for 8 directions (1-3 per direction).

## Plan (show it - prompt_improver §5)

- **Canvas** - the cheapest that fits the move (Pro Flash bills by the longest side):
  - overhead swings, slams, leaps, spells cast upward → **room above**: 192×256 (heroes ≤100 px wide)
    or 256×256 (bigger sprites). Poses cost 9 each.
  - thrusts, lunges, throws, bow shots, bashes, sweeps at waist height → **room in front only**:
    192×200 (or ≤200 tall) - poses cost 6 each, **≈30% cheaper**.
  - **shots (guns, bows, wands)**: 192×200, pose A = the aim, pose B = the recoil, no crescent swing;
    energy weapons: name the flash colour in the action (else it paints an orange gunpowder flash),
    `scrub.py … --clear-right <tip x>` for the generator's own flash, muzzle flash from `vfx_workbench` `muzzle_flash`
    (`preview_gif.py … --vfx <export>.png --vfx-at <tip> --vfx-on 1`), `make_sheet.py --hit 1` (`<skill>/references/animation.md` → "Shots"). **18**.
  Free space on the side the sprite faces (profile `facing`). Record the pad offset.
- **Look line**: who + 2-3 identifying colours/props (from looking at the sprite once).
- **Pose A (wind-up)**: a real coil - where the weapon/fist ends up and how far the torso turns. Never the standing pose.
- **Pose B (hit)**: the follow-through.
- **Dynamic layer on both** (Pro-quality poses from Pro Flash - `<skill>/references/animation.md` → "The dynamic layer"):
  `dynamic exaggerated pose`, stance depth (wind-up: "deep low stance, knees bent, weight on the back foot";
  hit: "extremely deep lunge, front knee bent low, back leg stretched straight"), torso lean/twist, and the
  character's soft parts (tabard, cape, robe, hair) "flaring with the motion".
- **Action**: motion only, one short line. Never add "no effects / no white lines" - it makes flashes worse.
- Edit template: `The same <look>, <pose core>, dynamic exaggerated pose: <stance>, <torso>, <secondary motion>, <facing>. Same size, same colours and pixel style, feet in the same place, no background.`
- Tool: Pro Flash (default). Pro `edit_image` (~10/pose, same text) for showpiece moves or a move that
  still flashes after one swing re-roll - its in-betweens are cleaner.
  (`back foot in the same place` for lunges.)
- Swing: `frame_count: 10` (smooth). Weapon swings also get a 6-frame swing of the same poses to
  harvest the crescent slash.
- Cost = 2 × (6 or 9) + 10-frame swing (6 at 192×200, 8 at 192×256) + 6-frame swing for a weapon
  crescent (4 / 5): **31** for an overhead melee move at 192×256, **22** at 192×200, **26** non-weapon.

## Run

1. `python <skill>/scripts/pad_sprite.py <sprite> <out>/pad.png <W> <H> <x>` → offset.
2. `get_upload_url`, `python <skill>/scripts/upload.py <url> <out>/pad.png`.
3. Both `edit_image_pro_flash` calls in the same turn (`use_color_palette_correction: true`,
   `no_background: true`); `fetch.py --jobs` both with `--log`.
4. `qa.py A.png B.png --anchor <sprite>`; half-size sheet of sprite | A | B. Re-roll a pose once
   for a hard defect (prompt_improver §8): it reads as standing, a prop changed hands/sides or
   appeared. Colour drift is not a re-roll - fix it with `apply_palette.py`.
5. `animate_image(first_frame_url=A, last_frame_url=B, frame_count=10, no_background=true, action=…)`
   → `fetch.py <job> <out>/raw10 --frames 11 --log …`; weapon swings also `frame_count=6` → `<out>/raw6 --frames 7`.
   If the 10-frame swing invents a pose that is in neither key pose, use the 6-frame one (or re-roll once).
6. `qa.py <out>/raw10/*.png --anim --sheet <out>/flagged.png` → look at the flagged sheet and one half-size
   sheet of all frames. **Keep every good frame.** Same-hue streaks: `recolor_trail.py <out>/raw10 1 … 9 --hue <hue>
   --to none --ref <sprite>`; off-palette flashes: `scrub.py <out>/raw10 <frames> --keep-main`.
   Weapon swings: `scrub.py <out>/raw6 3 4 --keep-main`, `slash_layer.py extract <out>/raw6/3.png <out>/raw6/3_s.png
   <out>/crescent.png --to air` (+ frame 4 → follow-through), then `slash_layer.py apply <frame> <out>/crescent.png
   <out> --behind` on the mid-cleave frame, `--fade 0.3` on the next, the follow-through on the one after
   (`<skill>/references/animation.md` → "Swing length, timing and the slash").
7. Ground the feet: `ground_snap.py <sprite> X,Y <frames> --check`, then without `--check` if any frame floats.
8. Export with light holds: `make_sheet.py <out>/<name> <frames> --beat light --pad X,Y --facing <dir>`
   (+ `--godot` if profile engine is godot) and `preview_gif.py <out>/<name>.gif <sprite> <picked> --offset X,Y`.
9. Report: sheet + JSON (+ .tres), GIF, pad offset, what was dropped/scrubbed, generations used.
