# VFX (`vfx_workbench`)


### CURRENT house style (boss strikes, sweeps, eruptions; latest calls)
Painted, volumetric, outlined effects: shaded puff clouds with a dark outline. The timing runs
launch, billow, dissipate into embers or droplets, using staggered layer `life` windows. Frame
durations themselves are not set in these argv.

Global recipe settings (identical on every current effect):
```
"tones": 5, "detail": 0.1, "shading": "lit", "outline": {"mode": "dark"}, "fps": 12, "loop": false
```
Each effect has one 6-stop `main` ramp from near-black to highlight, plus an optional accent ramp
(gold or rune). The template is re-skinned per boss by patching only `ramps.main`.

Command sequence:
```
start --fps 12          (notes: who, what move, the look you want)
<id> render {"recipe": {...full recipe...}}          (first render)
<id> render {"patch": [...set/replace_layer ops...], "frames": [2,5,8]}   (check key frames)
<id> export --name <Boss> <Move>
```
A new variant from an existing template is a single `render {"patch":[{"op":"set","path":"ramps.main","value":[...]}]}` followed by `export`.

**Template A – single-target strike** (112x112, 12 frames, origin [56,62], played over the victim):
- `arc` layer (`profile:"slash"`, radius about 30, thickness 4–7, life [0,0.4], z front). For a
  thrust use `points` and `corners:"smooth"`. For claws use `claws:3, spacing:7`. Add `mirror:"x"`
  if the attacker strikes left.
- `puffs` billow: `mode:"burst", radius 24, count 6, throw 0.55, rise 0.3–0.6, thin 0.45, lump 0.4, billow 1.0, highlight 0.65, life [0.16,1.0], z back`.
- `particles`: embers (`dot`), shards or stars (`sparkle`), droplets (`droplet`, gravity 70–110),
  chunks (`chunk`, `floor:30, bounce:0.3`), or sparks (`streak`). Count 12–16, life [0.2–0.4, 1.0],
  `outline:true`, z front.
- An optional flash: `rays` (count 8, length 10→30, life [0,0.28]) or a 4-point `star`, plus a
  `ring` slam ring (`squash 0.35`).

Verbatim (lich boss strike):
```
render {"recipe": {"canvas": {"w": 112, "h": 112}, "frames": 12, "fps": 12, "loop": false, "origin": [56, 62], "ramps": {"main": ["#0a140e", "#1f3a26", "#2f5f3a", "#4f8f45", "#a8c860", "#f0e8a0"]}, "outline": {"mode": "dark"}, "tones": 5, "detail": 0.1, "shading": "lit", "layers": [{"id": "swing", "type": "arc", "profile": "slash", "x": 52, "y": 52, "radius": 30, "start": -130, "sweep": 180, "thickness": 7, "life": [0.0, 0.42], "z": "front"}, {"id": "billow", "type": "puffs", "mode": "burst", "x": 56, "y": 62, "radius": 24, "count": 6, "throw": 0.55, "rise": 0.5, "thin": 0.45, "lump": 0.4, "billow": 1.0, "highlight": 0.65, "life": [0.18, 1.0], "z": "back"}, {"id": "motes", "type": "particles", "mode": "rise", "x": 56, "y": 66, "radius": 18, "count": 12, "speed": 40, "size": [2, 3], "shape": "dot", "lifespan": 0.7, "fade_out": 0.4, "life": [0.35, 1.0], "z": "front", "outline": true}]}}
```
Verbatim (stone golem slam layers): flash `rays` with a `rune` ramp, slam `ring`, dust `puffs`, and
`chunk` particles:
```
{"id": "chunks", "type": "particles", "mode": "burst", "x": 56, "y": 62, "count": 10, "speed": 62, "direction": -90, "spread": 170, "gravity": 90, "size": [3, 5], "shrink": 0, "shape": "chunk", "lifespan": 0.8, "floor": 30, "bounce": 0.3, "life": [0.14, 0.92], "z": "front", "outline": true}
```

**Template B – party sweep / wave** (340–360 x 130–140, 14 frames, origin [40,72], `mirror:"x"`,
built pointing right):
- a wide `arc` swing (radius 34, sweep 210, thickness 9, life [0,0.3])
- three chained cartoon `shape` streams: `closed:false, smooth:1, fill:"cartoon", width keys 9→15→18, spacing 0.9, drift 40`, with staggered life [0.12,0.78] / [0.19,0.84] / [0.26,0.88], `dissolve` keys [[0,0],[0.6,0],[1,1]]
- a `midcloud` puffs at x 190 (radius 22) and an end `cloud` puffs at x 290 (radius 40, count 10, life [0.36,1.0])
- `embers` particles along a `line: 180` (count 34, gravity 40, life [0.55,1.0])

Variants were made by patch only: droplets (`shape:"droplet", gravity:70`), gold sparkles
(`ramp:"gold", shape:"sparkle", blink:2`), crimson streaks, or `remove_layer swing` + a `poof`
surge puff for a tide.

**Template C – eruption under each hero** (100x136, 12 frames, origin [50,124], `camera.tilt 0.15`):
a ground `ring` (`plane:"ground"`, radius 6→34), an upright `flame` (width 26, height keys
6→70→56→10, tongues 3), billow puffs rising (rise 0.9), and rising embers. The gold variant adds a
falling star built from a `paths.fall` path plus a `ribbon` trail and a `glow` head.

Pitfalls:
- `detail: 0.3` looked busy. It was lowered to 0.1 on the first boss and kept there.
- The first parts-based attempt (`add_part swing_slash + fire_blast`) was removed, and the effect
  was rebuilt from raw layers. Parts are a quick start, not the house look.
- A single long stream looked like a pipe. Splitting it into three overlapping streams with
  staggered `life` gives a rolling front.
- Check the key frames with `"frames": [2,5,8,10]` on every patch before exporting.

### Legacy / superseded
- **Status loops and signature clips on a hero sprite** (`start --sprite <image> --fps 12`, then
  `add_part {"name":"stun_stars"|"poison_bubbles"|"bubble_shield"|"curse_skulls"|"on_fire"|"buff_arrows", "size":2.2, "colour":[5 hex]}`,
  then hand-tuned `render` patches with custom pixel `particles`, then `export --name <Game> <name> --game-pack`).
  Still useful for loops anchored to a fighter. Example part call:
  ```
  add_part {"parts": [{"name": "slam_dust", "around": "subject", "anchor": "feet", "size": 1.6, "core": true, "start": 0.0, "end": 1.0}, {"name": "shockwave_ring", "around": "subject", "anchor": "feet", "size": 1.3, "start": 0.0, "end": 0.5}, {"name": "debris_burst", "around": "subject", "anchor": "feet", "size": 1.0, "start": 0.05, "end": 0.8}]}
  ```
  Notes on redo calls name the failure modes: too small at play size, sat too low at the feet, dead
  first frames, burst off-centre, flat 3-tone fills. Fix them with canvas plus `subject {align:"feet"}`,
  with a bounce in the y keys, and with bevelled outlined shapes.
- **AI-drawn VFX frames:** a pixflux 128x128 still (`pixel art game spell effect, a burst of sharp pale blue ice shards exploding outward from a centre, frost mist, muted colours, no character, centred`)
  animated with `animate_image` at 6 frames (`the ice shards burst outward, spread wider, then shatter into small fragments and fade away to nothing`).
  This was replaced by the workbench, which gives exact pixels and timing. The negatives needed
  then were `no weapon, no character, no arrow, no torch, no object`.
