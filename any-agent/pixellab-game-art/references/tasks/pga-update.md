# Task pga-update

Run when the user asks for `pga-update` (with or without a slash) or describes this job in plain words.
Input: (nothing) | check | undo | from <downloaded zip or folder>

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's input: **(the user's request)**

No PixelLab calls. The skill gets an update every week (the lessons from shared results, fixes, new
commands). The user's `pixellab.json`, styles, logs and generated files live outside the skill folder
and are never touched.

- nothing / `now`: `python <skill>/scripts/update.py` - downloads the latest version, backs up this one,
  installs the new one with the same options as before and puts back every skill file the user edited.
- `check`: `python <skill>/scripts/update.py check` - one line: newer version or up to date.
- `undo`: `python <skill>/scripts/update.py rollback` - restores the version from before the last update.
- `from <zip or folder>`: `python <skill>/scripts/update.py --from <path>` - for a ZIP the user downloaded
  from the repository page (green **Code** button → Download ZIP) when the download fails.

After an update, in this order:
1. Print the "Updated A -> B" line and the "What's new" notes as the script printed them.
2. **Merge** every `MERGE` line: the user edited a file the update also changed. Read `<file>` (theirs)
   and `<file>.from-update` (the update's), write `<file>` = the update's version with the user's own
   additions and changes carried over (their wording wins where both changed the same lines), then
   delete `<file>.from-update`. One line per file: what came from the update, what was kept from theirs.
3. Say: restart the assistant so new or changed commands load; `/pga-update undo` reverts.

Errors: "could not check" / download failed → offline, or the repository isn't public yet; give the
`from <zip>` route. "installer failed" → show its output; nothing was lost (`undo` restores).
