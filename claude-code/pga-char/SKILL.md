---
name: pga-char
description: "Make a pixel-art character sprite (hero, monster, boss, NPC, portrait) with PixelLab in the pixellab-game-art house style - improves the description first, then generates, QA-checks and logs. Use when the user types /pga-char."
argument-hint: "<character idea> [hero|monster|boss|npc] [--ref sprite.png] [--n 3] [--draft] [--dry]"
disable-model-invocation: true
model: sonnet
allowed-tools: mcp__pixellab__* Bash(python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(python3 ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*) Bash(py ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/*)
---

The main skill lives next to this one: `R` = `${CLAUDE_SKILL_DIR}/../pixellab-game-art`. Run its scripts exactly as
`python ${CLAUDE_SKILL_DIR}/../pixellab-game-art/scripts/<name>.py …` (pre-approved). Follow the shared loop in
`R/references/prompt_improver.md` (setup check, `pixellab.json` profile, flags `--dry` `--draft`
`--ref` `--n`, QA before looking, logging). Read only the files named below - not the whole skill.

# /pga-char

User's request: **$ARGUMENTS**

Read: `R/references/library/house_rules.md`, `R/references/library/characters.md`.

| Kind | Tool | Size (profile `sizes`) | Template |
|---|---|---|---|
| Hero / party member / portrait | `create_image_pro_flash` + `style_image` (profile anchor `heroes`) | 96×200 | `full body portrait of a <man\|woman> <role> hero standing, facing <heroes facing>, <base look>, <gear tier>, <accent colour>. <one-line flavour>. <look>, clear role colours, whole body fits inside the canvas with a small margin` |
| Monster / elite / boss | `create_image_pro_flash` + `style_image` (anchor `monsters`, or the old sprite when redrawing) with `style_options` outline/detail/shading (+ color_palette when redrawing); "facing left" in the text; profile seed. Cost 6. Many candidates to pick from: `create_image_pro` at ≤170 px (4 candidates, 10) - it ignores facing, mirror it. Cheap draft or forced-palette recolour only: `create_image_pixflux` (1, `direction`, `color_image_url`) | 200×200 | `<look> <monster\|elite monster\|boss monster>, full body, three-quarter view facing <foes facing>: <body plan>, <material>, <weapon/pose>, <glow colour>, heavy dark shading` |
| Detailed redraw of an existing sprite | `create_image_pro` + `reference_images` (old sprite) + `style_copy` | sprite size | the same character, "crisp detailed pixel art, clean dark outline" |

Cost: Pro Flash 6 (96×200 or 200×200) · Pro 10 · pixflux 1 (drafts). `--n 3` = three seeds submitted together.

Tested 2026-10-13 on the same humanoid foe prompt with an existing foe as style ref: **Pro Flash** (6) was the most detailed, followed the brief fully, faced left as asked and matched the anchor's outline and shading; **Pro** (10) was close in quality but ignores facing (came out facing right - mirror it); **pixflux** (1) was flat and its forced palette changed the colours; **v3** `create_character` (6 for 8 directions) gave a thin side profile, humanoid-only - only for games that need 8 facings.

Improve: body plan + material (a creature, not a concept); role colours for party members
(warrior steel + deep red, ranger forest green + brown, mage deep blue, cleric white + gold, rogue
dark violet) unless the profile says otherwise; gear tier word; pitfall negatives - only ones that
don't contradict the request (ranged with no firearm asked for → `medieval, no guns`; a named
firearm → keep it, era word + two-handed hold inside the canvas, `R/references/library/characters.md` §e; stone → `no metal, no armour plates`; birds → `not a dragon`; bows → `bow held
upright at the side, lower limb outside the leg`; robes → `two human legs hidden by the robe`);
always `whole body fits inside the canvas with a small margin`, `no_background: true`, profile seed.

QA: `qa.py <files> --anchor <anchor>`; look at the half-size sheet. Report as in §8.
