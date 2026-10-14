# Changelog

## 1.2.1 - 2026-10-14
- Data sharing stays consent-only (off by default). New: shared results are reviewed weekly and their
  lessons released to all users as a skill update; each weekly entry here says what changed because of
  shared data and how many shared jobs it came from. Raw records are never published.

## 1.2.0 - 2026-10-14
Built for people who have never used PixelLab.
- "Let your AI assistant set it up": SETUP_FOR_AI.md walks any assistant through installing, connecting
  PixelLab and checking it; the user only installs Python if missing and runs one command with their token.
- `/pga-start`: a guided first project - three starter assets that fit the chosen style, a 1-generation
  draft before each, a plain sentence at every step, and a wrap-up of what was spent and what to try next.
- Beginner mode (asked at setup, on by default; `/pga-start off`): short explanations and drafts first.
- Every job ends with a plain summary - what was made, how it looks, cost and what's left, the next
  steps as exact commands; the detailed table with `--verbose` or for batches.
- Plain-language error guide (references/errors.md) for connection, token, balance, tier, failed,
  slow and flagged jobs; `profile.py` for project settings.

## 1.1.0 - 2026-10-14
Easier first ten minutes, more control after.
- Shorter setup: plan, art style (reference image, or setting + pixel size + view; "advanced" for
  colours, outline, shading, light, dithering), engine (default: just PNGs), output folder, sharing.
  Unanswered = default; typos get one question with the closest options; pixel size defaults to mid.
- Compact output: one line per PixelLab call (tool + settings), full JSON with `--verbose`; the plan
  line shows the expected wait ("starts now, ~10 min").
- New `/pga-history` (past jobs, cost, spend per day/command) and `/pga-reroll` (redo a result with a
  new seed or one wording change); `/pga-style anchor <family> <image|last>` approves a result as the
  reference art for its kind.
- README: "Your first ~20 generations" walkthrough with costs and waits, a glossary, and import notes
  for Godot, Phaser, Unity, GameMaker and others.
- Non-generating commands no longer load the shared generation instructions (less context, cheaper).

## 1.0.0 - 2026-10-14
First versioned release (everything before this was unversioned work on one game).
- 16 commands: init, style, analyze, prompt, char, bg, scene, building, icon, anim, vfx, batch,
  doctor, feedback, tech, help. Same skill as an Agent Skills package for Codex, Gemini CLI,
  Cursor, Copilot, OpenCode (`pixellab-agent-skill`), with per-task models via `install.py --agent`.
- Setup conversation (`/pga-init`): plan tier, art style from parameters or a reference image,
  engine, output folder, sharing choice; several named art styles per project (`/pga-style`, `--style`).
- Every PixelLab call shown with its parameters and cost; no permission prompts; no repeated calls;
  a results table with generations used and balance before → after.
- Plan tiers: parallel-job limits and fallbacks for the six Tier-1+ tools.
- Opt-in sharing of job outcomes (`/pga-feedback`), off by default; `/pga-doctor` setup check;
  `/pga-tech` explanations; one-command install / uninstall.
