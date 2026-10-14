# pixellab-game-art: an agent skill for any AI coding agent

Pixel-art game assets with PixelLab (sprites, battle backgrounds, buildings, icons, padded wind-up →
hit attack animations, 8-direction moves, painted VFX), driven by your AI agent: Codex, Gemini CLI,
Cursor, GitHub Copilot, Claude Code or any other agent that can use MCP tools and read files.

It is the same skill as the Claude Code bundle, in the open **Agent Skills** format (a folder with a
`SKILL.md`) plus an `AGENTS.md` for agents that don't load skills.

## Easiest: let your AI assistant set it up

1. Download this folder (or `git clone` it) and open your AI assistant (Codex, Gemini CLI, Cursor, Copilot, OpenCode…) in it.
2. Say: **"Set up the PixelLab skill in this folder for me - follow SETUP_FOR_AI.md."**
3. It installs everything and checks it. The only things it asks of you: install Python if it's
   missing, get your PixelLab token (free account at https://pixellab.ai) and run **one** command with
   it, then restart the assistant in your game's folder.
4. Say **`pga-init`** (pick your art style), then **`pga-start`** - a guided first project that
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
   It copies the skill into `~/.agents/skills` (the shared Agent Skills folder) and installs the image
   packages (Pillow, numpy, scipy). Only one project? Run it from that project's folder with
   `--project` (also writes an `AGENTS.md` there). Run it again any time to update.
3. **Connect PixelLab** - get your token at https://api.pixellab.ai/mcp (signed in), store it in
   an environment variable (it then never sits in a config file), and add the server for your agent
   below. Restart the agent.
   - macOS / Linux: `echo 'export PIXELLAB_TOKEN=YOUR_TOKEN' >> ~/.zshrc` (or `~/.bashrc`), open a new terminal
   - Windows: `setx PIXELLAB_TOKEN "YOUR_TOKEN"`, open a new terminal

| Agent | Add the PixelLab server | Check it |
|---|---|---|
| **Codex** | `codex mcp add pixellab --url https://api.pixellab.ai/mcp --bearer-token-env-var PIXELLAB_TOKEN` | `codex mcp list` |
| **Gemini CLI** | in `~/.gemini/settings.json`: `"mcpServers": {"pixellab": {"httpUrl": "https://api.pixellab.ai/mcp", "headers": {"Authorization": "Bearer $PIXELLAB_TOKEN"}}}` | `/mcp` in Gemini |
| **Cursor** | in `~/.cursor/mcp.json`: `{"mcpServers": {"pixellab": {"url": "https://api.pixellab.ai/mcp", "headers": {"Authorization": "Bearer ${env:PIXELLAB_TOKEN}"}}}}` | Cursor Settings → MCP (green dot) |
| **VS Code / Copilot** | in `.vscode/mcp.json`: `{"inputs": [{"type": "promptString", "id": "pixellab-token", "description": "PixelLab token", "password": true}], "servers": {"pixellab": {"type": "http", "url": "https://api.pixellab.ai/mcp", "headers": {"Authorization": "Bearer ${input:pixellab-token}"}}}}` (asks for the token once) | MCP: List Servers |
| **OpenCode** | in `opencode.json`: `{"mcp": {"pixellab": {"type": "remote", "url": "https://api.pixellab.ai/mcp", "oauth": false, "headers": {"Authorization": "Bearer {env:PIXELLAB_TOKEN}"}}}}` | `opencode mcp list` |
| **Claude Code** | `claude mcp add --transport http --scope user pixellab https://api.pixellab.ai/mcp --header "Authorization: Bearer YOUR_TOKEN"` | `claude mcp list` |
| other | MCP server named `pixellab`, URL `https://api.pixellab.ai/mcp`, HTTP (streamable), header `Authorization: Bearer <token>` | the agent's MCP list |

   (Config formats as each tool documents them in Oct 2026; if a field name changed, PixelLab's
   https://pixellab.ai/mcp page and the tool's MCP docs have the current one. Already in the file?
   Add only the `pixellab` entry inside the existing `mcpServers` / `servers` / `mcp` block.)

**Check everything:** ask the agent `pga-doctor`. It checks the PixelLab connection and token, your
plan and balance, Python and packages, and prints the exact fix for anything missing.

**Agent doesn't see the skill?** It reads its own skills folder instead of `.agents/skills` - find it
in the agent's docs and run `python install.py --to <that folder>`. No skills support at all? Use
`--project`: the `AGENTS.md` it writes tells the agent where the skill is.

**PixelLab plan:** everything works on the free trial and every paid tier. Higher tiers run more jobs
at once (trial 1 · Tier 1 8 · Tier 2 10 · Tier 3 20) and unlock six tools (`animate_image_pixminimax`,
`inpaint_image`, `transfer_outfit`, `create_tiles_pro`, `create_path_tiles`, `create_building_kit`);
below that tier the skill uses a fallback by itself. Credits-only accounts count as the free tier.

**Cheaper models per task (optional):** add `--agent <name>` to the install command - `codex`,
`gemini`, `cursor`, `opencode`, `copilot` or `claude` - and it also adds one small subagent per task,
each on the model set for it in `models.json`: text-only tasks (help, prompt, style, feedback) on a
cheap/fast model or low effort, image-judging tasks on a standard one, `pga-anim` on your strongest.
Out of the box: Cursor `fast` for the light tasks, Codex reasoning effort low / medium / high,
Claude haiku / sonnet / inherit; the others use your current model until you put model names in
`models.json` (names differ per account) and run the installer again. Without `--agent` everything
runs on the agent's current model.

<details><summary>Manual install / details</summary>

- Copy the `pixellab-game-art` folder into your agent's skills folder (commonly `.agents/skills/` in a
  project or `~/.agents/skills/`; some agents use `.codex/`, `.gemini/` or `.cursor/` skills folders).
- MCP by hand: server name `pixellab`, URL `https://api.pixellab.ai/mcp`, HTTP (streamable) transport,
  header `Authorization: Bearer YOUR_TOKEN`. Your token is never asked for in the chat.
- Packages by hand: `python -m pip install pillow numpy scipy` (generation works without them; QA,
  cleanup and sheets don't).
- The first task of a session checks the setup by itself and prints the exact fix if something is missing.
</details>

## Use

Name a task or just describe the job:

```
pga-char boss: a drowned bell-ringer ghost
pga-anim knight.png overhead axe chop --draft
make me a 40px icon of a rusty iron helmet, rare and epic tiers
pga-tech explain pga-anim
```

<!-- pga:commands -->
| Task | Makes | Example |
|---|---|---|
| `pga-start` | a guided first project for PixelLab newcomers: three starter assets, explained step by step | `pga-start` |
| `pga-help` | this list of commands with an example each (free) | `pga-help` |
| `pga-init` | setup: your PixelLab plan, your art style (pick parameters or send a reference), saved under a name - run once per project | `pga-init` |
| `pga-style` | your saved art styles: list, switch, show, add a new one, approve a result as reference art | `pga-style anchor heroes last` |
| `pga-analyze` | reads your own art or GIF and turns its style into rules every command follows (free) | `pga-analyze art/hero_attack.gif --save hero-style` |
| `pga-prompt` | only improves a prompt and says which command to run (no cost) | `pga-prompt a goblin with a spear` |
| `pga-char` | hero / monster / boss / NPC sprite | `pga-char boss: a drowned bell-ringer ghost` |
| `pga-bg` | side-view battle background | `pga-bg flooded crypt with candles --draft` |
| `pga-scene` | hub backdrop, story picture, region map | `pga-scene story: the party camps under a dead tree` |
| `pga-building` | building or prop (+ upgrade tiers) | `pga-building blacksmith forge --tiers 3` |
| `pga-icon` | item / skill / status icons (+ rare/epic) | `pga-icon rusty iron helmet --tiers` |
| `pga-anim` | attack / skill animation: wind-up → hit | `pga-anim knight.png overhead axe chop` |
| `pga-vfx` | painted effect clip (free) | `pga-vfx ice spear hits one enemy` |
| `pga-batch` | many assets in one go, one review sheet | `pga-batch icons: helmet, boots, ring, amulet` |
| `pga-doctor` | checks the PixelLab connection, plan, Python, packages and project; prints the fix (free) | `pga-doctor` |
| `pga-feedback` | your choice about sharing results to improve the skill: status, on/off, preview, forget | `pga-feedback preview` |
| `pga-history` | past generations: what, when, cost, verdict, files; spend per command and day (free) | `pga-history 20 --cost` |
| `pga-reroll` | re-run a past result with a new seed or one wording change | `pga-reroll last no cape` |
| `pga-tech` | explains why the skill does something, or walks through how it does a task step by step (free) | `pga-tech explain pga-anim` |
<!-- /pga:commands -->

Flags work in plain text: `--dry` (show the calls and cost, generate nothing), `--draft` (1-generation
preview), `--n 3`, `--ref <image>`, `--size WxH`, `--max-cost N`, style and animation flags
(`references/parameters.md`).

**Every task:** prints each PixelLab call (tool and settings - full JSON with `--verbose`) with the cost and wait time before it runs,
runs without asking for permission, never repeats a call (reuses logged jobs), and ends with a results
table - generations per call, total vs estimate, balance before → after, files. Output goes to
`pixellab_out/<task>/<name>/` with a `log.jsonl` (or the `out` folder in `pixellab.json`).

## Your first ~20 generations

PixelLab bills in **generations**: your plan's monthly allowance (pay-as-you-go credits only kick in
when it runs out). Every command shows the cost before it runs; `pga-history --cost` shows what you spent.

| Step | Try | Costs | Takes |
|---|---|---|---|
| 1. See what would happen | `pga-char a goblin with a spear --dry` | 0 | instant |
| 2. Check the layout cheaply | `pga-char a goblin with a spear --draft` | 1 | under a minute |
| 3. The real sprite | `pga-char a goblin with a spear` | ~6 | 7-15 min |
| 4. Make it the reference for all monsters | `pga-style anchor monsters last` | 0 | instant |
| 5. A matching icon (you pick from many candidates) | `pga-icon rusty spear` | ~10 | 1-10 min |
| 6. Not quite right? Change one thing | `pga-reroll last shorter spear` | same as before | same |

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

Anything else: `pga-tech explain <word>`.

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

## Privacy: sharing results (opt-in, off by default)

Every job's outcome (QA flags, kept / re-rolled / rejected, your reason) is written to the local
`log.jsonl` - that stays on your machine. You can choose to share outcomes with the skill's authors
so the skill learns from more than one project (setup question 5, or `pga-feedback on stats|prompts`):

| Level | Sent after each run |
|---|---|
| `off` (default) | nothing |
| `stats` | task, tool, numeric/enum settings (size, seed, frames, mode), style summary (setting, density, view, outline, shading, colours), cost vs estimate, time, QA flags, keep/re-roll/reject, skill version, agent name, plan tier |
| `prompts` | `stats` + your prompt text and your reason when you reject or re-roll a result |

Never sent at any level: your PixelLab token, file paths, URLs, uploads, images, your game's name or
PixelLab job ids (each job goes as a one-way hash, so a changed verdict replaces its record). At the
`prompts` level your prompt text is sent as typed - **it can contain names you wrote** (characters,
places), so use `stats` for secret projects. Only jobs made **after** you opt in are sent.
Records carry a random id per machine (`~/.pixellab-skill/id.json`); `pga-feedback forget` deletes
everything that id sent, switches sharing off and starts a new id; `pga-feedback preview` shows exactly
what would go out. `PIXELLAB_SKILL_NO_TELEMETRY=1` blocks sending on a machine whatever the projects say.
Data goes to a Cloudflare Worker run by the skill's authors, is used only to improve the skill's
prompts, settings and pitfall notes, and is not sold or shared.

**What happens with shared data - weekly, for everyone.** Once a week the authors review what was
shared and fold the lessons (prompts that work, settings that fail, new pitfalls) back into the skill as
an update for all users. Each weekly update's CHANGELOG entry says what changed because of shared
results and how many shared jobs it was based on. Raw records are never published - only the lessons.

## Differences from the Claude Code version

- No slash-command menu; the agent reads the task file when you name it. Per-task models come from
  `install.py --agent <name>` (subagents + `models.json`) instead of command headers.
- Tool names may carry your agent's prefix for the `pixellab` server; the skill refers to them by
  their PixelLab names (`create_image_pro`, `animate_image`, …).
- Running the Python scripts may need your agent's usual approval for shell commands.
