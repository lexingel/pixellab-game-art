# Task pga-icon

Run when the user asks for `pga-icon` (with or without a slash) or describes this job in plain words.
Input: <icon idea> [--size 32|40|64] [--tiers] [--ref icon.png] [--dry]

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's request: **(the user's request)**

Read: `<skill>/references/library/house_rules.md`, `<skill>/references/library/icons.md`.

- Generate at profile `icon_gen` (64), box-downscale to `icon_final` (40 items / 32 skills) so
  pixels stay whole. `create_image_pixflux` (1) for sets; `create_image_pro` ~40 px (10-15, many
  candidates) to match a polished set. `no_background: true`, seed, style ref = **one** icon
  (anchor `icons`; a grid of icons makes Pro wrap candidates across corners).
- Template: `pixel art game icon, a single <object>, <material + 1-2 details>, centred, filling the
  frame, thick dark outline, strong highlight and shading, no frame, no square, no backdrop, no text`
- `--tiers`: rare = polished blue steel + silver + blue sapphire; epic = dark steel + ornate gold
  filigree + glowing violet gem, faint violet glow - via `edit_image_pro_flash`
  `Same <item>, same shape, size and position, upgraded to a <rare|epic> version: … Transparent background.` (5 each)
- Many icons → use `/pga-batch` (one sheet, one wait).

Improve: one object, silhouette first; class/school colour family for skill icons; say what it
must NOT be when ambiguous ("a lion-head shield, NOT a lion").

QA at the final size: downscale first (Pillow `Image.BOX`), then `qa.py`, then look.
