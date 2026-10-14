# Task pga-building

Run when the user asks for `pga-building` (with or without a slash) or describes this job in plain words.
Input: <building or prop idea> [--tiers 3] [--ref building.png] [--draft] [--dry]

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's request: **(the user's request)**

Read: `<skill>/references/library/house_rules.md`, `<skill>/references/library/buildings.md`.

- `create_image_pro` small (≤ profile `building_max`, 170): returns 4-16 candidates - pick the best.
  Profile seed, `no_background: true`, style ref = anchor `buildings`. Cost 10-15.
- Template: `single <building>, flat side elevation, not isometric, <materials>, <2-3 details>,
  night, warm light from the windows, no people, no text, whole building fits inside the canvas
  with a small margin, <look>`
- `--tiers N`: tier 1, then each next tier with `edit_image_pro_flash` on the previous:
  `grow this <tier n> into <tier n+1>: <changes>, same pixel art style and palette` (seed 1 or 3).
  Cost 5-6 each at ≤200 px.

Improve: one building per call; materials + one signature feature (forge glow for a smithy, a
sign shape without letters for a tavern). Cropped roof → edit "zoom out: draw this same building a
little smaller so it fits with ~4 px transparent margin; keep design, colours, bottom position".

QA: `qa.py <candidates> --anchor <anchor>` (edge contact = cropped); pick from the half-size sheet.
