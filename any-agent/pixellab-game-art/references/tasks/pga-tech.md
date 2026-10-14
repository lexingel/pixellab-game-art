# Task pga-tech

Run when the user asks for `pga-tech` (with or without a slash) or describes this job in plain words.
Input: <question> | explain <command | script | step | concept | last | folder>  (e.g. "why pad the canvas", "explain /pga-anim", "explain scrub.py", "explain last")

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

Question: **(the user's request)**

Answer technical "why" and "how" questions about this skill. No PixelLab generation here.

**Two modes, picked from the input:**
- **A question** ("why …", "how does …", "what decides …"): answer it as below.
- **`explain <target>`**: a step-by-step walkthrough of how the skill performs that task.
  - `explain /pga-<cmd>` (or just the name): read `<skill>/references/tasks/pga-<cmd>.md`, then only
    the reference sections it names. Give the numbered pipeline as the command runs it, one line per
    step: **what happens · tool or script (key params) · why · cost**. End with the total cost range
    and where the files land. Mark optional steps (`--draft`, `--n`, re-rolls) as optional.
  - `explain <script>.py`: its docstring, inputs/outputs, the main algorithm in 3-6 steps (what it
    measures or changes, thresholds and defaults), when the pipeline calls it, what it can't do.
  - `explain <step or concept>` (e.g. "key poses", "dynamic layer", "splice", "ground snap",
    "style anchors", "precedence"): definition in one line, the mechanism, where it lives
    (file → section), the measured reason it exists.
  - `explain last` or `explain <folder | asset>`: reconstruct what was actually done for that job
    from this session's tool calls and `<out>/log.jsonl` (tool, prompt, params, seed, cost, job id,
    scripts run on the result), in order, and point out any step that deviated from the standard
    pipeline and why.
  - Unclear target: list the 3 closest matches (commands, scripts, concepts) and stop.

**Where to look, in order (stop as soon as the answer is grounded):**
1. `<skill>/references/rationale.md` - the reasons behind each design choice, with pointers.
2. The file it points to (`<skill>/references/animation.md`, `costs.md`, `pixellab_api.md`,
   `prompt_improver.md`, `parameters.md`, `vfx.md`, `library/<type>.md`) - read only the section needed.
3. The script itself (`<skill>/scripts/<name>.py`) when the question is about what code does: read its
   docstring first, then the function in question.
4. About a job that just ran in this session: the actual tool call and parameters in the
   conversation, and the last lines of `<out>/log.jsonl` (prompt, tool, params, seed, cost, job id).
5. Still unknown: say so in one line, and name what would settle it (a `--draft`, a `search_help`
   question to PixelLab's docs agent, or https://api.pixellab.ai/mcp/docs).

**How to answer:**
- Questions: lead with the answer in one or two sentences, then the mechanism, then the evidence
  (measured numbers, the test that showed it), then the trade-off or alternative. Usually 3-8 lines.
- Walkthroughs: a numbered list or a compact table, no intro paragraph; as long as the pipeline
  needs, no longer.
- Cite the file (and section or line) the answer comes from.
- Use exact numbers (costs, sizes, frame counts, timings) instead of adjectives.
- A failure or bad result: state the cause, the fix, and its cost. No apologies, no reassurance,
  no praise, no filler ("great question", "I hope this helps"). If the skill's choice was wrong for
  this case, say so plainly and say what to change.
- If the user asks for more depth, go one level down (the code path or the measurement), not wider.
- Distinguish what is **measured** (from logs/tests) from what is **inferred**.

Don't call any PixelLab tool from this command. Don't rewrite files; if a reference is wrong or
missing a reason, say which line to change.
