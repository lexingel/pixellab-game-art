# Task pga-scene

Run when the user asks for `pga-scene` (with or without a slash) or describes this job in plain words.
Input: <scene idea> [backdrop|story|map] [--ref image.png] [--draft] [--dry]

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's request: **(the user's request)**

Read: `<skill>/references/library/house_rules.md`, `<skill>/references/library/scenes.md`.

| Kind | Tool | Size | Notes |
|---|---|---|---|
| Hub / menu backdrop | `create_image_pro` | 624×392 (Pro max 16:10 ≈ 632×424) | keep UI/button areas calm |
| Story / cutscene picture | `create_image_pro` | 288×120 or 640×272 | one moment, one focal subject |
| Region map | `create_image_pro` | 640×400 | top-down, readable paths, no labels |

Profile seed, `no_background: false`, style ref = anchor `scenes`. Cost 15-25. `--draft` = pixflux first.

Improve: one moment, one focal point, fore/mid/background; light story (warm vs cold); for
backdrops say where empty space must be; negatives `no text, no letters, no UI, no frame` (+`no labels` for maps).
Clean plate for clickable props: generate the scene, then edit "the same room, empty, without <props>".
Panoramas merge buildings - make each with `/pga-building`.

QA: `qa.py <file> --opaque --anchor <anchor>`.
