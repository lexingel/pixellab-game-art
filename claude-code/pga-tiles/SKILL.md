---
name: pga-tiles
description: "Make terrain tilesets that autotile with PixelLab - top-down Pro Wang sets chained across several terrains (sea > beach > grass), platformer sets, hex/iso transitions - then downloads the sheet + corner metadata, paints a test map to check the seams and logs. Use when the user types /pga-tiles."
argument-hint: "<terrain> > <terrain> [> …]  |  platform: <material> + <top layer>  |  hex|iso: <a> to <b>  [--size 16|32|64] [--soft|--cliff] [--draft] [--dry]"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-tiles

User's request: **$ARGUMENTS**

Read: `R/references/library/ui_tiles.md` (section "Terrain tilesets").

| Kind | Tool | Cost |
|---|---|---|
| Top-down terrain (default) | `create_topdown_tileset(mode="pro")` | 15 at 16/32 px, 25 at 64 |
| Platformer | `create_sidescroller_tileset` (`lower_description` = platform, `transition_description` = top layer; `base_tile_id` chains). Pro platformer sets are website-only so far | 2-3 |
| Hex / iso / oblique transition | `create_tiles_pro(tile_feature="tileset", tile_type=…)` - describe it as "grass to water" (Tier 1+) | ~3 |
| Loose ground variants (no autotiling) | `create_tiles_pro`, numbered list `1). … 2). …` | ~3 |
| Roads / walls + floors | `create_path_tiles` / `create_building_kit` (Tier 1+) | - |

**Chain** `a > b > c` = one tileset per pair, in order. Submit the first; its result gives the base
tile ids; the next set's `lower_base_tile_id` = the previous set's **upper** base tile id, and its
`lower_description` repeats that terrain's words exactly. Submit each set when the one before it
has finished (tested path). Terrains that never touch don't need a set (sea never meets grass here).

**Settings** (pro): `tile_size` profile or `--size` (32 default) · `transition_size 0.25` (16 tiles;
0.5/1.0 make 25-tile cliff sets that need the wall rule in the engine) · `boundary_amplitude 0.15`
(a natural meandering edge; 0 = straight) · `step_slope` 0 cliff (`--cliff`) … 1 soft bank (`--soft`,
the default for land) · `view "high top-down"` · a `transition_description` for the edge strip
("wet sand with a thin line of white foam"). `--draft` = the same call with `mode="standard"`
(1-4 gens) first.

Improve: each terrain = one material + one detail, colours from the profile; no objects, no
characters (they'd repeat on every tile).

**Download + QA:** `python R/scripts/fetch.py <tileset_id> <out>/<lower>_<upper>.png --tileset --log …`
(saves the sheet and its `.json` corners), then
`python R/scripts/tileset_preview.py <out>/map.png <sheet1.png> <sheet2.png> …` (chain order) and
look at `map.png` once (no seams, no banding, the shared terrain looks the same on both sides) and
at `map_tiles.png`: the two diagonal tiles `0110` / `1001` are the weak ones (random maps rarely use
them) - a broken or thin bank there → re-run that set with another `boundary_seed` or
`connect_diagonals: true`.

**Engine:** godot → read the MCP resource `pixellab://docs/godot/wang-tilesets` (PixelLab's
converter to a TileMapLayer terrain set; paint with the Rect tool) and run it for the user. Any
engine: place tiles by `corners` (NW/NE/SW/SE) and cut them by `bounding_box` - never by the `wang_N`
name or `original_position`. Report as in §8 with the base tile ids (needed to extend the chain later).
