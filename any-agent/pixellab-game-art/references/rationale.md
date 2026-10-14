# Rationale: why the skill does what it does

Short reasons behind each design choice, each with the file that holds the detail. Read by
`/pga-tech`. Keep entries to the reason, the evidence (measured numbers, tests), and the trade-off.

## Pipeline and plumbing

- **PixelLab via MCP tools, not REST/curl.** The tools handle auth and job tracking, and the
  account's generations are billed the same way. The REST "API v2" is for runtime generation
  in shipped code, not for this skill. → `pixellab_api.md` "How the service behaves".
- **Every job is async → `fetch.py` waits and downloads.** Create/edit/animate return a job id
  immediately; results arrive 10 s to 15 min later. `fetch.py` polls the no-auth download URL,
  writes the files, and logs one JSON line per job. Stdlib only, so it runs without installs.
  Failed jobs (404/410) are refunded by PixelLab → resubmit, don't wait. → `scripts/fetch.py`.
- **Output folders are chosen by the instructions, not code.** `prompt_improver.md` §6 tells
  the agent the path (`pixellab.json` `out`, else `./pixellab_out/<command>/<slug>/`); `fetch.py`
  writes wherever it is told. Set `out` for a fixed location.
- **`log.jsonl` per job.** Prompt, tool, params, seed, cost and job id for re-rolls ("same, but…")
  and for `cost_report.py`. The tool result's reported cost is what was charged.
- **Uploads instead of base64.** MCP clients truncate long base64 arguments and corrupt the image.
  `get_upload_url` + `upload.py` gives an `upload:<id>` usable anywhere a URL is (kept 3 days).
  Base64 is fine only for tiny images (≤ ~48 px, e.g. one icon as a style image).
- **Submit independent jobs in one turn.** Up to the tier's limit run in parallel (trial 1, Tier 1 8,
  Tier 2 10, Tier 3 20); total wait = slowest job. Submitting past the limit only queues or refuses.
- **Tier-gated tools get a planned fallback.** Six tools need Tier 1+ (`inpaint_image` >256 px Tier 2+);
  credits don't unlock them. Planning the fallback up front avoids a refused call and a retry.
  → `pixellab_api.md` "Subscription tiers".
- **Pillow + numpy are for local pre/post steps, not the API call.** Padding, palette checks,
  flash detection, scrubbing, ground snap, sheets/GIFs. These are exact pixel fixes the generator
  can't be told to do; doing them locally costs 0 vs 6-9 per re-roll. numpy makes per-pixel scans
  of every frame fast. Without them, generation still works; only those scripts fail.
- **QA before looking.** `qa.py` flags empty images, non-transparent backgrounds, cropping, palette
  drift and animation flashes, so the agent only opens flagged images. Reading images is the most
  expensive thing for the agent in tokens. → `scripts/qa.py`.

## Tool choice

- **Pro Flash for sprites and key poses.** Cost by longest side: ≤96 → 5, ≤200 → 6, >200 → 9
  (measured over 214+ jobs). Close to Pro quality at a third of the price. → `costs.md`.
- **Pro for icons and small props.** One call returns many candidates (64 at ≤32 px, 36 at 40 px)
  for 10-15 gens, so picking beats re-rolling. → `library/icons.md`.
- **Pixflux (1 gen) for drafts.** `--draft` previews composition before a 6-25 gen job.
- **`style_copy` without `color_palette`.** Keeps outline weight, detail and shading of the anchor
  but lets new subjects take their own colours.
- **`use_color_palette_correction` on edits.** Keeps an edited pose on the source sprite's palette;
  without it the edit drifts in hue.
- **vfx_workbench for effects (free).** Effects drawn into body frames can't be timed, recoloured or
  reused; a separate clip can. → `vfx.md`.

## Animation

- **Padded canvas.** A standing sprite is cropped tight; asked for a big swing on that canvas the
  model has nowhere to put the weapon, so the body barely moves. 192×200 (16 gens/move) when the
  weapon stays below the head, 192×256 (23) otherwise; the engine grows the rect by the recorded
  offset so scale and feet don't move. → `animation.md` "Why padding".
- **Two key poses, then interpolate.** Prompt-only `animate_image` invents the motion: weak moves,
  mutating weapons, random flashes. Fixing both ends (wind-up A, hit B) leaves the model only the
  in-between to invent. → `animation.md` "Key poses".
- **The "dynamic layer" in pose prompts.** Exaggerated pose + stance depth + torso lean + soft parts
  in motion: tested to match Pro's dynamism at Pro Flash cost. → `animation.md`.
- **Motion-only `action` text.** Re-describing the character or naming fire/glow re-lights the whole
  body; the action describes only the path of the limb/weapon.
- **11 frames (frame_count 10).** Smoothness is judged by pixels moved per frame; mixing 7- and
  11-frame moves on one character reads as a stutter. Longer moves above the 256² canvas cap are
  spliced from two takes (fastest span re-animated).
- **Timing: hold wind-up, fast swing, hold hit, settle.** Even timing reads as floaty; the holds sell
  weight. Heroes light (~60 ms/frame), bosses heavier. Impact fires on the frame before last. →
  `animation.md` "Timing".
- **Scrub vs drop.** Off-palette flash pixels (colours not in pose A/B) can be cleared by `scrub.py`;
  flashes in the character's own colours can't be separated → drop or re-roll.
- **Ground snap.** Poses float up to ~20 px; `ground_snap.py` aligns the lowest opaque row per frame.
- **Shots: no crescent; the generator's flash marks the muzzle.** `find_muzzle.py` uses it to place
  your own effect, then the generated flash is cleared. → `animation.md` "Shots".
- **8 directions: rotate, animate 5, mirror 3.** v3 rotation from a south-facing reference costs 3;
  animate is billed on its own ~224² canvas (7/direction); "forward" means screen-right to the model,
  so directions use screen words. → `animation.md` "8 directions".

## Prompts and style

- **Outcomes are logged locally; sharing is opt-in.** Every job gets an outcome line (QA flags,
  keep/reroll/reject, the user's reason) in its `log.jsonl` - the raw material for new lessons.
  Sending it to the skill's authors is off by default; `stats` sends numbers and enums only,
  `prompts` adds prompt text and reasons. Paths, URLs, images, names and the token are never sent
  (the script and the server both whitelist fields). `share.py forget` deletes an install's records.
- **Named styles, edited by a script.** A project can mix looks (a cozy town, a dark dungeon); each is
  saved under the user's name and picked with `--style` or `active_style`. `style.py` writes the JSON
  so a typo in the chat can't corrupt the profile. → `parameters.md` "Named styles".
- **Setup asks; jobs don't.** The plan tier and the art style are the user's to choose (tier sets
  parallel jobs and fallbacks; style sets every prompt), so setup asks once. After that the skill runs
  without confirmations.
- **One style anchor per asset family.** Several references average into mush; one approved image
  per family keeps sets coherent. → `prompt_improver.md`, `parameters.md`.
- **Precedence: user's words > flags > profile rules > preset > house.** So a one-off request never
  silently loses to a saved default. → `parameters.md`.
- **Seeds fixed by default (7, then 11).** Re-rolls change one thing at a time.
- **Analyse own art at native scale.** Upscaled art is measured at 1 px = 1 pixel, otherwise colour
  counts and outline widths are wrong. → `scripts/analyze_style.py`.

## Budget

- **Estimate before batches.** Costs are known per tool and size (`costs.md`); a batch states its
  total before submitting.
- **Contact sheets for picking.** All candidates on the target background at 3×, numbered, in one image:
  one look instead of dozens.
