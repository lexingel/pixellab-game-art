# UI assets, tiles and floors


### (a) Templates
```
seamless tileable top-down ground texture, pixel art: <ground>, <small details>, <palette>, even lighting, no objects
top-down pixel art road strip that tiles horizontally: <path material> running straight from left to right through the middle, <edge material> along both edges, <palette>
dark fantasy pixel art <window panel|button|inventory slot>: <material frame> with <trim colours>, plain empty <interior|face|center> for <text|icon>
```

### (b) Parameters
- Ground: `create_image_pixflux` 64x64 or 256x256, `view: "high top-down"`, `color_image_url`
  = the region's battle background, `seed: 7`. Re-runs used `init_image_url` with
  `init_image_strength` 40–90 to calm noisy texture.
- Road strips: pixflux 128x64 `view:"high top-down"` (`init_image_strength` 60–150), or
  pro_flash 64x64 with `style_image {usage_description:"the ground this road runs across: match its palette and pixel density"}`.
- `create_tiles_pro`: `tile_type:"square_topdown"`, `tile_view:"top-down"`, `tile_size:64`,
  `outline_mode:"segmentation"`, with a numbered list of 6 variants.
- `create_ui_asset`: 192x192 / 256x256 / 384x192, `color_palette` as hex text,
  `elements:["window"|"button"]`, optional `pieces` (a hexagon polygon), `seed: 7`.
- Scene repair: `inpaint_image_pro_flash` with `context_image {usage_description:"the whole … scene this tile belongs to"}` and `bounding_box`.

### (c) Examples
```
seamless tileable top-down ground texture, pixel art: violet cobblestone street with thin gold cracks glowing between the stones, even lighting, no objects
```
```
top-down view of scorched volcanic ground, dark ash and cracked basalt with thin glowing embers in the cracks, seamless tileable ground texture, dark fantasy, evenly lit, no objects, no characters
```
```
top-down texture of a cobblestone road running horizontally from left to right across the whole image: rounded grey and tan cobbles, a thin grassy verge along the top and bottom edges, flat top-down view, pixel art texture, fills the whole canvas
```
```
1). dark cracked basalt ground 2). basalt with thin glowing ember cracks 3). grey ash ground 4). scorched rock with cinders 5). cracked obsidian ground 6). ash with small burning embers
```
```
dark fantasy pixel art button: dark violet stone plate with a bronze and ember-orange beveled rim, plain empty face for a text label
```
```
A single ornate hexagonal RPG skill-tree node badge, pixel art, dark violet-black background with a thin bright violet glowing border and gold-bronze corner accents, 2px black pixel outline, flat readable shading, empty hollow center for an icon to sit inside, isolated single shape not a UI kit sheet
```
```
the near part of a worn flagstone dungeon floor: large cracked stone slabs in warm brown-grey, continuing the corridor floor perspective, dim torchlight; no reflections, no mirrored shapes
```

### (d) Pitfalls
- A UI asset came back as a sheet of many frames. Add `isolated single shape not a UI kit sheet`
  and pass `pieces` to pin the geometry.
- Beach sand came back streaky. The re-run asked for `flat … even texture, no streaks` at
  `init_image_strength` 40.
- Inpainted floors came back with grids and boxes. Ask for `empty floor, no items, no boxes, no frames, no lines`.
