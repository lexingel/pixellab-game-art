# PixelLab costs: measured vs official

Measured from ~3,550 jobs (Sept-Oct 2026, Tier 3 subscription) using the cost each job reported,
cross-checked against `get_balance` before and after batches - **the reported cost is what is
charged, and failed jobs (HTTP 410 / "failed" / "stalled") are refunded.** Official = the live tool
guide at https://api.pixellab.ai/mcp/docs (2026-10-12). Prices change: re-measure with a few jobs
and `get_balance` before a big batch.

| Tool | Official | Measured | Rule of thumb |
|---|---|---|---|
| `create_image_pixflux` | 1 | **1** at every size we used (32² … 400×184, 451 jobs) | 1 per image |
| `create_image_pixen` | 1 | - (not used) | 1 |
| `create_image_pro` | 10-25 | **since 2026-10-11: 10-25** · before: 20-40 | see the Pro table below |
| `create_image_pro_flash` | quote via `get_pro_flash_capabilities` | **5 / 6 / 9** by longest side (214 jobs) | ≤96 px → 5 · ≤200 → 6 · >200 (to 256) → 9 |
| `edit_image_pro_flash` | quote via `get_pro_flash_capabilities` | **5 / 6 / 9**, same tiers (296 jobs) | 96×200 → 6 · 192×256 → 9 · 256² → 9 |
| `inpaint_image_pro_flash` | quote via `get_pro_flash_capabilities` | **5 / 6 / 9**, same tiers (53 jobs) | billed by the full canvas, not the mask |
| `animate_image` | "scales with total pixels" (64²×8 = 1, 128²×16 = 4) | **ceil(W × H × frames ÷ 65,536)** - exact on all 2,040 jobs | 96×200×4 = 2 · 200²×4 = 3 · 192×256×6 = 5 · 256²×6 = 6 · 64²×8 = 1 |
| `animate_character` (v3 custom) | ceil(canvas² × frames ÷ 65,536) per direction, on the grown canvas | **7 per direction** for a 96×200 sprite at 8 frames (canvas grew to 224², 9 jobs) | budget by the generated canvas, not the sprite: ~224² for a 96×200 character |
| `animate_image_pixminimax` | by length; 40 frames ≈ 6 | - | Tier 1+ |
| `create_1_direction_object` | 10-25 | **20-25** (34 jobs) | 25 at small sizes (many candidates) |
| `create_ui_asset` | 10-25 | **10-20** (5 jobs) | |
| `inpaint_image`, `edit_image`, `transfer_outfit` | 10-25 (by size / whole grid) | - | `inpaint_image` Tier 1+ (>256 px Tier 2+), `transfer_outfit` Tier 1+ |
| `create_character` | standard 1 · v3 2-9 · pro 10-25 | **v3 with a 96×200 reference: 3** (8 directions, 1 job) | rotating your own sprite is cheap |
| `image_to_pixelart` / `_pro_flash` | 1 / 6 | - | |
| `correct_pixelart`, `reduce_colors`, `unzoom_image` | 0.1 | - | |
| `vfx_workbench`, `pixelart_workbench` | free (subscribers) | **free** (498 + calls) | build effects here, not with generations |
| `get_balance`, `get_upload_url`, `get_*`, `list_*`, `wait_for_jobs` | free | free | |
| Failed job | - | **refunded** (balance confirms) | resubmit without worrying about cost |

## `create_image_pro` in detail

| Canvas | Until 2026-10-07 | From 2026-10-11 |
|---|---|---|
| ≤ 48 px (icons) | - | 10 (32²: 10 · 40²: 15 · 48²: 10) |
| ~64-112 px (props, small sprites) | 20-25 | 10-15 |
| 96×200 (a hero sprite) | - | 10 |
| 288×120 (story banner) | 25 | 15 |
| 320×200 | 25 | - |
| 624×392 (screen backdrop) | 40 | 25 |
| 640-688 × 256-384 (battle background, wide scene) | 40 | 25 (688×256) |

The official 10-25 matches the newer prices; the older 40 for large scenes no longer applies.

## Typical jobs, measured

| Job | Generations |
|---|---|
| A monster sprite (Pro Flash 200×200, the current pick) | 6 · pixflux draft 1 |
| A hero sprite (Pro Flash 96×200) | 6 |
| A battle background (Pro 640×256) | 25 (was 40) |
| A screen backdrop (Pro 624×392) | 25 (was 40) |
| An icon (pixflux 64 → downscale) | 1 · (Pro 40², many candidates) 15 |
| Hero melee move, house process (2 poses 192×256 + 10-frame swing + 6-frame swing for the crescent) | 9 + 9 + 8 + 5 = **31** |
| Hero non-weapon move (2 poses 192×256 + 10-frame swing) | 9 + 9 + 8 = **26** |
| Hero melee move on 192×200 (forward-only: thrusts, bashes) | 6 + 6 + 6 + 4 = **22** |
| Pixflux `--draft` preview before a Pro image | 1 |
| Boss move (2 poses at 256² + 6 frames) | 9 + 9 + 6 = **24** |
| Re-animating an existing move at 256², 9 frames (reuse its key poses) | **8** |
| … spliced to 11 frames (3 in-betweens in the fastest span) | 8 + 4 = **12** (Korrath pilot: 3 moves, 64 incl. re-rolls) |
| Gun/bow shot (2 poses 192×200 + 10-frame motion, VFX free) | 6 + 6 + 6 = **18** |
| 8-direction shot, cheap route (front edit + v3 rotations + 5 directions animated, 4 re-rolled, 3 mirrored) | 6 + 3 + 35 + 28 = **72** |
| 8-direction move, exact route (per direction: 2 poses + animation) | ~18 × 5 + 9 = **~100** |
| Old-style 4-frame attack on a 96×200 hero | 2 |
| Walk cycle from a 64 px copy (8 frames) | 1 |
| A painted VFX clip | 0 |
| 5 base classes × (attack + skill), incl. one re-roll, one refunded failure | 239 (balance-checked) |
