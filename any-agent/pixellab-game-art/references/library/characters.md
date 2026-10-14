# Characters (heroes, monsters, bosses, champions, portraits)

> **Current pick for monsters (2026-10-13 test):** Tested 2026-10-13 on the same humanoid foe prompt with an existing foe as style ref: **Pro Flash** (6) was the most detailed, followed the brief fully, faced left as asked and matched the anchor's outline and shading; **Pro** (10) was close in quality but ignores facing (came out facing right - mirror it); **pixflux** (1) was flat and its forced palette changed the colours; **v3** `create_character` (6 for 8 directions) gave a thin side profile, humanoid-only - only for games that need 8 facings. The pixflux monster recipe below is the older way; keep it for drafts.


### (a) Templates
Hero class/subclass portrait (pro_flash, 96x200, generated per data row):
```
full body portrait of a <man|woman> <subclass name> hero standing, <class base look>,
<gear tier>, <accent colour>. <one-line flavour>. Dark fantasy pixel art, muted shading, clear role colours
```
- class base looks: `a warrior with a weapon and armour in steel armour with a deep red tabard` ·
  `a ranger with a bow in a forest green cloak and brown leathers` ·
  `a mage with a focus or staff in deep blue robes with a soft magical glow` ·
  `a cleric with a holy symbol in white and gold vestments` ·
  `a rogue with daggers in dark violet hooded leathers`
- gear tiers: worn mismatched recruit, simple practical, seasoned well-used, solid veteran, fine
  distinctive, elite ornate, legendary gear with a faint aura
- accents: warm ember red and orange, pale icy blue, faintly glowing blue-violet runes, deep shadowy
  violet and black, earthy greens and leather

Monster (pixflux, 200x200, facing left):
```
dark gritty fantasy pixel art <monster|elite monster|boss monster>, full body, three-quarter view
facing left: <body plan>, <material>, <weapon/pose>, <glow colour>, heavy dark shading
```

### (b) Parameters
- Heroes: `create_image_pro_flash` 96x200 (151 calls), also 76–92 wide x 200. `seed: 7`.
  `style_image: {source_image_id, usage_description: "match this portrait's pixel art style, proportions, outline and shading"}`
  or `"Match this sprite's outline weight, pixel detail, shading and palette exactly"`.
  `no_background: true`.
- Monsters: `create_image_pixflux` 200x200 (121 calls), `direction: "west"`, `seed: 7`
  (21 for bosses), `color_image_url` = a region sprite or background for the palette,
  `no_background: true`.
- Detailed redraws: `create_image_pro` 96x200 with `reference_images` (the old sprite) and
  `style_copy`.
- Early monsters: `create_1_direction_object` with `view: "sidescroller"`, `size: 160`,
  `style_images` = a hero sprite. This was superseded by pixflux and pro.

### (c) Examples
```
full body portrait of a man berserker hero standing, a warrior with a weapon and armour in steel armour with a deep red tabard, seasoned, well-used gear, warm ember red and orange accents. Considers armor a personal insult. Dark fantasy pixel art, muted shading, clear role colours
```
```
Full-body pixel art portrait of a young recruit ranger standing, facing right, forest green hooded cloak over brown leathers, a simple longbow and a quiver, plain gear, alert, dark fantasy, muted colours, dark outline, light from above
```
```
full body portrait of a charming mercenary captain standing, trimmed dark beard, long dark coat, a badge shaped like a crown on his chest, a rapier at his hip, a smile that doesn't reach his eyes, dark fantasy pixel art
```
```
dark fantasy pixel art monster, full body, standing, three-quarter view facing left: a drowned bell-ringer, a pale ghost in waterlogged monk robes, seaweed hair, ringing a heavy rusted bronze bell, cold blue glow, detailed shading, dark outline
```
```
dark gritty fantasy pixel art monster, full body, three-quarter view facing left: city watchman in tarnished gold and violet armour holding a lantern on a pole, his cape floating upward as if gravity were reversed, heavy dark shading
```
```
dark gritty fantasy pixel art boss monster, full body, three-quarter view facing left: a towering figure made of old parchment pages and flowing green ink in the shape of a robed sorceress, glowing green lines of handwritten script running across its whole body, a crown of ash, long quill-like fingers, torn pages drifting from its hem, heavy dark shading
```
```
full-body standing hulking bald brawler, front view turned slightly right, huge bare muscular tanned chest and arms, blue cloth mask over the lower face, chain bandolier across the chest, big golden belt buckle, brown leather loincloth and kilt, two huge blue steel gauntlets covered in golden spikes on both fists held low at his sides, dark blue trousers with golden knee guards, heavy brown leather boots, wide planted stance, whole body fits inside the canvas with a small margin. Crisp detailed pixel art, clean dark outline, smooth realistic shading, readable shapes
```

### (d) Pitfalls (from re-prompts of the same subject)
- **A swamp sniper** came back with a gun. The rewrite added `medieval`, "primitive wooden crossbow
  made of bone and reeds", and `no guns`.
- **A slag golem** came back as armoured metal. The rewrite was "rough natural black volcanic boulders
  … organic rough rock, no metal, no armor plates".
- **A hawk-like fire bird** came back as a dragon. The rewrite was "a fierce hawk-like bird of prey … not a dragon".
- **A cultist oracle and a rope-wrapped reaver** came out non-human or abstract. Name the body plan: `full body human cultist …
  two human legs hidden by the robe`, `wrapped from head to toe in thick frayed ropes like a mummy`.
- **Concept overload.** "colossal humanoid shape made of a shattered night sky" was rewritten three
  times into a concrete body ("hunched giant whose whole body is a window into a starry night sky …
  a crescent moon in its chest"). Describe a creature, not an idea.
- **Cropped limbs and weapons.** Add `whole body fits inside the canvas with a small margin`
  (canvas 96x200 became 92x170 on retry).
- **Bows cross the legs.** On front-facing heroes the lower bow limb kept crossing the thighs. This
  took a dozen inpaints and edits (§8), so describe the bow as held "upright and vertical at the
  side, lower limb outside the leg" in the first prompt.
- **Facing.** Heroes say `facing right`. Monsters say `three-quarter view facing left` plus
  `direction: "west"`. Bosses that came out facing the viewer were later posed via edits.

### (e) Firearms and other named weapons (tested 2026-10-13: 3 of 3 seeds right first time)
The sniper pitfall above is for an unasked-for gun. When the user names a firearm, keep it:
- **Drop `medieval` and `no guns`** - both pull it back to a crossbow.
- **Give it an era that fits the look**, keeping the user's word: dark fantasy → "long black-powder
  rifle" / "flintlock musket" / "wheellock pistol"; a modern or sci-fi profile keeps "rifle".
- **Hold it so it fits a 96 px-wide hero**: "held diagonally across the chest in both <gauntleted>
  hands, barrel pointing up" or "resting upright against the shoulder", plus "whole rifle inside the
  canvas". Aiming level runs off the canvas - the aim belongs to the animation's pose A.
- **Name the rest of the kit** so the gun doesn't turn it into a soldier's uniform: "heavy full plate
  armour, closed visored helm, plate gauntlets, tabard".
- **Negatives against swaps**: `no sword, no bow, no crossbow` (+ `no shield` if it has none).

```
full body portrait of a man knight hero standing, facing right, heavy full plate armour with a closed visored helm, plate gauntlets and a deep red tabard, long black-powder rifle held diagonally across his chest in both gauntleted hands, barrel pointing up, whole rifle inside the canvas. Dark fantasy pixel art, muted shading, steel and deep red, whole body fits inside the canvas with a small margin, no sword, no bow, no crossbow
```
