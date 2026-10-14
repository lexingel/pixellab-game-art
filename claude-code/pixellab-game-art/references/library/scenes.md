# Screen / hub backdrops and story pictures


### (a) Templates
Hub interior (a room with clickable props):
```
<room> at night, wide view: <prop 1 on the left>, <prop 2 in the centre>, <prop 3 on the right>,
<light source>, <mood words>, empty of people
```
Story banner (wide 288x120):
```
Dark fantasy pixel art story banner, wide scene: <who> <doing what> <where>, <2–3 details>;
<warm light> against <cold shadow>, <palette>
```
or the event-card variant:
```
wide pixel art scene banner: <scene>, muted dark palette, painterly pixel art, side view
```
Cinematic intro panel:
```
<scene>, <foreground subject>, <background landmark>, cinematic wide shot
```

### (b) Parameters
- `create_image_pro` is the main tool. Sizes: 288x120 story banners (73 calls), 624x392 or
  640x400 hub rooms (78), 688x384 / 672x336 cinematic panels, 640x272 title, 688x256
  top-down region maps. Settings: `style_image_url`, `style_copy: ["outline","detail","shading"]`,
  often `reference_images` with usage "scene layout, colors and lighting only", `seed: 7`.
- `create_image_pixflux`: 320x180 or 320x200 for cheap drafts, `color_image_base64/url` for the
  palette. 128x80 for small vignettes.
- To get an empty version of a scene, add `reference_images` = the full scene and ask for "the same
  scene with every … removed".

### (c) Examples
```
a stone portal hall interior: a large swirling violet portal in a stone archway in the centre, a smaller blue magic doorway on the left, a chained iron-barred gate with rubble on the right, wall torches, worn flagstone floor, no people
```
```
a guild master's war room: a round wooden table covered by a large parchment map, open books, a candle holder, a pot of gold coins, a glowing crystal and brass gears, helmets on shelves behind, flagstone floor, warm candle light, no people
```
```
a medieval monster hunter's study at night, wide view: specimen jars with strange creatures on shelves, sketches of monsters pinned to the walls, a mounted beast skull, a dissection table with tools, a lantern, a large tome open on a lectern, eerie but warm, empty of people
```
```
Dark fantasy pixel art story banner, wide scene: a wounded knight sits against a rock in a dark crystal cavern binding a bloody bandage round his arm, a cracked shield and broken sword beside him, a companion holding a torch over him; violet arcane glow, deep red and cold blue shadows
```
```
wide pixel art scene banner: masked bandits with torches and knives creeping out of a dark treeline toward a fantasy camp at night, an iron-bound strongbox in the foreground, muted dark palette, painterly pixel art, side view
```
```
dark fantasy pixel art illustration, wide cinematic scene, no text: deep beneath an upside-down city, an old knight in chains pressing his shoulder against a huge glowing door to hold it shut, light leaking through its cracks, frayed ropes hanging around him, violet and gold light
```
```
the same night scene with every building, ruin, tent, archway and structure removed: only the starry indigo sky, distant dark hills, a few trees at the sides, a low grassy hill in the back centre and a flat dirt courtyard ground across the bottom, empty, side view, no people
```
```
top-down overhead view of a dark fantasy region map of a drowned marshland: murky marsh pools, reeds, sunken drowned ruins and bell towers half under black water, mist, glowing violet magic cracks, seen directly from above like a game world map, muted dark colours, low contrast, no text, no characters, no UI
```

### (d) Pitfalls
- **Text creeps in.** One early pixflux camp prompt was rewritten from "no UI elements" to
  `No text, no letters, no numbers, no watermark, no signature, no UI elements anywhere in the image.`
  A later rewrite dropped banners and flags altogether (`no banners or flags … no signs with writing`)
  because banners kept carrying fake letters. Inpaint was used for leftover signs, with
  "blank cloth with no numbers, no letters, no symbols".
- **Buildings merging in a panorama.** The camp scene went through about 6 rewrites, from
  "arranged in a rough circle" to "exactly six large, clearly separated, distinct buildings in a
  single row, generous gaps of open ground between each one" with "Building 1 (far left): …". The
  final approach was to give up on one image: generate an empty backdrop and each building as its
  own sprite (§3).
- **Dark scenes read as mud.** An empty hall had to be re-edited to
  `same abandoned great hall, but lit: pale moonlight falls through a tall window and a few candles glow on the long table, so the table, chairs, pillars and banners read clearly; keep the composition`.
- **Room framing:** `straight-on front view of a room filling the whole frame edge to edge, no borders`
  fixed vignettes that came back with frames.
