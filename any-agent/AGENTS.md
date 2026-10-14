# AGENTS.md

This folder contains **pixellab-game-art**, a skill for making pixel-art game assets with the
PixelLab MCP tools (sprites, backgrounds, buildings, icons, attack/skill animations, VFX).

When the user asks to set this skill up or install it: follow `SETUP_FOR_AI.md`.

When the user asks for pixel-art game assets, a PixelLab job, or a task named `pga-<something>`:
1. Read `pixellab-game-art/SKILL.md` and follow it.
2. For a named task, read `pixellab-game-art/references/tasks/<task>.md` and its shared loop
   `pixellab-game-art/references/prompt_improver.md`. Read only the files they name.
3. If a subagent named `pga-<task>` exists, delegate the task to it (it runs on the model chosen
   for that task); otherwise do it yourself. pga-init, pga-style and pga-analyze ask the user
   questions - always run those yourself.
4. Working rules: print every PixelLab call with its full parameters and cost before submitting;
   never ask for permission or confirmation; never repeat a call; end with the results table
   (generations per call, total, balance before -> after, files).
