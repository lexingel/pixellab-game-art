# Parameters: setting, density, style rules, animation

Everything here is a **default the user can change** - per call with a flag, per project in
`pixellab.json`, or learned from their own art with `/pga-analyze`. The house look (dark fantasy,
high density, side view) is just the `dark-fantasy` + `high` preset.

## Precedence (highest first)

1. The user's own words in this prompt ("a rifle", "pastel", "8 frames").
2. Flags on this command (`--setting scifi --frames 9`).
3. The named style in use - `--style <name>` on this command, else `pixellab.json` → `active_style` -
   its `rules` and style fields (see Named styles below).
4. `pixellab.json` top-level `rules` and style fields (older profiles keep their style here).
5. The setting preset below.
6. House defaults (the rest of this skill).

A lower level never contradicts a higher one: a preset's negative that clashes with the user's
request is dropped, not kept (a sci-fi knight with a sword keeps the sword).

## Style flags (every generating command) → profile field

| Flag | `pixellab.json` | Values | Default |
|---|---|---|---|
| `--style NAME` | `active_style` | a saved style's name (`/pga-style list`) - use it for this call | the active style |
| `--verbose` | `output` (`compact` / `verbose`) | full JSON for every PixelLab call instead of one line each | `compact` |
| `--max-cost N` | `max_cost` | stop before submitting if the run's estimate exceeds N (no question asked) | none (no cap) |
| `--setting S` | `setting` | a preset name below, or free words ("solarpunk") | `dark-fantasy` |
| `--density D` | `density` | `low` · `mid` · `high` | `high` |
| `--colors N` | `colors` | max colours per sprite (8-64) | none |
| `--palette P` | `palette_hex` | hex list, a palette.png, or an analysis.json | none |
| `--outline O` | `outline` | `dark` · `selective` · `none` | `dark` |
| `--shading S` | `shading` | `flat` (2 tones) · `soft` (3) · `detailed` (4-6) | `detailed` |
| `--dither` / `--no-dither` | `dither` | true / false | false |
| `--light L` | `light` | `top` · `top-left` · `top-right` · `front` | `top` |
| `--view V` | `view` | `side` · `3/4` · `top-down` · `iso` | `side` |
| `--face F` | `facing` | heroes `right`, foes `left` (side view) | as profile |

## Named styles (several art styles per project)

`pixellab.json` keeps **project** fields at the top (`game`, `tier`, `out`, `engine`, `max_cost`)
and any number of **art styles** under `styles`, each saved under the user's own name:

```json
{
  "game": "Moonwell", "tier": 1, "out": "pixellab_out", "engine": "godot",
  "active_style": "cozy-town",
  "styles": {
    "cozy-town":  {"setting": "cozy", "density": "mid", "view": "top-down", "colors": 16,
                   "outline": "selective", "shading": "soft", "light": "top-left",
                   "rules": ["chunky proportions, head ~1/3 of the height"], "anchors": {"heroes": "art/hero.png"}},
    "dungeon":    {"setting": "dark-fantasy", "density": "high", "view": "side", "reference": "art/ref_knight.png"}
  }
}
```
- Project field `share`: `{"level": "off"|"stats"|"prompts", "install_id": "<random>"}` - the
  user's sharing choice (setup question 5, `/pga-feedback`); written only by `scripts/share.py`.
- Style fields: `setting density look palette palette_hex colors outline shading dither light view
  facing sizes negatives rules anim anchors seed reference analysed_from notes`.
- A command uses `--style <name>` if given, else `active_style`; its fields overlay the top-level ones.
- Manage them with `python <skill>/scripts/style.py list|show|save|use|rename|delete` (exact JSON
  edits; never hand-edit the file in the chat) or the `/pga-style` command. `/pga-init` and
  `/pga-style new` build a style with the user and save it under the name they give.

## Settings (genre presets)

Each gives the look words, palette words, the era of weapons and tech, and genre-aware negatives.
Free words also work (`--setting "frozen viking saga"`): write the same four fields for it yourself.

| Setting | Look words | Palette words | Weapons / tech era | Negatives (only if not asked for) |
|---|---|---|---|---|
| `dark-fantasy` (house) | dark fantasy pixel art, muted colours, gritty | deep violet, ember orange, cold blue, worn steel | swords, bows, crossbows; black-powder guns only if named | no modern objects, no guns |
| `high-fantasy` | bright high fantasy pixel art, heroic, clean | royal blue, gold, emerald, warm white | swords, staves, longbows | no modern objects, no guns |
| `cozy` | cute cozy pixel art, chibi proportions, big head, rounded shapes | soft pastels, warm cream, sage green | tools, wands, slingshots | no blood, no gore, no realistic weapons |
| `scifi` | sci-fi pixel art, clean hard-surface shapes, glowing accents | gunmetal, teal, cyan glow, warning orange | blaster rifles, plasma pistols, energy blades | no medieval weapons, no wooden bows |
| `cyberpunk` | cyberpunk pixel art, neon rim light, rainy night, high contrast | magenta, cyan, deep navy, acid yellow | smart pistols, SMGs, cyber katanas, implants | no medieval armour |
| `steampunk` | steampunk pixel art, brass and copper, rivets, steam | brass, copper, sepia, soot black | flintlocks, clockwork rifles, brass gauntlets | no plastic, no neon |
| `post-apoc` | post-apocalyptic pixel art, dusty, rusted, scrap-built | rust, khaki, bleached sand, olive | makeshift rifles, pipe weapons, scrap armour | no clean new gear |
| `modern` | modern-day pixel art, realistic proportions, everyday clothes | natural, urban greys, one accent | modern firearms, tools | no fantasy armour, no magic glow |
| `horror` | horror pixel art, deep shadows, unsettling | sickly green, bone white, dried-blood red, black | improvised weapons, lanterns | no bright cheerful colours |
| `western` | western frontier pixel art, sunbaked, dusty | sand, burnt orange, leather brown, sky blue | revolvers, lever-action rifles, lassos | no modern guns, no armour plates |

## Density (pixel resolution)

How many pixels a character gets. It sets the canvas sizes, the detail words and the cost.

| Density | Character height | Hero / monster / boss canvas | Icon (gen → final) | Detail words | Pro Flash cost |
|---|---|---|---|---|---|
| `low` | ~24-40 px | 32×48 · 48×48 · 96×96 | 32 → 16 | simple chunky low-resolution pixel art, few colours, minimal detail, bold readable silhouette | 5 |
| `mid` | ~56-90 px | 64×96 · 96×96 · 128×128 | 64 → 32 | clean pixel art, moderate detail | 5-6 |
| `high` (house) | ~150-190 px | 96×200 · 200×200 · 200×200 | 64 → 40 | detailed shading, high detail, crisp | 6 |

Pro Flash takes any size 16-256 in multiples of 4. Backgrounds scale with the character:
battle background ≈ 3.3× the hero's height wide (low 160×64, mid 320×128, high 640×256).
Animation padding scales the same way: canvas ≈ 2× the sprite's width, +28% height for overhead moves.
At `low`, `animate_image` costs 1 and allows 16 frames.

## Style fields → prompt words, tool parameters, post-processing

| Field | Prompt words | Tool parameter | After generation (free, local) |
|---|---|---|---|
| `colors N` | "limited palette of about N colours" | Pro: `max_colors` | `apply_palette.py auto <files> --colors N` |
| `palette_hex` | the palette words, not the hexes | Pro: `palette`; Pro Flash: an anchor with those colours + `style_options.color_palette` | `apply_palette.py <palette> <files>` |
| `outline dark` | "1 px dark outline" | pixflux `outline` (weak) | - |
| `outline selective` | "selective outline, each colour edged in its own darker shade, no black outline" | - | - |
| `outline none` | "no outline, soft edges" | - | - |
| `shading flat/soft/detailed` | "flat colours, 2 tones" / "soft shading, 3 tones" / "detailed shading" | pixflux `shading` (weak) | - |
| `dither` | "dithered shading" / "no dithering, clean colour blocks" | - | - |
| `light` | "light from the <dir>" | - | - |
| `view` | "side view" / "three-quarter view" / "top-down view" / "isometric view" | pixflux/objects `view`; for 4/8 facings use `create_character` | - |
| `rules` | each rule applied where it fits (a rule about colours → palette step; about timing → animation) | - | - |

An anchor image still beats all of these words: if the profile has one, keep passing it.
Upscaled reference art must be shrunk to 1 px = 1 pixel first (`analyze_style.py` writes `native/`;
PixelLab's `unzoom_image` does the same for 0.1 gen).

## Animation flags (`/pga-anim`) → profile `anim`

| Flag | `anim` field | Values | Default |
|---|---|---|---|
| `--frames N` | `frames` | total frames incl. both key poses, 5-17 | 11 |
| `--timing T` | `timing` | `light` (hero holds) · `heavy` (boss holds) · `even` · `custom` | `light` |
| `--fps F` | `fps` | with `even` | 12 |
| `--durations a,b,…` | `durations_ms` | one per frame (`custom`, e.g. measured by /pga-analyze) | - |
| `--fx X` | `fx` | `crescent` (weapon cut) · `streak` (recoloured generator streaks) · `none` · `keep` (as generated) | `crescent` for blades, `none` for shots |
| `--hit N` | `hit` | the damage frame | frame before last; shots 1 |
| `--loop` | `loop` | idle / walk / hover cycles: last frame = first | off |
| `--canvas WxH` | - | padded canvas | from the move and density |
| `--dirs N` | `dirs` | `1` (side view) · `8` (top-down: rotate, animate 5, mirror 3 - animation.md "8 directions") | 1 |

**Checking `--frames`** against `animate_image`: it generates `frame_count` = N - 1 in-betweens + the
first frame, `frame_count` must be **even, 4-16**, and **W × H × frame_count ≤ 524,288**.
- N even → generate N (one more) and drop the weakest in-between; say so.
- Too many for the canvas → say the maximum (192×256: 10 → 11 frames; 256²: 8 → 9 frames) and offer a
  smaller canvas, a lower density, or a **splice** (animation.md: 9 frames + 3 in-betweens in the fastest
  span = 11, +4 gens at 256²).
- Cost = ceil(W × H × frame_count ÷ 65,536).
- Keep every move of one character at the same N (the eye compares motion per frame).
