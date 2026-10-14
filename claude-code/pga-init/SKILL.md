---
name: pga-init
description: "Set up PixelLab for a project: asks the user's PixelLab plan tier, then their art style (pick parameters or send a reference image), shows the resulting setup, and saves it as a named art style in pixellab.json. Use when the user types /pga-init."
argument-hint: "[reference image or art folder] (optional)"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-init

User's input: **$ARGUMENTS**

The setup conversation. No generation unless the user asks for a draft. Questions are fine here
(it is setup); never ask permission for anything else.

**Adding a style to an existing project:** if `pixellab.json` already has `tier`, `engine` and `out`,
ask only question 2 (and 5 if `share` is missing), then steps 2-4 save the new style next to the
others (`style.py save <name> --from …`, `--use` only if the user says to switch to it).

**Step 1 - ask, in ONE message** (call `get_balance` first, free, and pre-fill what it shows):
```
Let's set up PixelLab for this project - one reply; "ok" keeps a [default].

1. Plan: I see <Tier N (name) | a free trial | credits only> - right? New to PixelLab? [yes] - then I
   explain each step in a sentence and show a 1-generation draft before bigger jobs (turn off any time).
2. Art style - A, B or C:
   A) a reference: the path to (or attach) an image or GIF of art you like - I copy its style
   B) pick three things:
      setting: dark-fantasy · high-fantasy · cozy · scifi · cyberpunk · steampunk · post-apoc ·
               modern · horror · western · or your own words ("frozen viking saga")
      pixel size [mid]: low (~32 px, NES feel) · mid (~64 px, SNES feel) · high (~180 px, detailed)
      view [side]: side (platformer / side battles) · top-down (Zelda-like) · iso
      e.g. "B: cozy, mid, top-down" - say "advanced" for colours, outline, shading, light, dithering
   C) both: "C: art/hero.png, but top-down"
3. Engine [none - just PNGs]: godot · unity · unreal · gamemaker · defold · phaser · rpg maker · other
4. Output folder [pixellab_out]: e.g. assets/sprites
5. Share results to improve the skill? [off] · off · stats (numbers only) · prompts (+ your prompt text). The lessons go back into the skill for everyone in a weekly update - /pga-feedback explains

Example reply:  1 ok, yes · 2 B: cozy, mid, top-down · 3 unity · 4 assets/art · 5 off
```
**Reading the reply:**
- Unanswered → the default. B without a setting → take it from words in the user's request if any,
  else ask once ("which setting? cozy, high-fantasy or your own words").
- A value you don't recognise (typo, unknown field) → ask once with the 2-3 closest options; never guess silently.
- "advanced" → one more short message (defaults in brackets, answer in one line):
  colours [no limit]: 8 (retro) · 16 · 32 · no limit · an exact palette (hex list or a palette image) ·
  outline [dark]: dark · selective (coloured, lighter on lit edges) · none ·
  shading [soft]: flat (1-2 tones) · soft (3) · detailed (4+) · light [top-left]: top-left · top · top-right · front ·
  dithering [no]: no · yes - e.g. "16, selective, soft, top, no".
- `game` = the project folder's name (don't ask).
- Engine: every engine gets PNG sprite sheets + Aseprite-format JSON; Godot also gets a SpriteFrames
  `.tres`. Unity / GameMaker / Phaser import notes are in the README ("Using the files in your engine").

If `$ARGUMENTS` already names an image/folder, treat it as answer 2A and say so. A project with an
obvious art folder: mention it ("I can use art/heroes as the reference - say A to use it").

**Step 2 - build the setup.**
- Reference (A/C): `python R/scripts/analyze_style.py <path> --out <out>/style_analysis`, look once at
  its `look.png`, map the numbers with `R/references/parameters.md` (the `/pga-analyze` steps 1-3),
  then apply any parameters they gave on top. Keep the reference path as `reference` and use it as
  the style anchor for its asset family.
- Parameters (B): fill the style fields from `R/references/parameters.md` (setting preset → look,
  palette, negatives; density → sizes; colours, outline, shading, view, light, dither as given).
- Write the proposed style to `<out>/style_draft.json` (style fields only).

**Step 3 - show it, in ONE message:**
```
Proposed style
| field | value | from |          (from = your answer · the reference · preset default)
...
Sample prompt (free, nothing generated): "<an improved prompt for one typical subject, e.g. a hero>"

Reply:  save <name>              keep it under that name (e.g. "save cozy-town")
        change <field> <value>   adjust and show again
        draft                    a 1-generation sample sprite first
```
`draft` → pixflux at the style's hero size with the sample prompt (cost 1), show it (QA first), then
offer the same three replies again. `change` → update the draft file and show the table again.

**Step 4 - save** (on "save <name>", or "yes"/"looks good" → ask only for the name, default = the setting):
1. Write the project fields to `pixellab.json` (create it if missing; keep fields already there):
   `game`, `tier` (trial/credits-only = 0), `engine` (answer 3), `out` (answer 4, created if missing),
   `seed` 7, `max_cost` null.
2. `python R/scripts/style.py save <name> --from <out>/style_draft.json --use`
   and `python R/scripts/share.py set <off|stats|prompts>` (answer 5; default off)
   and `python R/scripts/profile.py set beginner <true|false>` (answer 1; default true).
3. Report in 3 lines: the style name and that it is active; how to use others later -
   `--style <name>` on any command, `/pga-style list` / `use <name>` / `new` to add another;
   then the next step: beginners → "say `/pga-start` for a guided first project (~15-20 generations)";
   others → "try `/pga-char <idea> --dry` (free) to see a plan".

Anchors must be uploadable PNGs ≤ 256 px for sprite tools (backgrounds can be bigger for Pro); note any that are too big.
