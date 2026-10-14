# Items and icons


### (a) Templates
Skill icon (pro, 32x32):
```
pixel art game skill icon, 32x32, <one concrete object/symbol>, <ability name>, bold dark outline,
<2–3 colour family per class>, centred, readable at small size
```
Relic or item (pro 40x40 / pixflux 64x64):
```
fantasy relic item icon: <object>, <material + glow colour>, single centered object, dark outline
game icon of <object>, dark fantasy RPG <skill|relic item|item|legendary item> icon, single object centred, bold dark outline, rich shading, muted colours
```
Status or intent icon (pro 32x32):
```
<status effect|enemy intent|boss mechanic|elite affix> icon: <symbol>, <meaning>. Single bold symbol, centered, thick dark outline, high contrast
```
Tiny UI glyph (pro 16x16):
```
tiny 16x16 pixel art UI icon, <object>, bold dark outline, simple shading, readable at small size, centred, transparent background
```
Heraldry (pro 40x40, greyscale so it can be tinted in-engine):
```
pixel art heraldic emblem, <charge>, white and light grey only, greyscale, solid black outline, bold silhouette, centred, no colour
```

### (b) Parameters
- `create_image_pro`: 32x32 (94 calls), 40x40 (74), 16x16 (30), 48x48 (map markers).
  Uses `style_image_url` (one anchor icon per set), `style_copy: ["outline","detail","shading"]`
  for skill sets, and `no_background: true`.
- `create_image_pixflux`: 64x64 (about 167 icons), `seed: 7` then 11, `no_background: true`.
  Cheap first pass.
- `create_1_direction_object` with `item_descriptions: [...]`, `size: 40` for a whole sheet at once.
- One colour family per class keeps sets coherent: warrior "steel grey and red", ranger "forest green
  and brown", mage "blue and violet", cleric "gold and white", rogue "dark grey black and purple".

### (c) Examples
```
pixel art game skill icon, 32x32, a round magic mirror with a shimmering blue and violet surface reflecting a lightning bolt back, mirror ward, bold dark outline, blue and violet colours, centred, readable at small size
```
```
game skill icon: a heavy executioner's axe standing diagonally, broad crescent steel blade with a dark red edge, long dark wooden haft wrapped in leather, one strong silhouette, thick dark outline, readable at small size
```
```
fantasy relic item icon: a small open holy book with a silver clasp, its pages burning with pale blue-white fire, single centered object, dark outline
```
```
enemy intent icon: a huge war hammer smashing down with a red impact burst, heavy blow warning. Single bold symbol, centered, thick dark outline, high contrast
```
```
tiny 16x16 pixel art UI icon, a gold double chevron pointing up, two stacked upward arrowheads, level up symbol, bold dark outline, simple shading, readable at small size, centred, transparent background
```
```
game icon of a sword with a small round brass clock face set in its crossguard and a glowing pale blue blade, diagonal, dark fantasy RPG legendary item icon, single object centred, bold dark outline, rich shading, muted colours
```
```
small game map location sprite, three-quarter top-down view: a dark ruined fortress gate with a huge horned skull above the doorway and red light glowing inside, the boss lair, dark fantasy, clear silhouette, dark outline
```
```
pixel art heraldic emblem, coiled serpent snake in an S shape with head raised, white and light grey only, greyscale, solid black outline, bold silhouette, centred, no colour
```

### (d) Pitfalls
- **Boxed icons.** Icons came back on a square plate. The fix was
  `isolated object only, no frame, no square, no backdrop` (also `no frame, no shield, no badge, no border`).
- **Too small in the canvas.** Add `filling the frame`, plus `the whole idol and cloud fully inside the frame with a small margin` when parts got cropped.
- **Ambiguous silhouettes.** `clearly a scythe not a pickaxe`, `clearly shorter than a sword`,
  and naming a direction (`pointing diagonally up-right`, `the arrow coming in from the lower left`).
- **Heraldry drift.** The horse and dragon kept turning into lions. Edits added
  `greyscale like the original, NOT a lion` and `no mane`. For wide charges (wreath, wings) give
  the layout: `left wing on the far left and right wing on the far right … large empty gap in the middle`.
- **Rarity tiers** are made by editing the base icon, not regenerating it (§8).

### (d) Lessons from real jobs
- Measured: Pro at 32x32 = 10 gens for 64 candidates, 40x40 = 15 for 36. One call per icon is enough; pick from the sheet.
- `style_copy: ["outline","detail","shading"]` (no `color_palette`) with ONE existing icon of the set keeps the outline weight and shading but lets the new icon have its own colours — the style icon's subject can be anything (a boot styled a gold hourglass fine).
- Don't ship a copy of another icon as a placeholder (same picture for two meanings confuses players, and art tests that forbid duplicate icons will catch it later). A 32px Pro call costs less than the cleanup.
- A status/buff icon and the skill that applies it need different subjects (skill: winged hourglass; status chip: lightning bolt with speed lines), or the chip reads as "the skill" instead of "the effect".
- Picking at 32px: dark iron/black objects vanish on dark UI panels — prefer the steel/light-grey candidates; symmetric, upright silhouettes read better than tilted ones; skip candidates with stray sparkle pixels in the corners.
- Make a contact sheet (all candidates at 3x on the UI's background colour, numbered) and look before choosing.
