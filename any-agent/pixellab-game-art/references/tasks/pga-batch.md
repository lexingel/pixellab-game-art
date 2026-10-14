# Task pga-batch

Run when the user asks for `pga-batch` (with or without a slash) or describes this job in plain words.
Input: <type>: item, item, item…  |  <file.csv or .txt, one item per line>  [--dry] [--draft]

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's request: **(the user's request)**

Read: `<skill>/references/library/house_rules.md` and the library file for each type in the batch.

1. **Items**: from the list in the arguments, or a CSV/TXT file (`type,prompt[,size][,ref]` or one
   prompt per line). Mixed types are fine - group them by command type (char / bg / scene /
   building / icon). Animations and VFX are not batched - use `/pga-anim` / `/pga-vfx`.
2. **Improve every prompt** with that type's rules (prompt_improver §3-4). Keep one anchor and one
   seed per type so the set matches.
3. **One table**: `# | type | improved prompt (short) | tool | size | cost` + total, and balance.
   Then the call block for every job (prompt_improver §5). `--dry` stops here; otherwise submit
   without asking (a `max_cost` cap stops before submitting and prints the override flag).
4. **Submit every job in the same turn** up to the tier's limit (`<skill>/references/pixellab_api.md` → Subscription tiers); send the rest when
   the first finish. Write `jobs.txt` (`name job_id [frames] {meta}`), then one
   `python <skill>/scripts/fetch.py --jobs <out>/jobs.txt --out <out> --log <out>/log.jsonl`.
   FAILED lines are refunded - resubmit them once, in one go.
5. **QA everything at once**: `qa.py <out>/*.png [--anchor …] --sheet <out>/flagged.png`; then one
   half-size contact sheet of the whole batch (`contact_sheet.py … --scale 0.5`, 6-8 per row).
   Look at the sheet once and the flagged sheet if any.
6. **Report**: the prompt_improver §8 results table (one row per job: tool, job id, generations,
   status OK / flagged + why, file), total vs estimate, balance before → after, the sheet, and a
   ready-to-run `/pga-batch` line for the items worth re-rolling (with the wording change).
