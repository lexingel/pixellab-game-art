# pixellab-skills - pixel-art game assets with Claude + PixelLab

A main skill (`pixellab-game-art`) and a set of `/pga-*` slash commands that turn short ideas into game-ready
pixel art with PixelLab: style-matched sprites, backgrounds, buildings and icons; attack and skill
animations made from two painted key poses; painted, timed VFX; automatic QA, cost tracking and
engine-ready spritesheets. Distilled from ~4,300 real PixelLab jobs on a dark-fantasy side-view game.

## Easiest: let your AI assistant set it up

1. Unzip the download and open your AI assistant **inside that folder** - it has to be "in" the folder
   to read the setup instructions:

   | You use | Do this |
   |---|---|
   | **Claude desktop app** (Code tab) | Start a new session and choose the `pixellab-skills` folder as the folder to work in. |
   | **Claude Code** in a terminal | Open a terminal in the folder (below), type `claude`, press Enter. |
   | **Codex CLI** / **Gemini CLI** / **OpenCode** | Open a terminal in the folder (below), type `codex` / `gemini` / `opencode`, press Enter. |
   | **Cursor** / **VS Code** (Copilot) | *File → Open Folder…* → pick the folder, then open the chat (agent) panel. |

   *Open a terminal in a folder:* **Windows** - open the folder in File Explorer, click the address bar, type
   `cmd`, press Enter. **Mac** - right-click the folder in Finder → *New Terminal at Folder*.

2. Copy this sentence into its chat and send it: **"Set up the PixelLab skill in this folder for me - follow SETUP_FOR_AI.md."**
3. It installs everything and checks it. The only things it asks of you: install Python if it's
   missing, get your PixelLab token (free account at https://pixellab.ai) and run **one** command with
   it, then restart the assistant in your game's folder.
4. Say **`/pga-init`** (pick your art style), then **`/pga-start`** - a guided first project that
   explains every step (about 15-20 generations).

Prefer to do it by hand? The three steps below are the same thing.

## Setup (3 steps, ~5 minutes)

1. **Python** - install Python 3.8+ if you don't have it: https://www.python.org/downloads/
   (Windows: tick "Add Python to PATH"). On macOS / Linux the command is usually `python3` - use it
   wherever this README says `python`.
2. **Install** - unzip, open a terminal in the unzipped folder and run:
   ```
   python install.py --pip
   ```
   It copies the skill and all commands into `~/.claude/skills` and installs the image packages
   (Pillow, numpy, scipy). Only one project? Add `--project` and run it from that project's folder.
   Run it again any time to update.
3. **Connect PixelLab** - get your token at https://api.pixellab.ai/mcp (signed in), then run once,
   with your token in place of `YOUR_TOKEN`:
   ```
   claude mcp add --transport http --scope user pixellab https://api.pixellab.ai/mcp --header "Authorization: Bearer YOUR_TOKEN"
   ```
   Restart Claude Code.

**First:** in your game's folder run `/pga-init` - it asks your PixelLab plan and your art style (pick
parameters or send a reference image), shows the setup and saves it under a name you choose. Add more
styles later with `/pga-style new`; pick one per job with `--style <name>`.

**Check everything:** type `/pga-doctor`. It checks the PixelLab connection and token (`claude mcp list`
should also show `pixellab`), your plan and balance, Python and packages, and prints the exact fix
for anything missing. Start Claude Code in your game's folder.

**Then:** `/pga-help` lists all commands. Try `/pga-prompt a goblin with a spear` (free) or
`/pga-char a goblin with a spear --dry` (shows the exact calls and cost, generates nothing).

The first command of a session checks the setup by itself (PixelLab connection, Python packages) and
prints the exact fix if something is missing. Your token is never asked for in the chat.

**PixelLab plan:** everything works on the free trial and every paid tier. Higher tiers run more jobs
at once (trial 1 · Tier 1 8 · Tier 2 10 · Tier 3 20) and unlock six tools (`animate_image_pixminimax`,
`inpaint_image`, `transfer_outfit`, `create_tiles_pro`, `create_path_tiles`, `create_building_kit`);
below that tier the skill uses a fallback by itself. Credits-only accounts count as the free tier.

<details><summary>Manual install / details</summary>

- Copy all the folders (`pixellab-game-art` and every `pga-*` folder) side by side into
  `~/.claude/skills/` (all projects) or `<project>/.claude/skills/` (one project).
- The MCP server must be named `pixellab` - the commands pre-approve `mcp__pixellab__*`, so they run
  without permission prompts.
- Packages by hand: `python -m pip install pillow numpy scipy` (generation works without them; QA,
  cleanup and sheets don't).
- `/pga-init` is also started by the first generating command in a project without `pixellab.json`.
- The slash commands are Claude Code features. In the Claude app (Settings → Capabilities → Skills)
  upload only the `pixellab-game-art` folder as a zip and ask for art in plain words.
- Other agents (Codex, Gemini CLI, Cursor, Copilot, …): use the `pixellab-agent-skill` package instead.
</details>

## Commands

<!-- pga:commands -->
| Command | Makes | Model |
|---|---|---|
| `/pga-start` | a guided first project for PixelLab newcomers: three starter assets, explained step by step | Sonnet |
| `/pga-help` | this list of commands with an example each (free) | Haiku |
| `/pga-init` | setup: your PixelLab plan, your art style (pick parameters or send a reference), saved under a name - run once per project | Sonnet |
| `/pga-style` | your saved art styles: list, switch, show, add a new one, approve a result as reference art | Haiku |
| `/pga-analyze` | reads your own art or GIF and turns its style into rules every command follows (free) | Sonnet |
| `/pga-prompt` | only improves a prompt and says which command to run (no cost) | Haiku |
| `/pga-char` | hero / monster / boss / NPC sprite | Sonnet |
| `/pga-bg` | side-view battle background | Sonnet |
| `/pga-scene` | hub backdrop, story picture, region map | Sonnet |
| `/pga-building` | building or prop (+ upgrade tiers) | Sonnet |
| `/pga-icon` | item / skill / status icons (+ rare/epic) | Sonnet |
| `/pga-anim` | attack / skill animation: wind-up → hit | your own model |
| `/pga-vfx` | painted effect clip (free) | Sonnet |
| `/pga-batch` | many assets in one go, one review sheet | Sonnet |
| `/pga-doctor` | checks the PixelLab connection, plan, Python, packages and project; prints the fix (free) | Haiku |
| `/pga-feedback` | your choice about sharing results to improve the skill: status, on/off, preview, forget | Haiku |
| `/pga-history` | past generations: what, when, cost, verdict, files; spend per command and day (free) | Haiku |
| `/pga-reroll` | re-run a past result with a new seed or one wording change | Sonnet |
| `/pga-update` | gets the weekly skill update and merges it into your install, keeping your own edits (free) | Haiku |
| `/pga-tech` | explains why the skill does something, or walks through how it does a task step by step (free) | Sonnet |
<!-- /pga:commands -->

Flags on generating commands: `--dry` (improved prompt, tool, size and cost only) · `--draft`
(1-generation preview before an expensive image) · `--ref <image>` · `--n 3` (variations) ·
`--size WxH`, plus style (`--setting --density --colors --palette --outline --shading --dither
--light --view`) and animation (`--frames --timing --fps --fx --hit --loop --dirs`) parameters. Every command prints each PixelLab call (tool and settings - full JSON with `--verbose`) and the cost and wait time up front, runs without asking, and ends with a results table (generations per call, total, balance before → after). Set `max_cost` in `pixellab.json` (or `--max-cost N`) to cap a run.

Cheaper models do the text-only work (Haiku) and the generating/reviewing (Sonnet); `/pga-anim`
keeps your own model because judging animation frames is where a stronger model pays off.

## What you get in each output folder (`pixellab_out/` by default)

- the images / frames, a half-size `sheet.png` and (if anything was flagged) `flagged.png`
- `log.jsonl` - one line per job: prompt, settings, job id, cost. `python
  ~/.claude/skills/pixellab-game-art/scripts/cost_report.py pixellab_out/log.jsonl` totals it.
- animations: `<name>.png` spritesheet + `<name>.json` (Aseprite format: frames + durations,
  plus pad offset, facing, hit frame) + `<name>.tres` for Godot when the profile says godot, and a preview GIF

## What's inside `pixellab-game-art`

- `SKILL.md` - rules, which tool for what, the animation and VFX house style, review, budget, licence.
- `references/prompt_improver.md` - the loop every command follows (setup check, profile, flags,
  prompt check and rewrite, generate, QA, report).
- `references/library/` - prompt templates, parameters, real example prompts and pitfalls, one file
  per asset type (backgrounds, scenes, buildings, characters, icons, ui_tiles, animation,
  pose_edits, vfx) + `house_rules.md`.
- `references/pixellab_api.md` - how the PixelLab MCP service works and which tool to use first
  for any asset (condensed from https://api.pixellab.ai/mcp/docs).
- `references/parameters.md` - every user parameter (setting presets, density, colours, outline,
  shading, view, frames, timing, effects) and which one wins when they conflict.
- `references/costs.md` - measured vs official generation costs for every tool.
- `references/animation.md`, `references/vfx.md` - the pipelines in detail; `references/stats.md`.
- `assets/vfx_templates/` - three complete effect recipes (strike, wave, eruption).
- `scripts/` - setup check, upload, fetch + log, cost report, pad, QA, scrub, contact sheet,
  preview GIF (with VFX overlay), spritesheet export, style analysis, palette enforcement,
  ground snap, trail recolour, slash layer, muzzle finder and an 8-direction finisher (`--dirs 8`:
  rotate a sprite into 8 facings, animate 5, mirror 3).

The example prompts use generic descriptions; swap in your own.

## Your first ~20 generations

PixelLab bills in **generations**: your plan's monthly allowance (pay-as-you-go credits only kick in
when it runs out). Every command shows the cost before it runs; `/pga-history --cost` shows what you spent.

| Step | Try | Costs | Takes |
|---|---|---|---|
| 1. See what would happen | `/pga-char a goblin with a spear --dry` | 0 | instant |
| 2. Check the layout cheaply | `/pga-char a goblin with a spear --draft` | 1 | under a minute |
| 3. The real sprite | `/pga-char a goblin with a spear` | ~6 | 7-15 min |
| 4. Make it the reference for all monsters | `/pga-style anchor monsters last` | 0 | instant |
| 5. A matching icon (you pick from many candidates) | `/pga-icon rusty spear` | ~10 | 1-10 min |
| 6. Not quite right? Change one thing | `/pga-reroll last shorter spear` | same as before | same |

Typical costs: a sprite 6 · an icon 10-15 · a battle background 25 · an attack animation 16-31 (two
poses + the frames between) · a painted effect 0. Waits are PixelLab's, not your machine's: the agent
says "starts now, ~10 min" and fetches the result when it's ready.

## Words used

| Word | Means |
|---|---|
| generation | one unit of your PixelLab allowance; each job costs a few |
| tier | your PixelLab plan level: how many jobs run at once, and six tools that need Tier 1+ |
| style | a saved set of choices (setting, pixel size, view, colours, outline…) under your own name |
| reference art (anchor) | an image you approved; every later job of that kind is matched to it |
| pixel size (density) | how tall a character is in pixels: low ~32, mid ~64, high ~180 |
| Pro / Pro Flash / pixflux | PixelLab's models: Pro = best, many candidates at small sizes; Pro Flash = near-Pro and cheaper (sprites, poses); pixflux = 1-generation drafts |
| key poses | the wind-up and the hit, drawn first; the animation is generated between them |
| padded canvas | empty space added around a sprite so a swing has room |
| in-between / splice | the generated frames between key poses; splicing joins two takes into a longer move |
| QA / scrub / ground snap | automatic checks before you see anything; removing stray off-colour pixels; keeping feet on one line |

Anything else: `/pga-tech explain <word>`.

## Using the files in your engine

Animations come as a PNG sheet (frames in a row) plus a JSON in Aseprite's format (frame boxes and
per-frame milliseconds); single images are plain PNGs. For crisp pixels in any engine: nearest-neighbour
(point) filtering, no compression, whole-number scaling.
- **Godot:** you also get a `.tres` SpriteFrames - drop it on an AnimatedSprite2D's *Sprite Frames*.
- **Phaser 3:** `this.load.aseprite('hero', 'hero.png', 'hero.json')`, then `this.anims.createFromAseprite('hero')`.
- **Unity:** import the PNG as *Sprite (2D and UI)*, *Sprite Mode: Multiple*, *Filter Mode: Point*,
  *Compression: None*; Sprite Editor → Slice → *Grid By Cell Size* = the frame size in the JSON; set
  each frame's time in the Animation clip from the JSON durations.
- **GameMaker:** Create Sprite → *Import Strip Image*, frame count and size from the JSON.
- **Defold, RPG Maker, others:** use the numbered frames (`0.png`, `1.png`, …) in the output folder, or the sheet + JSON.

## Updates (weekly)

The skill gets an update every week - the lessons from shared results, fixes and new commands. Your
assistant mentions it at most once a week when one is out. To get it: `/pga-update` (or
`python <skill>/scripts/update.py`). It backs up your install, installs the new version with the same
options as before and keeps any skill file you edited (if the update changed the same file, your
assistant merges the two). `/pga-update undo` goes back. Your `pixellab.json`, styles and generated
files are never touched. No internet / download blocked: download the repository ZIP and run
`/pga-update from <the zip>`.

## Privacy: sharing results (opt-in, off by default)

Every job's outcome (QA flags, kept / re-rolled / rejected, your reason) is written to the local
`log.jsonl` - that stays on your machine. You can choose to share outcomes with the skill's authors
so the skill learns from more than one project (setup question 5, or `/pga-feedback on stats|prompts`):

| Level | Sent after each run |
|---|---|
| `off` (default) | nothing |
| `stats` | task, tool, numeric/enum settings (size, seed, frames, mode), style summary (setting, density, view, outline, shading, colours), cost vs estimate, time, QA flags, keep/re-roll/reject, skill version, agent name, plan tier |
| `prompts` | `stats` + your prompt text and your reason when you reject or re-roll a result |

Never sent at any level: your PixelLab token, file paths, URLs, uploads, images, your game's name or
PixelLab job ids (each job goes as a one-way hash, so a changed verdict replaces its record). At the
`prompts` level your prompt text is sent as typed - **it can contain names you wrote** (characters,
places), so use `stats` for secret projects. Only jobs made **after** you opt in are sent.
Records carry a random id per machine (`~/.pixellab-skill/id.json`); `/pga-feedback forget` deletes
everything that id sent, switches sharing off and starts a new id; `/pga-feedback preview` shows exactly
what would go out. `PIXELLAB_SKILL_NO_TELEMETRY=1` blocks sending on a machine whatever the projects say.
Data goes to a Cloudflare Worker run by the skill's authors, is used only to improve the skill's
prompts, settings and pitfall notes, and is not sold or shared.

**What happens with shared data - weekly, for everyone.** Once a week the authors review what was
shared and fold the lessons (prompts that work, settings that fail, new pitfalls) back into the skill as
an update for all users. Each weekly update's CHANGELOG entry says what changed because of shared
results and how many shared jobs it was based on. Raw records are never published - only the lessons.

## Licence and PixelLab's terms

The skill files are free to share. Everything you generate falls under PixelLab's terms of service
(https://pixellab.ai/termsofservice) - notably, training AI models on PixelLab outputs isn't
allowed without PixelLab's written permission. Check the current terms before selling or
redistributing assets.
