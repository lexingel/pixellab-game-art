# Task pga-help

Run when the user asks for `pga-help` (with or without a slash) or describes this job in plain words.
Input: [command]

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

Asked about: **(the user's request)**

Print this (or, if a command was named, just its row plus its argument hint and 2 examples):

{{COMMAND_TABLE}}

Flags for every generating command: `--dry` (show the improved prompt and cost only), `--draft`
(1-generation preview first), `--ref <image>` (match this asset), `--n 3` (variations), `--size WxH`,
`--style <name>` (one of your saved art styles for this call).
Style: `--setting scifi|cozy|western|…` `--density low|mid|high` `--colors 16` `--palette <file|hex,…>`
`--outline dark|selective|none` `--shading flat|soft|detailed` `--dither` `--light top-left` `--view side|top-down|iso`.
Animation: `--frames 9` `--timing light|heavy|even|custom` `--fps 10` `--fx crescent|streak|none|keep` `--hit N` `--loop` `--dirs 8` (top-down: rotate + 8 facings).
All of them can be saved as project defaults (`/pga-init`, `/pga-analyze`); every value is listed in the
skill's `references/parameters.md` (full path: <skill>/references/parameters.md - print R expanded).
Start with `/pga-init` (or `/pga-analyze <your art>`), then `/pga-prompt` to see how your ideas get improved for free.
No profile yet? The first generating command starts the `/pga-init` setup (plan, art style, a name to save it under), then does your request.
Every command prints each PixelLab call with its parameters and the cost before it runs, never asks for permission, and ends with a results table (generations used, balance before → after, files).
Costs per tool: `<skill>/references/costs.md`. Don't call any PixelLab tool from this command.
