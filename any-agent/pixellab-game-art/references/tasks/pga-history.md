# Task pga-history

Run when the user asks for `pga-history` (with or without a slash) or describes this job in plain words.
Input: [N] [--cmd pga-char] [--find <text>] [--cost]

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's input: **(the user's request)**

No PixelLab calls. `<out>` = `pixellab.json` → `out` (default `pixellab_out`).
1. `python <skill>/scripts/history.py <out>/log.jsonl --n <N or 15> [--cmd …] [--find …]` - print its lines as a table.
2. `--cost` (or the user asks what they spent): also `python <skill>/scripts/cost_report.py <out>/log.jsonl`
   and call `get_balance` (free) for the balance left and the reset date.
3. End with the two next steps that fit: `/pga-reroll <name>` for a result they didn't like,
   `/pga-style anchor <family> <file>` for one they want every later job to match.
