---
name: pixellab-game-art
description: Use when making pixel-art game assets with the PixelLab MCP tools, or when picking the right PixelLab tool and parameters - backgrounds, backdrops, buildings, characters/monsters/bosses, icons, attack/skill animations and painted VFX. Any genre (setting presets), pixel density, palette, frame count and timing as parameters; can analyse the user's own art or GIF and turn its style into rules. Default preset is a proven dark-fantasy house style - style-anchored prompts, padded wind-up→hit key-pose animation, outlined vfx_workbench effects - plus review steps and budget rules.
---

# PixelLab game art

A PixelLab helper built from ~4,300 real calls. Its default is the house style of a side-view,
dark-fantasy pixel-art game (heroes on the left facing right, foes on the right facing left), but
genre, pixel density, colours, outline, shading, view, frame count and timing are all parameters -
per call (flags), per project (`pixellab.json`), or learned from the user's own art (`/pga-analyze`).
In a project with no `pixellab.json`, the first generating command sends the `/pga-init` setup message
(plan, art style or reference image, engine, output folder, sharing), waits for the answers, saves the
style, then does the original request - see prompt_improver.md §1.
**Working rules for every command:** print each PixelLab call with its full parameters and the cost
before submitting; never ask for permission or confirmation; never repeat a call (reuse logged jobs,
re-fetch instead of resubmitting); end with a results table - generations per call, total vs
estimate, balance before → after, files ([references/prompt_improver.md](references/prompt_improver.md) §5, §6, §8).
**[references/parameters.md](references/parameters.md)**: every parameter, the setting presets,
the density table and the precedence (user's words > flags > profile rules > preset > house).

Needs the PixelLab MCP server connected (tools `create_image_pro`, `create_image_pixflux`,
`create_image_pro_flash`, `edit_image_pro_flash`, `animate_image`, `vfx_workbench`, …).

## Tasks

Each command improves the user's prompt with this skill's references before it reaches PixelLab
(the shared loop: [references/prompt_improver.md](references/prompt_improver.md)). Flags on every
generating command: `--dry` (show prompt, tool, size, cost only) · `--draft` (1-generation pixflux
preview first) · `--ref <image>` · `--n 3` (variations) · `--size WxH` · style `--setting --density
--colors --palette --outline --shading --dither --light --view` · animation `--frames --timing --fps
--fx --hit --loop` (values and limits: [references/parameters.md](references/parameters.md)).

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
| `pga-update` | gets the weekly skill update and merges it into your install, keeping your own edits (free) | `pga-update` |
| `pga-tech` | explains why the skill does something, or walks through how it does a task step by step (free) | `pga-tech explain pga-anim` |
<!-- /pga:commands -->

Each task's steps are in `references/tasks/<task>.md` - read that one file when the user names the task (`pga-anim`, `/pga-anim`, "pga anim") or describes that job; flags (`--dry`, `--draft`, `--n 3`, …) work in plain text. The first task of a session checks the setup (PixelLab MCP connected, Python + packages) and stops with fix steps if something is missing - see prompt_improver.md §0. If a subagent named `pga-<task>` is installed (`install.py --agent`), hand the task to it - it runs on the model picked for that task in models.json (cheap for text-only tasks); otherwise do the task yourself. pga-init, pga-style and pga-analyze ask the user questions, so always run those yourself.

## Golden rules (every asset)

1. **Anchor the style.** Pass an approved asset of the same family as the style/colour reference on
   every production call (`style_image`, `style_image_url`, `color_image_url`). A prompt alone drifts.
2. **One fixed seed per family** (7 by default) so a batch matches.
3. **Say what you don't want**: `no characters`, `no text`, `no frame, no square`, `no guns`,
   `not a dragon`… Most retries in the log were fixed by one negative. A house negative never
   overrides what the user asked for: a requested rifle drops `no guns` (library/characters.md §e).
4. **Say how it sits in the canvas**: `whole body fits inside the canvas with a small margin`,
   `single object centred`, `feet in the same place`, `open flat ground along the bottom third`.
5. **Facing is data.** Heroes `facing right`; foes `three-quarter view facing left` (+ `direction: "west"`).
   Record each sprite's facing; mirror in the engine rather than regenerate.
6. **Sprites transparent** (`no_background: true`); backdrops and backgrounds opaque.
7. **Describe a creature, not a concept**: name the body plan, material, weapon, glow colour.
8. **Look before you install.** Contact sheet of every new frame next to what it replaces.

## Which tool for what

How PixelLab's MCP service works (async jobs, uploads, downloads, limits) and a full
"need → tool first → alternatives" table for every PixelLab tool, including ones the house style
rarely uses (rotating characters, tilesets, UI panels, fonts, cleanup):
**[references/pixellab_api.md](references/pixellab_api.md)** - read it before picking a tool; the
live docs are https://api.pixellab.ai/mcp/docs. The house picks:


| Asset | Tool | Typical size | Cost (gens) | Notes |
|---|---|---|---|---|
| Battle background | `create_image_pro` | 640×256 | 25 | style ref = an approved background; open ground bottom third |
| Cheap background variant | `create_image_pixflux` | 320×200 | 1 | `color_image_url` = the pro background |
| Screen backdrop / story picture | `create_image_pro` | 624×392 / 288×120 | 25 / 15 | Pro max for 16:10 is 632×424 |
| Building / prop | `create_image_pro` (small) | ≤170 px | 10–15 (was 20–25), 4–16 candidates | one building per call, flat side elevation |
| Hero / portrait sprite | `create_image_pro_flash` | 96×200 | 6 | style ref = an approved hero |
| Monster / boss | `create_image_pro_flash` | 200×200 | 6 | style ref = an approved foe, "facing left" in the text; pixflux (1) only for drafts |
| Icon | `create_image_pixflux` / Pro | 64 → box-downscale to 32/40 | 1 / 15 | one icon as style ref, never a grid |
| Key pose (attack/skill) | `edit_image_pro_flash` | padded canvas | 9 (>200 px side) | see animation |
| Swing animation | `animate_image` | padded canvas, `frame_count: 10` | 8 (192×256) / 6 (192×200) | first = wind-up, last = hit; weapon swings + a 6-frame swing for the crescent (5 / 4) |
| VFX | `vfx_workbench` | 112–360 px | **free** | see VFX |

Prompt templates, parameters, verbatim examples and pitfalls - **one file per asset type**; read
only the one you need plus `house_rules.md`: `references/library/` (`backgrounds`, `scenes`,
`buildings`, `characters`, `icons`, `ui_tiles`, `animation`, `pose_edits`, `vfx`); index in
[references/prompt_library.md](references/prompt_library.md). Usage numbers: [references/stats.md](references/stats.md).

## Characters

- Heroes: `create_image_pro_flash` 96×200 from a data row - *"full body portrait of a <man|woman>
  <subclass> hero standing, <class base look>, <gear tier>, <accent colour>. <flavour line>. Dark fantasy
  pixel art, muted shading, clear role colours"*, style ref an approved hero, seed 7.
- Monsters: **Pro Flash** 200×200 with an approved foe as `style_image` - *"dark gritty fantasy pixel
  art <monster|elite monster|boss monster>, full body, three-quarter view facing left: <body plan>,
  <material>, <weapon/pose>, <glow>, heavy dark shading"*. Tested 2026-10-13 on the same humanoid foe prompt with an existing foe as style ref: **Pro Flash** (6) was the most detailed, followed the brief fully, faced left as asked and matched the anchor's outline and shading; **Pro** (10) was close in quality but ignores facing (came out facing right - mirror it); **pixflux** (1) was flat and its forced palette changed the colours; **v3** `create_character` (6 for 8 directions) gave a thin side profile, humanoid-only - only for games that need 8 facings.
- Role colour coding keeps a roster readable: warrior steel + deep red, ranger forest green + brown,
  mage deep blue, cleric white + gold, rogue dark violet.
- Prevent problems in the first prompt (bows crossing legs, guns on "snipers", metal on rock golems);
  edits fix them slowly.

## Animation - the house style (attacks, skills, signature moves)

**Never animate on the tight standing-sprite canvas, and never start a swing from the plain
standing pose.** Both give a body that stands still and then snaps into the hit.

1. **Pad** the standing sprite onto a bigger canvas, feet on the bottom edge: room above and in
   front for overhead swings (heroes 192×256, bosses 256×256 - poses cost 9), room in front only for
   thrusts, throws, shots and bashes (192×200 - poses cost 6, the whole move 22 instead of 31). Record where the sprite's top-left
   sits - the engine grows the sprite's rect by that offset so pixel scale and feet stay put.
   `scripts/pad_sprite.py`.
2. **Two key poses** with `edit_image_pro_flash` on the padded upload,
   `use_color_palette_correction: true`, `no_background: true`:
   *"The same <short look>, <pose>. Same size, same colours and pixel style, feet in the same place, no background."*
   - **A = a real wind-up/coil**: name where the weapon/fist ends up and how far the torso turns
     ("blade raised high behind his shoulder", "fist cocked beside its right shoulder, torso rotated hard").
   - **B = the follow-through/hit** ("at the end of a heavy slash, sword swung down in front, deep lunge").
   - **Dynamic layer on both** (gives Pro-quality poses from Pro Flash): `dynamic exaggerated pose`,
     stance depth ("extremely deep lunge, front knee bent low, back leg straight"), torso lean/twist,
     and the character's tabard/cape/hair "flaring with the motion". Expect more swing flashes:
     QA + `scrub.py --keep-main`; never add "no effects" to the swing action (it made flashes worse).
   - Check hands and props didn't swap (shield moved to the wrong arm, lantern in the other hand) - re-roll that pose.
3. **`animate_image`** `first_frame_url = A`, `last_frame_url = B`, **`frame_count: 10`** (smooth; 6 only for short moves or when 10 goes off-script),
   `no_background: true`; the action describes **motion only** ("brings the raised sword down and
   forward in one heavy fast slash, stepping into a deep lunge").
4. **Review all 11 raw frames** (index 0 = A, 10 = B) with `qa.py --anim` + one half-size sheet and
   **keep every good frame**. Same-hue streaks → `recolor_trail.py --to none --ref <sprite>`;
   off-palette flashes → `scrub.py --keep-main`. Drop a frame only if it can't be cleaned. If the
   in-betweens invent a pose that is in neither key pose, re-roll once with the path pinned in the action and a new seed.
5. **Play it with light holds**: ~60 ms a frame, 160 ms wind-up, 140 ms hit (`make_sheet.py --beat light`).
   Long boss-style holds read as freezing / low fps on heroes (playtest feedback).
6. **Weapon swings get a crescent slash** in a pale air ramp behind the character - harvested from a
   6-frame swing of the same poses (`slash_layer.py`), while the generator's own thin streaks are
   removed (`recolor_trail.py --to none`). Thin streaks read as elemental magic; a crescent reads as a cut.
7. **Ground-snap** every frame (`ground_snap.py <sprite> <pad> <frames…> --check`, then without):
   generated poses float up to ~20 px above the standing sprite's feet line. Grounded moves only - not jumps or flyers.
8. **8 directions (top-down)**: front-facing reference → `create_character` v3 rotations → `animate_character` v3 per
   direction with the aim named in screen terms (never "forward" - it means screen-right) → mirror 3 → `dir8_finish.py`.
   Billed on the generated canvas (~7/direction for a 96×200 sprite). [references/animation.md](references/animation.md) → "8 directions".
9. **Same frame count for all of a character's moves** (11): the eye compares how far the body moves
   per frame, so a 7-frame skill next to an 11-frame attack looks choppy.

Details, timing tables, engine notes, idle/death/walk: **[references/animation.md](references/animation.md)**.

## VFX - the house style

Painted, outlined, lit effects built in the free `vfx_workbench`, in the attacker's own colour
ramp, much bigger than the body, with a fast launch, a long hold on the hit and a quick break-up.
Fixed recipe: `tones 5, detail 0.1, shading lit, outline dark, fps 12, loop false`, one 6-stop
`main` ramp (+ optional accent ramp). Three templates cover almost everything:

- **Strike** on one target - 112×112, 12 frames: `assets/vfx_templates/strike_single_target.json`
- **Wave** across a whole party - 340×130, 14 frames: `assets/vfx_templates/wave_across_party.json`
- **Eruption** under each target - 100×136, 12 frames: `assets/vfx_templates/eruption_per_target.json`

Re-skin a template for a new character by patching only `ramps.main`.
Timing spec, layer vocabulary and pitfalls: **[references/vfx.md](references/vfx.md)**.

## Review before installing

1. `scripts/qa.py` first - it flags empty images, wrong transparency, subjects touching the edge,
   palette drift from the anchor and (with `--anim`) flash pixels. Only flagged images need a close look.
2. One contact sheet, half size (`scripts/contact_sheet.py … --scale 0.5`) - new frames beside the
   art they replace. Never open frames one by one: images are the model's most expensive input.
3. A preview GIF with the real timing (`scripts/preview_gif.py`) - cheaper than running the game.
4. Engine export: `scripts/make_sheet.py` → spritesheet PNG + Aseprite-format JSON (durations, pad
   offset, facing, hit frame) + optional Godot SpriteFrames `.tres`.
5. Run the game's tests.

## Production helpers (`scripts/`, Python 3.8+, Pillow, numpy; scipy for scrub)

| Script | Does |
|---|---|
| `check_setup.py <command>` | lists missing Python packages with the fix |
| `upload.py <upload_url> <files…>` | local PNGs → `upload:<id>` refs (stdlib, no curl) |
| `fetch.py <job> <out> [--frames N]` / `--jobs jobs.txt --out dir` | waits for jobs, downloads, logs one JSON line each to `log.jsonl` (refunded failures marked) |
| `cost_report.py <log.jsonl>` | generations spent per command / tool / day |
| `pad_sprite.py` | sprite onto a padded canvas, prints the offset |
| `qa.py` | automatic checks before anyone looks |
| `scrub.py <dir> <frames…>` | removes off-palette flashes + specks from animation frames (`--clear-right X` for a shot's own muzzle flash) |
| `find_muzzle.py <dir>` | finds a shot's frame and muzzle from the generator's own flash |
| `dir8_finish.py <spec.json>` | 8-direction finish: clear flashes, bake your vfx flash rotated per direction, pad to one frame count, mirror the west side |
| `contact_sheet.py … --scale 0.5` | one review image |
| `preview_gif.py` | shareable GIF with the house rhythm (`--vfx` overlays a vfx_workbench export) |
| `make_sheet.py` | engine-ready spritesheet + JSON (+ Godot .tres) |
| `analyze_style.py <png/gif/folder>` | measures a reference's style (scale, palette, outline, tones, dithering, light, GIF timing) for `/pga-analyze` |
| `apply_palette.py <palette> <files>` | snaps generated art to a palette or N colours (enforces colour rules, free) |
| `ground_snap.py <sprite> <pad> <frames…>` | puts every frame's feet back on the standing sprite's ground line |
| `recolor_trail.py` / `slash_layer.py` | turn generator streaks into an effect colour / lift a crescent slash onto another swing |

## Budget rules

- Check `get_balance` first; say the estimate before a batch (e.g. *"10 key poses × 9 + 5 animations × 5 ≈ 115"*).
- `--draft` before any Pro image whose layout is uncertain: a 1-generation pixflux preview saves a 25.
- Don't pad past 200 px on the longest side unless the move needs the room (Pro Flash 6 → 9).
- Measured vs official prices for every tool: [references/costs.md](references/costs.md). Failed jobs
  are refunded.
- Large Pro images cost 25 (40 before Oct 2026): only for pictures seen full-screen and often.
- Pro Flash (create/edit/inpaint) by longest side: ≤96 → 5, ≤200 → 6, >200 → 9.
  `animate_image` = ceil(W × H × frames ÷ 65,536), capped at W × H × frames ≤ 524,288:
  192×256×10 = 8, 192×200×10 = 6, 192×256×6 = 5 (256² takes at most 8 frames).
- A hero melee move ≈ 2 poses + 10-frame swing + 6-frame crescent swing = **31** (26 without the
  crescent, 22 on 192×200), plus ~a third for re-rolls.
- VFX in the workbench cost nothing - spend time there, not generations.
- Concurrent jobs depend on the subscription tier, and six
  tools need Tier 1+ - table and fallbacks: [references/pixellab_api.md](references/pixellab_api.md) → Subscription tiers.
  Submit independent jobs in the same turn, up to that limit. A job returning HTTP 410 /
  "stalled" never finishes and is refunded: resubmit. Pro Flash takes 7-15 min, animations 1-3 min.
  `scripts/fetch.py` waits up to 100 s per run, downloads and logs; `TIMEOUT` = run the same command
  again (re-runs never double-log). Meta goes in a file (`--meta-file`), not inline JSON.

## Licence

PixelLab's terms of service (https://pixellab.ai/termsofservice) apply to everything generated.
Notably, training AI models on PixelLab outputs isn't allowed without PixelLab's written
permission. Check the current terms before selling or redistributing assets.
