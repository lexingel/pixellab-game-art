# Battle backgrounds


### (a) Template
```
dark fantasy pixel art battle background, side view, wide landscape, no characters,
open flat <ground type> along the bottom third for fighters: <scene>, <2–4 landmark details>,
palette of <3–4 colours>
```
Alternative (pro, with a reference scene):
```
<scene>, <details>, side view battle background with open ground in the foreground for
characters to stand on, no characters
```

### (b) Parameters
- `create_image_pro`: 640x256 (32 calls), 640x288, 640x248, or 320x200 for the region sets.
  `seed: 7`. `style_image_url` = an approved background.
  `style_copy: ["outline","detail","shading"]`.
  `reference_images: [{url:<image>, usage:"scene layout, colors and lighting only"}]`.
- `create_image_pixflux`: 320x200, `seed: 7`, `color_image_url` = the matching pro
  background, so the cheaper model keeps the same palette.
- Always `no_background: false`.

### (c) Examples
```
dark fantasy pixel art battle background, side view, wide landscape, no characters, open flat ground along the bottom third for fighters: a beach of glittering sea-glass sand at night, the tide rising upward into the sky in slow glowing arcs of water, broken stone pillars standing in the surf, stars hanging low over the sea, palette of muted sea-glass cyan, lilac, pearl white and deep teal shadows
```
```
dark fantasy pixel art battle background, side view, wide landscape, no characters, open flat marble floor along the bottom third for fighters: a grand upside-down palace hall, gold chandeliers rising up from the floor, violet stained glass windows, a staircase climbing up into darkness, palette of deep violet, dusky purple and warm gold
```
```
dark fantasy dungeon corridor battle background, side view, rough stone brick walls with burning iron wall torches, worn stone stairs rising in the center, flagstone floor in the foreground for characters to stand on, deep shadows, no characters
```
```
a volcanic cavern with lava falls and glowing lava pools, dark cracked rock, a scorched rock floor, side view battle background with open ground in the foreground for characters to stand on, no characters
```
```
a dark green swamp with dead twisted trees, a murky stream, glowing will-o-wisps, ruined stone walls behind, side view battle background with open ground in the foreground for characters to stand on, no characters
```
```
dark fantasy pixel art battle background, side view, wide landscape, no characters, a broad flat stone ledge along the bottom third for fighters: the edge of an open chasm beneath a floating city, frayed giant ropes dangling down into darkness, broken bridges, faint gold lamplight far below, palette of deep violet, dusky purple and warm gold
```

### (d) Pitfalls
- Without "open flat ground along the bottom third", fighters end up standing on clutter. Name the
  ground type (street, marble floor, cave floor, stone ledge).
- A region set is generated as a trio (exterior, interior, edge or chasm) that shares one palette
  sentence, so the three read as one place.
- Seams and mirrored artefacts in wide images were fixed with `inpaint_image_pro_flash` plus a
  `context_image` and `bounding_box` (see §6). Ask for `no reflections, no mirrored shapes`.
