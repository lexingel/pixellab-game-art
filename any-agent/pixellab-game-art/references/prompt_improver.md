# The pga-* task loop (shared by every command)

setup check → project profile → parse → check the prompt → pick the tool and rewrite → show →
generate → automatic QA → look (only where needed) → report. Every step is written to keep both
PixelLab generations and model tokens low.

`<skill>` below = this skill's folder (the one holding SKILL.md). Run scripts as
`python <skill>/scripts/<name>.py …` (or `python3 …`). Task names (`pga-anim`, `/pga-anim`, …) are
the steps in `<skill>/references/tasks/<name>.md`; the user may name one or just describe the job.
Show your work: every PixelLab call is printed with its parameters (§5), and every run ends with the
results table (§8).

## 0. Setup check (first pga-* task command of a session)

Skip for `/pga-prompt` and `/pga-help`. Remember the result for the session.

1. **PixelLab connection** - call `get_balance` (free).
   - No PixelLab tools → the MCP server isn't connected to this agent. Stop and show:
     1. Get an API token at https://api.pixellab.ai/mcp (signed in to PixelLab).
     2. Put it in an environment variable `PIXELLAB_TOKEN`, then add the MCP server for this agent -
        the exact command/config per agent (Codex, Gemini CLI, Cursor, VS Code/Copilot, OpenCode,
        the agent) is in the package README → "Connect PixelLab"; show the user the one for this
        agent. Generic: server `pixellab`, URL `https://api.pixellab.ai/mcp`, HTTP (streamable),
        header `Authorization: Bearer <token>`.
     3. Restart the agent, ask again.
     Never ask for the token in the chat, never print or store it.
   - Auth error → token wrong/expired: same steps with a new token.
   - Balance 0 → say so; `/pga-vfx` still works (the workbench is free).
2. **Local tools** - `python <skill>/scripts/check_setup.py <command>` (stdlib; try `python3` if `python`
   isn't found). Missing Python → https://www.python.org/downloads/. Missing packages → print
   `pip install pillow numpy scipy` for the user to run and carry on with what works without them
   (generation and download do; QA/cleanup scripts don't). Never install anything yourself.
   If it prints an `update` line (checked at most once a week), add "update X is out - `/pga-update`" to
   the setup line below; don't update unasked.
3. **Tier** - read it from `get_balance`'s `subscription:` line (trial/none or credits-only = Tier 0);
   if it can't be read, use `pixellab.json` → `tier` (asked at setup); neither → Tier 1. If the two
   disagree, trust `get_balance` and update `tier` in the profile. Keep it for the session: it sets
   how many jobs run at once and which tools need a fallback ([pixellab_api.md](pixellab_api.md) → Subscription tiers).
4. One line: `Setup: PixelLab OK (Tier N, balance B, M jobs at once) · python OK · packages OK`
   (or what's missing + fix).

## 1. Project profile

If `pixellab.json` exists in the project root (made by `/pga-init`, extended by `/pga-analyze`), read
it and use it as the defaults: look words, palette words, negatives, facing, sizes, anchors (style
references per asset family), seed, output dir, engine, the optional cost cap `max_cost`, and the style
parameters `setting`, `density`, `colors`, `palette_hex`, `outline`, `shading`, `dither`, `light`,
`view`, `anim{…}` and the plain-language `rules` list. What each one does and the precedence
(user's words > flags > profile rules > setting preset > house defaults):
[parameters.md](parameters.md) - read it whenever any of these is set or flagged.
**Named styles:** the style in use is `--style <name>` if given, else `active_style`; overlay its
fields on the top-level ones ([parameters.md](parameters.md) → Named styles) and print
`Style: <name>` in the plan line. Unknown name → list the saved ones and stop.

**No `pixellab.json` yet → setup first, then the request.** Send the `/pga-init` step-1 message and
stop (say "your request - <short> - runs as soon as this is saved"). When the user answers, finish the
`/pga-init` steps (show the setup, save on "save <name>"), then run the original request without
being asked again. Skip it for `/pga-prompt`, `/pga-help`,
`/pga-tech`, `/pga-vfx` (free) and `/pga-anim` (the sprite itself is the style reference). With
`--dry`, ask nothing: use the house defaults and say they are placeholders. Setup questions are the
only questions the skill asks; it never asks permission to run a job.

## 2. Parse

The text after the command is the user's prompt. Flags anywhere in it:

| Flag | Meaning |
|---|---|
| `--dry` | improve and show only; don't call PixelLab |
| `--draft` | only a 1-generation pixflux draft at the same size; prints the command for the full job (no waiting for an answer) |
| `--ref <path or URL>` | style anchor for this job (overrides the profile's anchor) |
| `--size WxH` · `--seed N` · `--face left\|right` · `--out <dir>` | overrides |
| `--n N` | N variations in one go (different seeds, submitted together) |
| `--style NAME` | use that saved art style for this call ([parameters.md](parameters.md) → Named styles) |
| `--max-cost N` | stop before submitting if the plan costs more than N (prints the override; never asks) |
| `--verbose` | print every PixelLab call as its full JSON (default: one compact line per call) |
| `--setting` `--density` `--colors` `--palette` `--outline` `--shading` `--dither` `--light` `--view` | style parameters for this call ([parameters.md](parameters.md)) |
| `--frames` `--timing` `--fps` `--durations` `--fx` `--hit` `--loop` | animation parameters (`/pga-anim`; [parameters.md](parameters.md)) |

## 3. Check the prompt

Mark each present / missing / wrong:

1. **Concrete subject** - something drawable, not a concept.
2. **Body plan / layout** - creatures: build, material, limbs; scenes: fore/mid/background, open ground.
3. **Identifying details** - 2-4 props/colours that make it recognisable.
4. **View and facing** (profile `facing` for heroes/foes).
5. **Canvas fit** - "whole body fits inside the canvas with a small margin", "single object centred".
6. **Style words** - the user's style, else flags, else the profile (`rules`, `look`, `outline`,
   `shading`, `dither`, `light`), else the `setting` preset's look words, else the house look:
   *dark fantasy pixel art, muted colours, dark outline, light from above, detailed shading*.
   `density` adds its detail words and sets the size (parameters.md).
7. **Palette** - 3-4 named colours.
8. **Negatives** - what must not appear, plus the pitfall negatives for the subject from the
   library file (snipers with no firearm asked for → `medieval, no guns`; rock → `no metal`; birds → `not a dragon`;
   scenes → `no characters, no text`; icons → `no frame, no square`; idle / death / walk loops → `body motion only, no effects` - never on attack or skill swings, where it makes flashes worse; see animation.md).
9. **Tool, size, seed, background** - see §4.
10. **Style anchor** - profile anchor or `--ref`; if none, warn the set may drift and suggest
    `/pga-init` or approving the first result as the anchor.

## 4. Pick the tool, then rewrite

- Tool: the "Use first" column of `<skill>/references/pixellab_api.md` (read only the table and the one
  tool section you need). Cost: `<skill>/references/costs.md`. Prefer the cheaper tier when it changes
  nothing visible: Pro Flash costs 5 / 6 / 9 by longest side (≤96 / ≤200 / >200 px), so don't
  pad past 200 px unless the job needs the room.
- Rewrite with the category template from `<skill>/references/library/<category>.md` (+ `house_rules.md`).
  Order: subject → body/layout → details → view/facing → canvas fit → style → palette → negatives.
- **Never drop a user detail**; turn vague words into drawable ones; keep their names for things.
  A user detail beats a pitfall negative: skip any negative that contradicts the request
  (rifle → no `no guns`, metal golem → no `no metal`).
- One subject per call. Under ~70 words for Pro/pixflux.
- Profile `rules` are applied every time, each where it fits (colours → §7 step 4, timing → the
  animation export, words → the prompt). Name the rules you applied in "Changed".
- Never ask for permission or confirmation. Ask only when the job can't run at all without an
  answer (e.g. no sprite given for an animation): one question, with your default.

## 5. Show

```
Original:  <their text>
Improved:  <the prompt>
Changed:   • <2-4 key fixes>
Plan:      <n> call(s) · ~<total> generations · ~<time> · balance <b> → ~<b - total> · Style: <name>
→ <tool>  <W>x<H> · seed <n> · <ref: style anchor / sprite / none> · <other set parameters> · ~<cost>
```
One `→` line per PixelLab call, before submitting it: the tool and every parameter you set except the
prompt (shown once above) - short values only (`upload:ab12…`, never base64). **`--verbose`** (or
`pixellab.json` → `"output": "verbose"`) prints each call as its full JSON instead:
```
→ <tool_name>
  { "description": "<full prompt>", "width": W, "height": H, "seed": n, "no_background": true,
    "<every other parameter you pass>": …, "style_image_url": "<url or upload:id - not base64>" }
  cost ~<n>
```
**Time** for the plan line, per job (they run in parallel, so the plan's time = the slowest job):
pixflux under 1 min · Pro 1-10 min · Pro Flash 7-15 min · animate_image / animate_character 1-3 min ·
vfx_workbench instant. Say "starts now, ~<time>" so a long wait doesn't look like a hang.

**Beginner mode** (`pixellab.json` → `"beginner": true`, set at setup; `/pga-start off` turns it off):
add one plain sentence before the plan on what is about to happen and why (which PixelLab model,
what it costs, how long), and define any word from the README's "Words used" list the first time
it appears. Jobs costing 6 or more start with a 1-generation `--draft`, shown with "`go` makes the
real one (~<cost>, ~<time>) · tell me what to change · `skip`" - the beginner's choice, not a
permission prompt. Without beginner mode, no explanations and no automatic drafts.

`--dry` stops after printing the plan. Otherwise submit straight away - no confirmation.
If the profile or a `--max-cost N` flag sets a cap and the plan exceeds it, don't submit: print the
plan and `re-run with --max-cost <total>` (that is a stop, not a question). An old profile's
`ask_above` counts as `max_cost`.

## 6. Generate

- Local images → `get_upload_url` once, then `python <skill>/scripts/upload.py <url> <files…>` → `upload:<id>`s.
- `--draft`: only the pixflux preview at the same size (seed, palette ref), 1 generation; show it
  and print the command that runs the full job. Don't wait for an answer.
- **Never repeat a call.**
  - Before submitting, check `<out>/log.jsonl`: the same tool + prompt + parameters + seed already
    done → reuse its files (say "reused job <id>, 0 generations"). A deliberate re-roll changes the
    seed or the wording and says so.
  - Never resubmit a job that is still running or timed out - run `fetch.py` on its job id again.
  - One `wait_for_jobs`/`fetch.py` per batch, not repeated `get_*` polling; `get_balance` once at the
    start (setup) and once at the end (report).
- Submit every independent job **in the same turn** (poses, variations, batch items), up to the
  tier's background limit ([pixellab_api.md](pixellab_api.md) → Subscription tiers); send the rest as jobs finish.
- Download + log with one call (no polling loops, no sleeping in the chat):
  write the job's meta (`{"cmd":"…","tool":"…","prompt":"…","params":{…},"cost":N}`) to `<out>/meta_<name>.json`, then
  `python <skill>/scripts/fetch.py <job> <out.png> --log <out>/log.jsonl --meta-file <out>/meta_<name>.json`
  (a file, not inline JSON: inline quotes break in PowerShell and on apostrophes like "knight's").
  - animations: `--frames <frame_count+1>` into a folder; several jobs: `--jobs jobs.txt --out <dir>`
    (one line per job: `name job_id [frames] {meta json}`).
  - fetch.py waits at most 100 s per run (agent shells stop commands at ~2 min). Pro Flash takes
    7-15 min and animations 1-3 min, so `TIMEOUT <name> <job> - still running` is normal: run the
    **same** fetch.py command again (it never logs a job twice) until every job is `OK`. If your shell
    allows longer commands or background runs, `--timeout 540` (or a background run) needs fewer rounds.
  - `FAILED` = refunded by PixelLab → resubmit once.
- Output dir: profile `out` or `./pixellab_out/<command>/<slug>/`.

## 7. QA, then look (only where needed)

1. `python <skill>/scripts/qa.py <files> [--opaque] [--anim] [--anchor <profile anchor>] --sheet <out>/flagged.png`
2. Images are the most expensive thing to read. Look at **one** sheet per job:
   `python <skill>/scripts/contact_sheet.py <out>/sheet.png <files…> --scale 0.5`
   - Nothing flagged and the request is routine → a quick look at the half-size sheet is enough.
   - Something flagged → look at `flagged.png` at full size.
   - Never open frames one by one.
3. Judge: subject right, readable silhouette, facing, matches the anchor, nothing invented.
4. **Enforce colour rules** (free): profile/flag `colors` or `palette_hex` →
   `python <skill>/scripts/apply_palette.py <palette.json|png|hex list|auto> <files> [--colors N]` before
   installing; say how many colours each file has after.
5. **Record the outcome** of every job (local, always - it is how the skill learns):
   `python <skill>/scripts/outcome.py <out>/log.jsonl <job_id> --verdict keep|reroll|reject|reused|failed
   --qa "<flags;…>" --est <estimated cost>` (the wait time comes from fetch.py's log line - don't time it yourself). When the user later reacts
   ("bad: the gun is in the wrong hand", "perfect"), record it again with `--verdict reject|keep
   --reason "<their words>"` (the latest outcome wins).

## 8. Report

Always end with the **plain summary** (call `get_balance` once for the "left" number; it is free):
```
Made:  <what, in the user's words> → <file>   (sheet: <path>)
Looks: <one honest sentence - matches the style / clean edges / what QA fixed>
Cost:  <sum> generations (estimate ~<est>) · <left> left, resets <date> · waited <from fetch.py's waited_s>
Next:  1. <the most useful next step, as an exact command, with its cost>
       2. <another>   3. <a re-roll with the one knob to turn, if it isn't perfect>
```
Good next steps: make it the reference (`/pga-style anchor <family> last`, free), animate it
(`/pga-anim <file> <move>`, ~16-31), a variation (`/pga-reroll last <change>`), a matching set (`/pga-batch`).
With `--verbose`, or more than three jobs, also print the detailed table:
```
| # | tool | job id | params (short) | generations | status | files |
|---|------|--------|----------------|-------------|--------|-------|
| 1 | create_image_pro | 3f2a… | 32x32 seed 7 | 10 | ok | pixellab_out/icon/helm/0.png |
```
Something failed → explain it in plain words with [errors.md](errors.md) (what happened, what you
did, the one thing the user may need to do) - never a raw error code alone.
Then, only if `pixellab.json` → `share.level` is `stats` or `prompts` (the user opted in at setup):
`python <skill>/scripts/share.py send --log <out>/log.jsonl --agent <your agent's name>` and add its one
line (`Shared: N record(s) (stats)`) under the table. At `off` (the default) skip it silently.
Failed jobs show `refunded` and 0. Reused jobs show `reused` and 0. A re-roll is automatic only for a
**hard defect**, at most once per item, and appears as its own row. Hard defects:
- found by `qa.py`: empty image, background not transparent (sprites), subject cut off at the canvas
  edge, animation frames of different sizes, a flash/blob over the body that `scrub.py` can't clear;
- found by looking (the one sheet): wrong subject, wrong facing, a requested item missing (weapon,
  colour, prop), a pose that doesn't read as the asked move (an attack that reads as standing).
Anything else (taste, small colour shifts, a slightly weak pose) is reported with its re-roll knob, not re-rolled.
