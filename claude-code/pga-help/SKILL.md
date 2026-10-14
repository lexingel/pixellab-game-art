---
name: pga-help
description: "List the pixellab-game-art slash commands with one example each, and how to start. Use when the user types /pga-help."
argument-hint: "[command]"
disable-model-invocation: true
model: haiku
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). This command makes nothing, so it doesn't need the
shared generation loop - read only the files named below.

# /pga-help

Asked about: **$ARGUMENTS**

Print this (or, if a command was named, just its row plus its argument hint and 2 examples):

| Command | Makes | Example |
|---|---|---|
| `/pga-start` | a guided first project for PixelLab newcomers: three starter assets, explained step by step | `/pga-start` |
| `/pga-help` | this list of commands with an example each (free) | `/pga-help` |
| `/pga-init` | setup: your PixelLab plan, your art style (pick parameters or send a reference), saved under a name - run once per project | `/pga-init` |
| `/pga-style` | your saved art styles: list, switch, show, add a new one, approve a result as reference art | `/pga-style anchor heroes last` |
| `/pga-analyze` | reads your own art or GIF and turns its style into rules every command follows (free) | `/pga-analyze art/hero_attack.gif --save hero-style` |
| `/pga-prompt` | only improves a prompt and says which command to run (no cost) | `/pga-prompt a goblin with a spear` |
| `/pga-char` | hero / monster / boss / NPC sprite | `/pga-char boss: a drowned bell-ringer ghost` |
| `/pga-bg` | side-view battle background | `/pga-bg flooded crypt with candles --draft` |
| `/pga-scene` | hub backdrop, story picture, region map | `/pga-scene story: the party camps under a dead tree` |
| `/pga-building` | building or prop (+ upgrade tiers) | `/pga-building blacksmith forge --tiers 3` |
| `/pga-icon` | item / skill / status icons (+ rare/epic) | `/pga-icon rusty iron helmet --tiers` |
| `/pga-anim` | attack / skill animation: wind-up → hit | `/pga-anim knight.png overhead axe chop` |
| `/pga-vfx` | painted effect clip (free) | `/pga-vfx ice spear hits one enemy` |
| `/pga-batch` | many assets in one go, one review sheet | `/pga-batch icons: helmet, boots, ring, amulet` |
| `/pga-doctor` | checks the PixelLab connection, plan, Python, packages and project; prints the fix (free) | `/pga-doctor` |
| `/pga-feedback` | your choice about sharing results to improve the skill: status, on/off, preview, forget | `/pga-feedback preview` |
| `/pga-history` | past generations: what, when, cost, verdict, files; spend per command and day (free) | `/pga-history 20 --cost` |
| `/pga-reroll` | re-run a past result with a new seed or one wording change | `/pga-reroll last no cape` |
| `/pga-tech` | explains why the skill does something, or walks through how it does a task step by step (free) | `/pga-tech explain /pga-anim` |

Flags for every generating command: `--dry` (show the improved prompt and cost only), `--draft`
(1-generation preview first), `--ref <image>` (match this asset), `--n 3` (variations), `--size WxH`,
`--style <name>` (one of your saved art styles for this call).
Style: `--setting scifi|cozy|western|…` `--density low|mid|high` `--colors 16` `--palette <file|hex,…>`
`--outline dark|selective|none` `--shading flat|soft|detailed` `--dither` `--light top-left` `--view side|top-down|iso`.
Animation: `--frames 9` `--timing light|heavy|even|custom` `--fps 10` `--fx crescent|streak|none|keep` `--hit N` `--loop` `--dirs 8` (top-down: rotate + 8 facings).
All of them can be saved as project defaults (`/pga-init`, `/pga-analyze`); every value is listed in the
skill's `references/parameters.md` (full path: R/references/parameters.md - print R expanded).
Start with `/pga-init` (or `/pga-analyze <your art>`), then `/pga-prompt` to see how your ideas get improved for free.
No profile yet? The first generating command starts the `/pga-init` setup (plan, art style, a name to save it under), then does your request.
Every command prints each PixelLab call with its parameters and the cost before it runs, never asks for permission, and ends with a results table (generations used, balance before → after, files).
Costs per tool: `R/references/costs.md`. Don't call any PixelLab tool from this command.
