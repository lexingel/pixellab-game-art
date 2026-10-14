# Task pga-style

Run when the user asks for `pga-style` (with or without a slash) or describes this job in plain words.
Input: list | use <name> | show <name> | new | anchor <family> <image|last> | rename <old> <new> | delete <name>

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's input: **(the user's request)**

No generation here (except an optional 1-generation draft inside `new`).

- `list` (or nothing): `python <skill>/scripts/style.py list` and print it as is (`*` = active).
- `use <name>`: `python <skill>/scripts/style.py use <name>` - every command uses it from now on;
  a single call can still pick another with `--style <name>`.
- `show <name>`: `python <skill>/scripts/style.py show <name>`, then a short table field | value.
- `rename <old> <new>` / `delete <name>`: the same script; confirm the result in one line.
- `anchor <family> <image | last>`: approve an image as the active style's reference art for one asset
  family (heroes, monsters, backgrounds, scenes, buildings, icons, ui) - every later job of that family
  matches it. `last` = the newest kept file from `python <skill>/scripts/history.py --n 1`.
  Run `python <skill>/scripts/style.py anchor <family> <image> [--style <name>]` and print its line.
- `new`: say "run `/pga-init` - with a profile already here it only asks for the new art style
  (send a reference or pick parameters) and saves it next to the others". (Building a style reads
  images and asks questions, so it lives in `/pga-init`; this command only manages saved styles.)
- Unknown name: show `list` and stop.
