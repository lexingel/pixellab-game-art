# PixelLab MCP - how it works and which tool to reach for

Live source of truth: **https://api.pixellab.ai/mcp/docs** (an AI-assistant guide generated from
the tool definitions; fetch it when a tool, parameter or limit here looks out of date). For
anything not covered, the `search_help` tool asks PixelLab's own docs agent. This file is a
condensed reading of that guide (as of 2026-10-12) plus what the house style learned in use;
where the two differ, **house settings win** (they were measured on real jobs).

## How the service behaves

- **MCP tools, not REST.** Call the tools (names may be prefixed, e.g. `mcp__pixellab__create_image_pro`).
  If no PixelLab tools are visible, the MCP server isn't configured - say so (setup in
  prompt_improver.md §0); don't fall back to curl against the API. (A separate REST "API v2" exists -
  https://api.pixellab.ai/v2/llms.txt - for code that generates assets at runtime; not for this skill.)
- **Everything is asynchronous.** A create/edit/animate call returns a job id at once; the work runs
  in the background (seconds for pixflux, 1-15 min for Pro / Pro Flash / animations).
  - Check with the matching `get_*` tool (`get_image` for raw images and `animate_image`,
    `get_character`, `get_object`, `get_tiles_pro`, …).
  - Prefer **`wait_for_jobs`** (blocks up to `timeout_seconds`, default 240) over sleep-and-poll;
    `list_jobs` shows what's running; `cancel_job` stops one.
  - Queue independent jobs together (e.g. both key poses, or several icons) - up to the tier's
    background limit at once (see Subscription tiers below).
  - A job that answers 410 / "failed" / "stalled" never finishes: resubmit it.
- **Downloads need no auth** - the UUID in the URL is the key
  (`/mcp/images/<job>/download`, `?index=N` for one frame of an animation). Don't paste these URLs
  publicly if the art is private.
- **Inputs: URLs, not base64.** Every tool that takes an image prefers a URL; MCP clients truncate
  long base64 strings and corrupt the image. For local files: `get_upload_url` → `scripts/upload.py <url> x.png` → pass the returned `upload:<id>` anywhere an image URL is accepted
  (uploads are kept 3 days). A finished job's download URL can also be passed straight on.
- **Sizes**: `get_pro_flash_capabilities(operation, width, height)` is a free quote for Pro Flash
  (native sizes, custom sizes up to 256×256 in steps of 4, and the cost). Other tools state their
  limits below.
- **Balance**: `get_balance` (free) - remaining subscription generations and credits.


## Subscription tiers (what each account can use)

From PixelLab's docs agent (`search_help`, 2026-10-14) and the MCP tool docs; re-check with
`search_help` if a tool refuses. Generations come from the subscription first, then USD credits.
**A credits-only account is Tier 0: credits pay for calls but never unlock a tier-gated tool.**

| Tier | Generations / month | Background jobs at once | Synchronous at once |
|---|---|---|---|
| Free trial / Tier 0 (incl. credits-only) | trial balance | **1** | 1 |
| Tier 1 | 2,000 | 8 | 5 |
| Tier 2 | 5,000 | 10 | 8 |
| Tier 3 (Pixel Architect) | 10,000 | 20 | 10 |

Tier-gated tools and the fallback to use below that tier (everything else - Pro, Pro Flash,
`create_character` v3/pro, `animate_character` v3, `edit_image`, maps, `vfx_workbench`,
`pixelart_workbench` - has no tier gate; "Pro" means a higher cost, not a paid plan):

| Tool | Needs | Fallback below it |
|---|---|---|
| `animate_image_pixminimax`, `animate_character` mode `pixminimax` | Tier 1+ | `animate_image` (up to 11 frames; splice two takes for longer, animation.md) |
| `inpaint_image` (longest side ≤256) | Tier 1+ | `inpaint_image_pro_flash` |
| `inpaint_image` (longest side >256) | Tier 2+ | `inpaint_image_pro_flash` on a ≤256 crop, pasted back |
| `transfer_outfit` | Tier 1+ | `edit_image` with all frames in `image_urls` (one call), or `edit_image_pro_flash` per key pose + re-animate |
| `create_tiles_pro` | Tier 1+ | `create_topdown_tileset` / `create_sidescroller_tileset` / `create_isometric_tile` |
| `create_path_tiles` | Tier 1+ | `create_topdown_tileset` with a road terrain |
| `create_building_kit` | Tier 1+ | `create_map_object` / `create_image_pro` per piece, one style anchor |

How the skill uses this: the setup check reads the tier from `get_balance` (its `subscription:`
line) and keeps it for the session - it caps how many jobs it submits at once to the tier's
background limit (the rest go in as earlier ones finish), and below Tier 1/2 it plans the fallback
tool from the start (the plan line says `fallback: <tool> (Tier N needed for <tool>)`). If a call is
refused for the tier anyway, switch to the fallback without asking.

## Which tool first (decision table)

| You need | Use first (house) | Use instead when… |
|---|---|---|
| A side-view hero/portrait sprite matching an existing roster | `create_image_pro_flash` + `style_image` (an approved sprite) | you need 4/8 rotations for a top-down game → `create_character` (mode `v3`, or `pro`) / `create_character_pro_flash` |
| A monster / foe sprite | `create_image_pro_flash` (6 at ≤200 px) + `style_image` of an approved foe; facing in the text (tested best, 2026-10-13) | several candidates → `create_image_pro` ≤170 px (4 for 10; no facing control, mirror) · 1-gen draft or forced-palette recolour → `create_image_pixflux` |
| Turn an existing sprite into 8 directions | `create_character(mode="v3", reference_image_url=…)` (the sprite must face the viewer = south) | it's a prop, not a character → `create_8_direction_object` |
| Battle background, backdrop, story picture | `create_image_pro` (`no_background: false`, style ref) | cheap variants → `create_image_pixflux` with `color_image_url` |
| Building / prop | `create_image_pro` small (candidates) | many small props at once → `create_1_direction_object` (size ≤85 gives 16 candidates) ; prop for a top-down map → `create_map_object` |
| Icons | `create_image_pixflux` at 64 → downscale | must match a polished set → `create_image_pro` ~40 px with one icon as style ref |
| A pose / outfit / detail change on an existing image | `edit_image_pro_flash` (+ `use_color_palette_correction`) | same edit on many frames at once → `edit_image` (`image_urls` list) ; quick cheap tweak ≤256² → `edit_image_pixen` |
| Fix one region (a hand, a stray object) | `inpaint_image_pro_flash` (mask box or mask image, `context_image`) | `inpaint_image` (10-25 gens, up to 512²; Tier 1+, >256 px Tier 2+) |
| Attack / skill animation | **two `edit_image_pro_flash` key poses → `animate_image` first→last, 10 frames** (animation.md) | long clips (up to 40 frames) → `animate_image_pixminimax` (Tier 1+) ; exact poses → `animate_with_skeleton_v3` |
| Walk / idle loop | `animate_image` (`last_frame` = first frame for a loop) | a `create_character` character → `animate_character` with a template (`walking-8-frames`, `breathing-idle`, …) |
| Spell / hit / aura VFX | **`vfx_workbench`** (free for subscribers; vfx.md) | - |
| Inspect / hand-edit / lint pixel art | `pixelart_workbench` (free; start with `describe cli`) | - |
| Clean up AI output | `correct_pixelart` (strength 0.1), `reduce_colors` (onto a game palette), `unzoom_image` (upscaled → true grid) - 0.1 gen each | - |
| Photo / painting → pixel art | `image_to_pixelart` (1 gen; `faithful` + strength 100-300 to keep the source) | higher quality → `image_to_pixelart_pro_flash` (6) |
| Recolour an animation into a new outfit | `transfer_outfit` (reference = the SAME character re-dressed; Tier 1+) | below Tier 1: `edit_image` with all frames in `image_urls` |
| UI panel / frame | `create_ui_asset` (style_image = a screenshot of the game) | - |
| Tilesets | top-down terrain: `create_topdown_tileset` (Wang, chain with base tile ids) · platformer: `create_sidescroller_tileset` · iso/hex/square sets: `create_tiles_pro` (Tier 1+) · roads: `create_path_tiles` (Tier 1+) · walls+floors: `create_building_kit` (Tier 1+) · single iso block: `create_isometric_tile` | - |
| Bitmap font | `create_font` (80-glyph atlas, no space glyph) | - |
| Talking portrait | `create_vocal_animation` → `create_talking_gif` / `get_lip_sync` | - |

## Key parameters and limits (the tools this skill uses)

**`create_image_pro`** - best quality, several candidates. Cost: docs say 10-25; **measured 10-25 since
2026-10-11** (25 for 624×392 and wide scenes, 15 for 288×120, 10-15 small); it was 20-40 before. Max 512×512 square, 688×384 for 16:9
(house: Pro max for 16:10 ≈ 632×424). `no_background` defaults **true** - set false for scenes.
`style_image_url` + `style_copy` (any of color_palette, outline, detail, shading);
`reference_images` up to 4, each with a `usage` note ("scene layout, colors and lighting only");
`palette` (hex list) / `palette_name` / `max_colors` to force a palette. Takes 1-10 min.

**`create_image_pixflux`** - 1 gen, 10-40 s. Default 128×128; total area ≥ 1024 px.
`no_background` (true for sprites), `view`, `direction`, `outline`, `shading`, `detail` (all *weak*
hints - the prompt text matters more), `text_guidance_scale` (default 8). `color_image_url` forces a
palette from any image. `init_image_url` + `init_image_strength` = how much is **kept** (500 barely
changes, 150 default real edit, ~50 keeps only composition - the opposite of usual img2img).

**`create_image_pixen`** - 1 gen alternative model; sides multiples of 4.

**`create_image_pro_flash` / `edit_image_pro_flash` / `inpaint_image_pro_flash`** - Pro Flash.
Measured cost by longest side: **≤96 px → 5, ≤200 → 6, >200 (to 256) → 9** (`costs.md`). Edit keeps the native canvas (no growth - pad first).
Edit `method`: `text` (description) or `reference` (a reference image + usage). `seed` default 0 -
change it to get a different take. `use_color_palette_correction: true` keeps colours on edits.

**`animate_image`** - any image + motion text. `frame_count` even, 4-16; width × height × frames
≤ 524,288 (256² → 8 frames max, 192×256 → 10). `last_frame_url` pins the end (interpolation).
Returns frame_count + 1 images: index 0 = your first frame. `action` = motion only. Cost scales with
pixels × frames (64²×8 = 1; 256²×6 ≈ 6; 192×256×6 ≈ 5). 1-3 min.

**`animate_image_pixminimax`** - multiples of 4 up to 40 frames, ≤ 256², `enhance_prompt`,
`direction`, `view`, `subject_description`, `initial_pose`; tier 1 subscription+. Use for long clips.

**`animate_character`** (for `create_character` characters) - template animations at 1 gen/direction
(`walking-8-frames`, `breathing-idle`, `fireball`, `cross-punch`, `taking-punch`,
`falling-back-death`, …) or custom v3 from `action_description` + `frame_count`; custom needs ONE
direction - ask the user which; `custom_start_frame_url` / `end_frame_url` = the same key-pose
trick as animate_image.
Billed per direction on the **generated** canvas (a 96×200 sprite animated on ~224² → 7 at 8 frames).
The model reads "forward" as screen-right in every direction: name the aim in screen terms, one
direction per call (animation.md → "8 directions").

**`create_character`** - `mode`: `standard` (1 gen, template skeleton, ≤128), `pro` (10-25, always 8
dirs), `v3` (2-9, best, up to 256, the only mode that rotates a reference sprite).
`reference_image_url` must face the viewer (south) or every direction label is off by the turn.
`view`: low top-down / high top-down / side. `proportions` presets (chibi, heroic, …).

**`create_1_direction_object`** - one call returns many candidates by size (≤42 → 64, ≤85 → 16,
≤170 → 4, else 1); `view` top-down or sidescroller; `style_images` (up to 8 at small sizes);
`item_descriptions` per slot. Result enters **review**: `get_object`, then `select_object_frames` or
`dismiss_review`. 10-25 gens.

**`animate_object`** - `mode` v3 (default, cheaper, better) or pro (10-25 per direction - call once
without `confirm_cost`, show the cost, set it only after the user agrees).

**`inpaint_image`** - 32-512 px, mask rect or mask image (white = regenerate), 10-25 gens.

**`edit_image`** - pro edit of one or many frames at once (`image_urls`), text or
`reference_image_url` (copy appearance, keep pose); 10-25 gens billed by the whole grid.

**`vfx_workbench` / `pixelart_workbench`** - free command lines (`argv` list). Call without `argv` for
the guide; `describe cli` / `describe start` lists commands. `mode: "low"` acts directly, `"high"`
reasons with a review checklist (put the plan in `notes`). VFX `export --name` saves to the user's
"My effects" and returns GIF + spritesheet PNG + JSON; `--game-pack` adds a ZIP of every piece.

**`get_image(job_id, index)`** - status / result of any raw-image job; `index` returns one frame inline.

**`create_ui_asset`** - 192-688 px, aspect-gated maxima (512² square, 688×384 16:9, 600×448 4:3);
`style_image_base64` = a game screenshot is the strongest way to match an existing UI; 10-25 gens.

## Gotchas worth remembering

- Weak hints (`outline`, `shading`, `detail`, `view`, `direction` on pixflux/pixen/objects) are
  suggestions; put the important things in the description.
- Characters for 8 directions: the reference must face the camera; a 3/4 reference shifts all labels.
- `create_image_pro` defaults to a transparent background - backgrounds/backdrops need
  `no_background: false`.
- pixflux `init_image_strength` is "how much to keep"; `image_to_pixelart` strength above ~300 just
  hands back the source.
- `correct_pixelart`: start at strength 0.1; high values redraw details.
- Pro object animations and some pro calls ask for `confirm_cost` - never set it on the first call.
- Downloads are public-by-UUID; uploads expire after 3 days.
- When a tool or limit here disagrees with the live tool description in the session, the live tool
  description wins - it is generated from the server.
