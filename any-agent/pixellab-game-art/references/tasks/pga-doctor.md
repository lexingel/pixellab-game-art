# Task pga-doctor

Run when the user asks for `pga-doctor` (with or without a slash) or describes this job in plain words.
Input: (no arguments)

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

No generation (only the free `get_balance` call). Run every check, then print one checklist.

1. **PixelLab connection:** call `get_balance`.
   - No PixelLab tools available → `✗ PixelLab not connected` + the connect steps from
     `<skill>/references/prompt_improver.md` §0 (for this agent).
   - Auth error → `✗ token rejected` + "get a new token at https://api.pixellab.ai/mcp and re-add the server".
   - OK → `✓ PixelLab: Tier N (name), balance B generations, resets <date>, M jobs at once`.
2. **Python + packages:** `python <skill>/scripts/check_setup.py pga-anim` (try `python3`, then `py` on
   Windows, if `python` isn't found) - it checks Python and Pillow / numpy / scipy and prints fixes.
   Report which python command works; the other commands will use that one.
3. **Project** (current folder):
   - `pixellab.json` missing → `• no project setup yet - run /pga-init` (not an error).
   - Present → `python <skill>/scripts/style.py list` (styles, active one), `tier` vs what `get_balance`
     showed (differs → say so and that the next command will update it), `engine`, `out` (exists?
     can be created?), `max_cost`.
4. **Sharing:** `python <skill>/scripts/share.py status` (level, since when, install id or none).
5. **Version:** read `<skill>/VERSION` (and `<skill>/../CHANGELOG.md`'s top entry if present) - say which version is installed.

Print:
```
pixellab doctor
✓/✗ PixelLab   …
✓/✗ Python     …   (use: python3)
✓/✗ Packages   …
•   Project    …
•   Sharing    …
•   Skill      version …
Fix first: <the single most important fix, as an exact command - or "nothing, you're ready: try /pga-char <idea> --dry">
```
