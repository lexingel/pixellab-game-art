# Task pga-prompt

Run when the user asks for `pga-prompt` (with or without a slash) or describes this job in plain words.
Input: <any PixelLab prompt or idea>

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's prompt: **(the user's request)**

Read `<skill>/references/prompt_improver.md` §1-5, `<skill>/references/library/house_rules.md` and the one
library file for the detected type (`characters`, `backgrounds`, `scenes`, `buildings`, `icons`,
`animation` + `pose_edits`, `vfx`). Use `pixellab.json` if present.

1. Detect the asset type → the command that would make it. If two fit, pick one and say why.
2. Check (§3) and rewrite (§4) with that category's template; cost from `<skill>/references/costs.md`.
3. Show the §5 block and one line with the command to run it, e.g.
   `/pga-char <improved prompt> --ref <anchor>`.

Never call a PixelLab tool here (not even get_balance).
