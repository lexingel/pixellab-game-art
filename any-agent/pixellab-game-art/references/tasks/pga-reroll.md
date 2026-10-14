# Task pga-reroll

Run when the user asks for `pga-reroll` (with or without a slash) or describes this job in plain words.
Input: [last | <name or file or words>] [<what to change: "no cape", "brighter", "seed 11">]

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's input: **(the user's request)**

Follows the shared loop's §5-§8 (call block, no permission prompt, results table).
1. Find the job: `python <skill>/scripts/history.py <out>/log.jsonl --n 1 --json` for `last` (or no target),
   else `--find <words> --n 3 --json` - more than one match → list them (one line each) and ask which (the only question).
2. Same tool, size, style anchor and parameters as that job. Change exactly one thing:
   - the user said what to change → apply it to the prompt (keep everything else word for word);
   - nothing said → the seed (previous seed + 1, or 11 if it was 7), and say so.
   Animation jobs: re-run only the step that failed (a key pose, or the in-between) - see `/pga-anim`.
3. Print the call block and the cost; submit; fetch; QA and look as in §7.
4. `python <skill>/scripts/outcome.py <out>/log.jsonl <old job> --verdict reroll --reason "<what changed>"`, then
   the new job's outcome as usual. Results table: old file → new file, and which one to keep.
