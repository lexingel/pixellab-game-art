# Buildings and hamlet props


### (a) Template
```
<building type> <material/size>: <roof>, <door/windows>, <2–3 identifying props>,
single building, side view, night lighting, no people
```
Upgrade tiers ask for the same building again ("the same training yard, upgraded: …"), or edit the
previous tier (§8 Other edits).

### (b) Parameters
- `create_image_pro`, `no_background: true`, `seed: 11` (21/22 for yard tiers),
  `style_image_url` = the approved backdrop, `reference_images` = sibling buildings,
  `style_copy: ["outline","detail","shading"]`. Sizes: 192x144 (landmark hall), 96x80–96x104
  (houses), 64x112 / 80x112 (towers), 160x64 (yards), 64x64 (campfire).
- `create_image_pixflux` drafts: `view: "side"` plus `color_image_base64`, 64x64 / 48x64 / 96x80.
  Later used `init_image_url` with `init_image_strength` 60 (tier 1) and 120–150 (tier 2), `seed: 3`.
- `create_map_object` (32x32 / 32x48, `view: "side"`) for small hamlet props.
- `create_image_pro_flash` with `style_image {source_image_id, usage_description:"same tower family: match palette, outline, shading and stone base"}` for a three-tier tower family at 96x96.

### (c) Examples
```
a great stone guild hall fully restored from a ruin: rebuilt grey stone walls, a new dark slate roof, warm lit arched windows, two red guild banners with a white sigil, a heavy wooden door flanked by torches, single building, side view, night lighting, no people
```
```
a healer's cottage of stone and timber with a white cloth awning marked with a red cross, bundles of drying herbs, a small herb garden, a lantern, single building, side view, night lighting, no people
```
```
an open training yard: a flat patch of packed dirt with a wooden rail fence along the back and a torch, three training stations evenly spaced in a row: a straw training dummy, a round archery target on a stand, and a weapon rack with swords and spears, side view, night lighting, no people
```
```
a small medieval music hall building for a village: timber-framed stone hall with a steep shingled roof, a round rose window glowing warm, open double doors with candlelight inside, a hanging wooden sign with a painted lyre, a little stage awning on the side with a lute leaning on a barrel; seen from the front at a slight angle, standing on a patch of grass and dirt
```
```
small open-air blacksmith forge at night, side-front view: a stone hearth with a short brick chimney and a bright orange ember glow, an iron anvil on a stump, a quench barrel of water, a slanted wooden lean-to plank roof on two posts, tongs and hammer, warm orange firelight on the stones, dark blue night shadows, game building sprite
```
```
front view pixel art, flat side elevation, not isometric: two-storey timber trading house with colorful awnings, a hanging gold coin sign and crates outside, medieval fantasy, night
```
```
a great blazing fire cauldron atop a tall stone tower, fire pouring over its rim, glowing runes on the stones, fantasy game defense tower at its strongest, three-quarter top-down view
```

### (d) Pitfalls
- **Wrong projection.** Pixflux with `view:"side"` still drew isometric buildings. The fix was
  the prefix `front view pixel art, flat side elevation, not isometric: … sitting on a flat ground line`.
- **Clipped edges.** Buildings touching the canvas edge needed
  `the whole building fully visible and centred with empty margin on all sides`, an edit
  (`zoom out very slightly: redraw … about 6 percent smaller … 2 pixels of empty transparent margin`),
  or inpaint to finish a roof or base ("the tower ends cleanly at its base; transparent background").
- **Tiers that look unrelated.** Generate tier 2 from tier 1 (`init_image` strength about 120, or an
  edit "grow this … into …") so the silhouette carries over.
- **Isolated means isolated.** Add `nothing behind it` / `isolated on transparent background` or
  you get ground and sky.
