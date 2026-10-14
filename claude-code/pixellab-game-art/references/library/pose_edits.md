# Pose edits (`edit_image_pro_flash`)


### CURRENT house style: A/B key poses for each move
**Add the dynamic layer** (`references/animation.md` → "The dynamic layer"): `dynamic exaggerated pose`, stance depth, torso lean/twist, secondary motion of the character's soft parts. It brings Pro Flash poses to Pro's level (tested 2026-10-13).

Template (one call for A, one for B):
```
The same <short look: who + 2–3 identifying colours/props>, <pose>. Same size, same colours and
pixel style, feet in the same place, no background.
```
- A = wind-up/coil: `raising … high above his head`, `drawing … far back over her shoulder`,
  `winding up …`, `coiled to …`.
- B = follow-through/hit: `at the end of …`, `… thrust fully extended`, `smashing … down into the ground`.
- For lunges, write `back foot in the same place`. For floating or serpent bodies, write
  `base of the robes in the same place` / `coils resting in the same place`.
- Parameters: `no_background: true`, `use_color_palette_correction: true`. `method: "text"` on
  some calls. Input is the padded idle sprite (256x256 bosses, 192x256 heroes). `seed` only on
  retries (3 or 7).
- Bosses attack toward the LEFT and heroes toward the RIGHT. Say it in every pose.

Verbatim (latest calls):
```
The same horned demon knight in the same golden spiked armour, now raising his flaming greatsword high above his head with both hands, the blade angled back over his shoulder, ready to cleave forward to the right. Same size, same colours and pixel style, feet planted in the same place, no background.
```
```
The same horned demon knight in the same golden spiked armour, at the end of a huge cleaving swing: the flaming greatsword swung far forward and down to the right, blade extended out in front of him near the ground, body leaning forward into the follow-through, flames trailing off the blade. Same size, same colours and pixel style, feet in the same place, no background.
```
```
The same ram-skulled olive serpent with glowing orange runes, rearing its head up high and pulled back, jaws open, coiled to strike toward the left. Same size, same colours and pixel style, coils resting in the same place, no background.
```
```
The same teal water spirit queen, thrusting her trident far forward to the left with both arms extended, body leaning into the thrust, water spraying off the prongs. Same size, same colours and pixel style, base of the robes in the same place, no background.
```
```
The same captain in a crimson coat and tricorn hat, in a deep fencing lunge to the right, rapier thrust fully extended in front of him, coat tails flying. Same size, same colours and pixel style, back foot in the same place, no background.
```
```
The same young warrior with brown hair, steel breastplate, red tabard, round wooden shield and sword, slamming the shield forward to the right in a powerful shield bash, arm fully extended, leaning into it, sword held back. Same size, same colours and pixel style, back foot in the same place, no background.
```
```
The same mage in a blue robe and pointed hat with a crystal-topped staff, winding up a spell: staff swung back over the shoulder, free hand pulled back gathering blue light, body coiled away from the right. Same size, same colours and pixel style, feet in the same place, no background.
```
```
The same hooded rogue in dark purple leathers with two daggers, just after hurling a dagger to the right: throwing arm fully extended forward, body following through, cloak swinging. Same size, same colours and pixel style, back foot in the same place, no background.
```

Pitfall: a wind-up that reads as idle. The cosmic brute backhand was rewritten three times, from
"one huge arm drawn back across its chest" to "fist pulled back behind its right hip" to "left arm
swung back across its chest so the fist is cocked high beside its right shoulder, torso rotated hard
to the right". Name where the fist or blade ends up and how far the torso turns.

### Other edit recipes (still in use)
- **Surgical fix:** `Change only the <part>: … Keep the face, hood, outfit, palette, size and stance exactly the same.`
  ```
  Remove the dark greatsword that hangs unheld from his belt down between his legs to his feet; in its place draw the blue tabard cloth and his armoured legs normally. Keep everything else exactly the same: bald bearded head, bronze armour, the chains in both hands, pose, colours, pixel style.
  ```
- **Rarity tiers** (`no_background: true`):
  `Same <item>, same shape, size and position, upgraded to a <rare|epic> version: <rare = polished blue-steel + silver + blue sapphire | epic = dark steel/black + ornate gold filigree + glowing violet gem, faint violet glow>. Transparent background.`
  ```
  Same round shield, same shape, size and position, upgraded to an epic version: dark wood with an ornate gold filigree rim, the central boss becomes gold with a glowing violet gem and a faint violet glow. Transparent background.
  ```
- **Building upgrade** (`seed` 1 or 3): `grow this <tier 1> into <tier 2>: …, same pixel art style and palette`.
  ```
  upgrade this smithy into a grand stone forge hall: solid grey cut-stone walls instead of timber, a taller steep slate roof, TWO tall stone chimneys both smoking, a big arched furnace mouth blazing bright orange in the front wall, two red cloth banners with an anvil emblem hanging on the walls, iron-bound door with a lantern, weapon rack and anvil out front, night, warm orange forge light spilling out, same pixel art style and palette
  ```
- **Style transfer onto an icon set:** `method: "reference"` with
  `reference_image {url:<image>, usage_description:"match this icon's art style: thick dark outline, saturated colours, strong highlights and shading"}`.
  ```
  a glossy red heart with a white highlight and dark red shading, thick dark outline, game icon (no symbol inside)
  ```
- **Fit to canvas:** `zoom out: draw this same barracks house a little smaller so the entire building … fits inside the canvas with about 4 pixels of empty transparent margin …; keep the same design, colours and bottom position`.
- **Masked repair** (`inpaint_image_pro_flash` / `inpaint_image` with a mask box): describe only
  what belongs inside the mask, and add what must not appear:
  ```
  empty dark starry night sky with distant mountain silhouette, seamlessly continuing the background exactly, absolutely no objects, no signs, no banners, no posts, no cross
  ```

### Legacy / superseded
- **Pose-only hero edits** before the A/B pipeline (16 identical reruns of one "now aiming" edit
  were made to get candidates):
  ```
  Same character in a full archery draw aiming to the viewer's right: the bow arm stretched straight out to the right holding the longbow vertical, the other hand pulling the bowstring back to her cheek with an arrow nocked and aimed right. The bow is smaller in view and stays fully inside the image with empty margin above and to the right. Legs, boots and stance planted as before. Keep the face, hood, outfit, palette and size exactly the same.
  ```
- **Two heroes per image for defeated poses** (batching to save credits). This needed
  `each stays strictly inside its own half … do not swap or merge the characters`, and the
  characters still swapped. Do one character per call.
- **The bow-limb saga.** About 12 edits and inpaints all said the same thing: "lower limb going
  straight down beside her leg on the outside … never crossing or passing through the leg". Lesson:
  prevent it in the generation prompt (§4), because edits fix it slowly.
