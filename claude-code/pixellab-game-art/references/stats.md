# PixelLab usage stats (one game project)

## Calls per tool (generative only; polling tools excluded)

| Tool | Calls | Unique prompts |
|---|---:|---:|
| animate_image | 2,100 | 957 actions |
| vfx_workbench | 498 | 118 exports |
| create_image_pro | 492 | 365 |
| create_image_pixflux | 465 | 367 |
| edit_image_pro_flash | 298 | 234 |
| create_image_pro_flash | 234 | 214 |
| animate_object | 78 | 47 |
| inpaint_image_pro_flash | 53 | 39 |
| create_1_direction_object | 35 | 32 |
| inpaint_image | 16 | 7 |
| create_map_object | 12 | 12 |
| create_ui_asset | 5 | 5 |
| create_tiles_pro | 3 | 3 |
| **Total** | **~4,290** | |

Polling and housekeeping calls that were skipped: wait_for_jobs 821, get_image 242, list_jobs 98,
get_balance 80, get_upload_url 59, get_object 36, list_objects 21, get_pro_flash_capabilities 20,
and others.

## Calls per category

Image creation (pro + pixflux + pro_flash = 1,191 calls), classified by keyword heuristics:

| Category | Calls | Unique |
|---|---:|---:|
| Items & icons (skill, relic, status, UI glyph, heraldry, map markers) | 429 | 400 |
| Characters (heroes, monsters, bosses, champions) | 359 | 279 |
| Screen/hub backdrops & story pictures | 207 | 136 |
| Buildings & hamlet props | 91 | 50 |
| Battle backgrounds | 46 | 29 |
| VFX stills (pixflux, legacy) | 30 | 28 |
| Tiles / floors / roads | 29 | 24 |

Animation (`animate_image`, 2,100 calls) by action:

| Kind | Calls |
|---|---:|
| Attack / skill / other | 894 |
| Walk | 483 |
| Hurt | 328 |
| Idle | 215 |
| Death | 180 |

- `frame_count`: 4 (1,500) · 8 (558) · 6 (42, the current keyframe style and VFX one-shots)
- `last_frame_url` set: 592 calls. In 369 of them it equals the first frame (loops).

Edits (`edit_image_pro_flash`, 298 calls): about 60 two-character "defeated" poses, about 60 A/B
attack key poses (bosses and heroes), 44 rare/epic item tiers, about 50 archery poses and fixes, and
the rest are repairs, style transfers and building upgrades. `use_color_palette_correction: true` in
207 calls. `method: "reference"` in 19, `"text"` in 8.

VFX (`vfx_workbench`, 498 calls): render 258, export 118 (90 with `--game-pack`), add_part 45,
start 27, describe 25, set_part 14. Layer types: particles 170, ring 108, shape 63, rays 57,
puffs 36, glow 33, arc 28, beam 24, flame 18. Particle shapes: sparkle 49, dot 42, custom 34,
streak 30, chunk 11, droplet 4. fps: 12 on almost every effect.

## Size distribution

**create_image_pro** (492): 32x32 (94) · 40x40 (74) · 288x120 (73) · 624x392 (60) · 640x256 (32) ·
16x16 (30) · 640x400 (18) · 48x48 (11) · 640x288 (10) · 688x384 (10) · 96x96 (8) · 160x64 (8) ·
320x200 (6) · 688x256 (5) · plus a long tail of building sizes (96x80 – 192x144) and 96x200 heroes.

**create_image_pixflux** (465): 64x64 (201) · 200x200 (121) · no size given (42, with
init_image) · 128x128 (15) · 320x200 (14) · 256x256 (9) · 320x180 (9) · 128x80 (9) · 32x32 (7) ·
128x64 (6) · 48x64 (5) · 400x184 (4).

**create_image_pro_flash** (234): 96x200 (151) · 80x200 (20) · 84x200 (18) · 96x96 (15) ·
76x200 (10) · 88x200 (7) · 64x64 (4).

Rule of thumb from the log:
- icons: 16 / 32 / 40 / 64
- hero portraits: 96x200
- monsters: 200x200
- buildings: 64–192 wide
- story banners: 288x120
- hub rooms: 624x392 or 640x400
- battle backgrounds: 640x256 or 320x200
- animation canvases (current): 256x256 for bosses, 192x256 for heroes

## Seeds and anchors
- create_image_pixflux seeds: 7 (241 calls), none (140), 3 (36), 11 (18), 21 (8)
- create_image_pro seeds: none (358), 7 (94), 11 (30)
- create_image_pro_flash seeds: 7 (127), none (107)
- create_image_pro uses `style_image_url` in 481/492 calls and `style_copy` in 241 (236 of them
  `["outline","detail","shading"]`). `reference_images` in 132.
- create_image_pro_flash uses `style_image` in 181/234 calls.
- pixflux `color_image` palette anchor: 113 calls. `direction:"west"` (monsters facing left): 59.

## Most common style keywords
Counted across 3,677 prompt and action strings:

| Keyword | Count |
|---|---:|
| body motion only | 1,339 |
| no effects | 1,219 |
| pixel art | 745 |
| no new objects | 676 |
| same colours | 650 |
| no glow | 622 |
| dark fantasy | 525 |
| colours unchanged | 464 |
| dark outline | 441 |
| exaggerated motion | 434 |
| side view | 374 |
| full body | 302 |
| gold | 298 |
| centred | 296 |
| night | 276 |
| violet | 258 |
| bold dark outline | 237 |
| muted | 226 |
| game icon | 187 |
| rich shading | 181 |
| facing left | 174 |
| single object | 167 |
| three-quarter | 163 |
| transparent background | 130 |
| keep every colour | 106 |
| painterly | 101 |
| readable at small size | 99 |
| ember | 94 |
| same size | 90 |
| no people | 81 |
| no characters | 74 |
| thick dark outline | 76 |
| detailed shading | 72 |
| cinematic | 51 |
| dark gritty / heavy dark shading | 51 / 45 |
| feet in the same place | 40 |
| no text | 39 |
