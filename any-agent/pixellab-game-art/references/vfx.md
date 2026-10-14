# VFX: painted, outlined, timed

## The target look (reference spec)

The style was set from one benchmark creature attack that read far better than ours. Its quality
came from the effect and the timing, **not** from body animation. Measured:

| Property | Value |
|---|---|
| Length | 14 frames, ~4.4 s, loops |
| Colours | ~56 per frame - the effect uses the attacker's own colour family (4-5 tones + dark outline + one highlight), nothing new |
| Body motion | almost none: a head tilt and a lunge of a few pixels |
| Effect size | the peak cloud is ~1.5-2× the creature's body |
| Shading | puffs lit from the top-left, each with a dark outline and a darker underside; a dark contact shadow where the cloud touches the ground |

Frame timing (ms), which is the real lesson:

| Phase | Frames | Durations | What happens |
|---|---|---|---|
| Anticipation | 3 | 250, 750, **1500** | the attacker tenses; nothing leaves yet |
| Launch | 3 | 90, 90, 100 | streams of small puffs shoot out |
| Peak | 1 | **200** | the big cloud lands, fully formed |
| Break-up | 6 | 110, 90, 80, 80, 80, 90 | the cloud breaks into smaller puffs, then specks |
| Recovery | 1 | **850** | back to rest |

So: **long hold before, very fast travel, a hold on the impact, fast dissolve, a rest.** A game
fight compresses this (whole move ~1-1.5 s) but keeps the shape.

Per-frame durations used in-game at 12 fps (in frames; 1 = 83 ms):
- Strike (12 frames): `0.8, 0.6, 0.6, 0.8, 1.0, 1.0, 2.2, 1.1, 1.0, 0.9, 0.9, 1.0`
- Wave (14): `1.2, 0.9, 0.9, 1.0, 1.0, 1.0, 1.1, 2.4, 1.2, 1.0, 0.95, 0.95, 0.95, 1.0`
- Eruption (12): `0.9, 0.9, 1.0, 1.2, 2.0, 1.2, 1.0, 1.0, 0.9, 0.9, 0.9, 1.0`

`vfx_workbench` exports frames; the durations live in your engine's clip table next to each sheet.

## Fixed recipe

```json
"tones": 5, "detail": 0.1, "shading": "lit", "outline": {"mode": "dark"},
"fps": 12, "loop": false
```
- `detail 0.3` looked busy; 0.1 reads clean at play size.
- One `main` ramp of 6 stops, near-black → highlight, in the attacker's colours. Optional accent
  ramp (`gold`, `rune`) for sparks/stars.

Ramps that worked:
```
fire     #2a0a08 #6e1409 #b3260e #e8561a #f8a531 #ffe08a
lich     #0a140e #1f3a26 #2f5f3a #4f8f45 #a8c860 #f0e8a0
violet   #12081f #2d0f4a #5a1f86 #8f45c4 #c48af0 #f0d8ff
stone    #141418 #2e2e36 #55575f #8a8d92 #c2c5c4 #ecece6   (+ rune #3a2a00 #9a7a00 #e6c21a #fff27a)
tide     #0b1d24 #1c4350 #35617b #4c9fb8 #90d4ec #e6f8ff
cosmic   #180e20 #381165 #56367c #8a5cc0 #c8a0f0 #f4e8ff   (+ gold #4a3410 #b29352 #debd77 #fff2c4)
crimson  #1e0710 #52012f #a3014b #d8306a #f080a0 #ffe0ea
spectre  #07120e #223e3b #416e60 #4fbf6a #9cf07a #e6ffd0
```

## Workflow

```
vfx_workbench(["start", "--fps", "12"], notes="who, which move, the look")
vfx_workbench([<id>, "render", "{\"recipe\": {...}}"])                       # from a template
vfx_workbench([<id>, "render", "{\"patch\": [...], \"frames\": [2,5,8,10]}"])  # tweak, check key frames
vfx_workbench([<id>, "export", "--name", "<Who> <Move>"])
```
Then download the sheet + JSON the export points to. A new character from an existing template is
one `render {"patch":[{"op":"set","path":"ramps.main","value":[...]}]}` and an export.

## Templates (`assets/vfx_templates/`)

**Strike - one target** (112×112, 12 frames, origin [56,62], drawn over the victim)
- `arc` slash (`profile:"slash"`, radius ~30, thickness 4-7, life [0, 0.4], front). Thrust: `points`
  + `corners:"smooth"`. Claws: `claws:3, spacing:7`. Attacker strikes left → `mirror:"x"`.
- `puffs` billow: `mode:"burst", radius 24, count 6, throw 0.55, rise 0.3-0.6, thin 0.45, lump 0.4,
  billow 1.0, highlight 0.65, life [0.16, 1.0]`, back.
- `particles`: `dot` embers, `sparkle` stars, `droplet` (gravity 70-110), `chunk` (floor 30,
  bounce 0.3), `streak` sparks; count 12-16, `outline: true`, front.
- Optional flash: `rays` (count 8, length 10→30, life [0, 0.28]) and a squashed `ring` for slams.

**Wave - across the whole party** (340×130, 14 frames, origin [40,72], built pointing right,
`mirror:"x"` for a left-facing attacker)
- wide `arc` swing (radius 34, sweep 210, thickness 9, life [0, 0.3])
- **three overlapping cartoon `shape` streams** (`fill:"cartoon"`, width keys 9→15→18, `drift 40`)
  with staggered life [0.12,0.78] / [0.19,0.84] / [0.26,0.88] and `dissolve` [[0,0],[0.6,0],[1,1]] -
  one long stream looks like a pipe; three give a rolling front
- a mid cloud (puffs radius ~22 at x 190) and a big end cloud (radius 40, count 10, life [0.36, 1.0])
- embers along the path (`line`, count ~34, life [0.55, 1.0])
- Scale it in-engine so its end cloud lands on the farthest target; record its start/end points.
- (The template file is the first render; the three streams replaced its single `stream` layer.)

**Eruption - under each target** (100×136, 12 frames, origin [50,124], `camera.tilt 0.15`)
- ground `ring` (`plane:"ground"`, radius 6→34), upright `flame` (width 26, height 6→70→56→10,
  3 tongues), billow puffs rising (rise 0.9), rising embers.
- A falling-star variant: a `paths.fall` path (from above, ease in) + a `ribbon` trail + a `glow` head.

## Pitfalls

- **Shapes must read as the thing**: a "star" made of a 4-point square read as a box → use `rays`;
  a "falling star" built as a rising pillar read wrong → path + ribbon + glow from above.
- **Too small at play size**: build the strike at 112 px and draw it at ~60 px per game unit; a
  wave should span the whole party.
- The library's ready-made `add_part` pieces are a quick start, not the house look - rebuild from
  raw layers (arc / puffs / shape / particles / rays / ring / flame).
- Check key frames (`"frames": [2,5,8,10]`) on every patch before exporting.
- The attacker's swing frames should replace a generic hit burst, not stack on top of it.
