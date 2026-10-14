# Task pga-bg

Run when the user asks for `pga-bg` (with or without a slash) or describes this job in plain words.
Input: <scene idea> [--ref background.png] [--draft] [--cheap] [--dry]

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's request: **(the user's request)**

Read: `<skill>/references/library/house_rules.md`, `<skill>/references/library/backgrounds.md`.

- Default `create_image_pro`, profile `sizes.background` (640×256), seed, **`no_background: false`**,
  `style_image_url` = anchor `backgrounds`, `style_copy: ["outline","detail","shading"]`. Cost 25.
- `--cheap`: `create_image_pixflux` 320×200, `color_image_url` = anchor. Cost 1.
- `--draft`: pixflux preview only (1); prints the command for the full Pro job.

Template:
```
<look> battle background, side view, wide landscape, no characters, open flat <ground> along the
bottom third for fighters: <scene>, <2-4 landmarks>, palette of <3-4 colours>
```
Improve: clear flat ground along the bottom third (clutter to the middle/back); 2-4 landmarks;
one light story (moonlight, torches, a glowing portal…); muted palette so sprites read on top;
negatives `no characters, no people, no text, no UI`. Several regions = one call each, same anchor + seed.

QA: `qa.py <file> --opaque --anchor <anchor>`. Review: ground clear, horizon not too high, no
figures/text, edges don't cut a landmark.
