---
name: pga-start
description: "A guided first project for someone new to PixelLab: explains what happens at each step, suggests three starter assets that fit the saved art style, makes them one by one with a cheap draft first, and ends with what was spent and what to try next. Use when the user types /pga-start."
argument-hint: "[off | on]  (off/on: stop or restart the beginner explanations and drafts)"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-start

User's input: **$ARGUMENTS**

`off` / `on`: `python R/scripts/profile.py set beginner false|true`, confirm in one line, stop.
No `pixellab.json` or no saved style → run the `/pga-init` steps first, then come back here.

Speak plainly: one or two short sentences per step, no jargon without a word of explanation
(the README's "Words used" list has plain definitions). Follow the shared loop for every job.

1. **Welcome (one message):** PixelLab draws pixel art from a description; each job costs a few
   *generations* from the monthly allowance - they have <balance> left (`get_balance`, free; resets
   <date>). Then offer three starter jobs that fit the active style's setting and view, each with its
   cost, e.g. for a cozy top-down style:
   ```
   1. A hero - "a young farmer with a straw hat"   draft 1 + sprite ~6
   2. An enemy - "a grumpy green slime"            draft 1 + sprite ~6
   3. An item icon - "a wooden watering can"       ~10 (you pick from many candidates)
   Pick 1-3 (or "all", or describe your own). Total for all three: ~24.
   ```
   Fit the examples to the setting (sci-fi: a space marine, a drone, a plasma cell; horror: a lantern
   bearer, a ghoul, a rusty key; …). Below the tier's budget left → offer fewer.
2. **Each pick, one at a time:**
   - Say what you're about to do in one sentence ("I'll ask PixelLab for a quick 1-generation
     sketch first so we can check the idea before the real one").
   - Draft (pixflux, cost 1) → show it → "Looks right? `go` makes the real one (~6, ~10 min) ·
     tell me what to change · `skip`". (A beginner's choice, not a permission prompt.)
   - Real job → while it runs, one sentence on what PixelLab is doing ("Pro Flash is drawing it at
     96x200 with your style; this takes 7-15 minutes").
   - Result in plain words (shared loop §8 "plain"): what was made, where, what it cost, what's left,
     one sentence on how it looks, and the 2-3 next steps.
   - After the first good character: suggest `/pga-style anchor <family> last` (free) and explain
     that every later job of that kind will match it.
3. **Wrap-up:** what they made (files), what they spent and have left, the three things worth trying
   next (`/pga-anim <sprite> <move>` ~16-31, `/pga-batch` for sets, `/pga-history`), and that
   `/pga-start off` stops the explanations and drafts once they're comfortable.
