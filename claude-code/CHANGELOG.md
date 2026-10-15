# Changelog

## 1.4.0 - 2026-10-15

**Skill**
- `/pga-tiles` (new): terrain tilesets that autotile - top-down Tileset Pro chained across terrains
  (`sea > beach > grass`), platformer sets, hex/iso/oblique transitions. Downloads the sheet and its
  corner data (`fetch.py --tileset`), paints a test map (new `tileset_preview.py`), sets it up in
  Godot with PixelLab's terrain converter.
- `/pga-normal` (new): normal maps so an engine can light sprites and animations. New `normal_map.py`
  packs frames into the GIF the tool reads, cuts the result into `<frame>_n.png` and lights it from
  three sides to check it.
- Engine notes for tilesets and normal maps (Godot, Unity, Phaser, Unreal); costs table gains both.
- Repo page: example art from every kind of command, a "Start here" for people new to AI assistants
  and PixelLab, and a "Keeping up with PixelLab" note.

**PixelLab updates (0.4.130)** - what PixelLab changed and what the skill does with it
- *Tileset Pro* (top-down): `create_topdown_tileset(mode="pro")`, 16/32/64 px, 15 generations at
  ≤32 px, 25 above; new border controls (roundness, meandering edge, bank slope, joined diagonals);
  connects to other sets through base tile ids. → `/pga-tiles` uses it by default.
- *Tileset Pro* (sidescroller): website only so far - not in the MCP tools or the API. → `/pga-tiles`
  uses the standard platformer tool until it is.
- *Target palette* for Create Image Pro: `palette` (hex list) - every pixel of the result is one of
  those colours. → noted in the API guide; more tools are getting it soon, per PixelLab.
- *VFX* in the MCP tools (`vfx_workbench`) - `/pga-vfx` already used it. No REST endpoint yet.
- *Normal maps* in the Creator, MCP and API (`create_normal_map`, 0.5 generation). → `/pga-normal`.

**What we learned** (tested 2026-10-15, 31.5 generations)
- Tileset Pro at 32 px costs exactly 15. A second set chained with the first set's *upper* base tile
  id and the same words for the shared terrain matched it - no seam between beach and beach.
- `step_slope 1` gives a soft earthy bank; 0 is a cliff edge.
- Check the two diagonal tiles (`0110`, `1001`): one came out as a thin broken bank while the test map
  looked fine, because random maps rarely use diagonals. Re-run with another `boundary_seed`.
- Tiles are placed by their corners and cut by `bounding_box`; the `wang_N` name is not a position.
- Normal maps: 0.5 per call, whether it's one sprite or 11 frames. The tool reads an animation from
  a GIF; a PNG strip counts as one image (and is refused over 1024 px).
- One call plans the shapes on the first frame: when the pose changes a lot (an attack's crouch),
  the later frames get horizontal bands. The same frames sent on their own came out clean - split
  clips where the pose changes.

## 1.3.2 - 2026-10-15
- Kick recipe for a cartoon reference (convert, pad, 3 short clips) and the double-kick pitfall in `references/animation.md`.

## 1.3.1 - 2026-10-15
- Hit reaction recipe (one peak pose + two 6-frame clips, ~33 gens) in `references/animation.md`.
- New `scripts/colormatch.py`: removes the brightness/colour shift generated poses get (matches each frame to the
  standing sprite, then snaps to its colours). Also noted: yellow swipe flashes can appear even on clean poses.

## 1.3.0 - 2026-10-14
- `/pga-update`: gets the weekly update and merges it into your install - backs up the old one, installs
  the new one with the same options (and your models.json picks), keeps skill files you edited and has
  your assistant merge any file both you and the update changed. `/pga-update check`, `/pga-update undo`,
  `/pga-update from <zip>` for offline installs.
- The setup check says once a week when a newer version is out (`PIXELLAB_SKILL_NO_UPDATE_CHECK=1` turns it off).
- Installers record what they installed (`.install.json`) so updates can tell your edits from the old version.

## 1.2.1 - 2026-10-14
- Data sharing stays consent-only (off by default). New: shared results are reviewed weekly and their
  lessons released to all users as a skill update; each weekly entry here says what changed because of
  shared data and how many shared jobs it came from. Raw records are never published.

## 1.2.0 - 2026-10-14
Built for people who have never used PixelLab.
- "Let your AI assistant set it up": SETUP_FOR_AI.md walks any assistant through installing, connecting
  PixelLab and checking it; the user only installs Python if missing and runs one command with their token.
- `/pga-start`: a guided first project - three starter assets that fit the chosen style, a 1-generation
  draft before each, a plain sentence at every step, and a wrap-up of what was spent and what to try next.
- Beginner mode (asked at setup, on by default; `/pga-start off`): short explanations and drafts first.
- Every job ends with a plain summary - what was made, how it looks, cost and what's left, the next
  steps as exact commands; the detailed table with `--verbose` or for batches.
- Plain-language error guide (references/errors.md) for connection, token, balance, tier, failed,
  slow and flagged jobs; `profile.py` for project settings.

## 1.1.0 - 2026-10-14
Easier first ten minutes, more control after.
- Shorter setup: plan, art style (reference image, or setting + pixel size + view; "advanced" for
  colours, outline, shading, light, dithering), engine (default: just PNGs), output folder, sharing.
  Unanswered = default; typos get one question with the closest options; pixel size defaults to mid.
- Compact output: one line per PixelLab call (tool + settings), full JSON with `--verbose`; the plan
  line shows the expected wait ("starts now, ~10 min").
- New `/pga-history` (past jobs, cost, spend per day/command) and `/pga-reroll` (redo a result with a
  new seed or one wording change); `/pga-style anchor <family> <image|last>` approves a result as the
  reference art for its kind.
- README: "Your first ~20 generations" walkthrough with costs and waits, a glossary, and import notes
  for Godot, Phaser, Unity, GameMaker and others.
- Non-generating commands no longer load the shared generation instructions (less context, cheaper).

## 1.0.0 - 2026-10-14
First versioned release (everything before this was unversioned work on one game).
- 16 commands: init, style, analyze, prompt, char, bg, scene, building, icon, anim, vfx, batch,
  doctor, feedback, tech, help. Same skill as an Agent Skills package for Codex, Gemini CLI,
  Cursor, Copilot, OpenCode (`pixellab-agent-skill`), with per-task models via `install.py --agent`.
- Setup conversation (`/pga-init`): plan tier, art style from parameters or a reference image,
  engine, output folder, sharing choice; several named art styles per project (`/pga-style`, `--style`).
- Every PixelLab call shown with its parameters and cost; no permission prompts; no repeated calls;
  a results table with generations used and balance before → after.
- Plan tiers: parallel-job limits and fallbacks for the six Tier-1+ tools.
- Opt-in sharing of job outcomes (`/pga-feedback`), off by default; `/pga-doctor` setup check;
  `/pga-tech` explanations; one-command install / uninstall.
