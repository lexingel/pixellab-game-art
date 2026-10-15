# Animation: padded wind-up → hit

The current way to animate attacks, skills and signature moves. It replaced prompt-only
`animate_image` (one first frame, the model invents the motion), which gave weak moves, mutating
weapons and random flashes.

## Why padding

A standing sprite is drawn tight to its silhouette. Ask for a big overhead swing on that canvas
and the model has nowhere to put the blade, so the body barely moves. Give it room:

| Who / move | Canvas | Sprite placement | Pose cost |
|---|---|---|---|
| Boss (≤ ~200 px tall) | 256×256 | feet on the bottom edge, free space on the side it faces and above | 9 |
| Hero (96×200), overhead swing, slam, upward cast | 192×256 | at (24, 56): ~72 px in front, 56 px above | 9 |
| Hero, thrust / lunge / throw / shot / bash / waist-high sweep | 192×200 | at (24, 0): ~72 px in front, none above | 6 |

Pro Flash bills by the longest side (≤200 → 6, >200 → 9), so a whole move costs 16 at 192×200
against 23 at 192×256. Pick the small canvas whenever the weapon never rises above the head.

Record the offset (sprite top-left on the padded canvas) per character and action. In the engine,
when a frame is bigger than the standing sprite, grow the sprite's rect by `offset × scale` so the
pixel scale and the feet stay exactly where they were (mirror the x offset when the sprite is
flipped). Snap back to the standing sprite when the move ends.

## Key poses (`edit_image_pro_flash`)

Template:
```
The same <who + 2-3 identifying colours/props>, <pose>, <facing>. Same size, same colours and
pixel style, feet in the same place, no background.
```
`use_color_palette_correction: true`, `no_background: true`, input = the padded upload
(`get_upload_url` + `scripts/upload.py`; uploads live 3 days). For lunges say `back foot in the same place`; for
floating/serpent bodies `base of the robes in the same place` / `coils resting in the same place`.

Pose pairs that worked:

| Move | A (wind-up) | B (hit) |
|---|---|---|
| Overhead sword | sword raised high above and behind the head, shield forward, weight on the back foot | deep lunge, sword swung down and out in front, shield still on the front arm |
| Shield bash | crouched and braced, shield pulled in to the chest | shield slammed forward, arm extended, leaning in |
| Bow shot | full draw, string past the cheek, leaning back | bow arm thrust out, drawing hand flung back open |
| Volley (skill) | on one knee drawing skyward | on one knee just after loosing high, cloak flaring |
| Staff bolt | staff swung back over the shoulder, free hand gathering light | staff thrust forward at arm's length, crystal blazing |
| Big cast (skill) | crouched, staff low in both hands | staff raised high overhead, robes whipping up |
| Flail | flail raised high behind the head, chain trailing | flail swung down in front, chain stretched |
| Prayer (skill) | head bowed, hands clasped at the chest | arms flung up and out, palms open, light at the hands |
| Twin daggers | crouched low, daggers drawn back behind the hips | far lunge, crossing double slash |
| Dagger throw | dagger drawn back behind the head, other arm pointing | throwing arm fully extended, body following through |
| Rapier sweep | blade raised high behind the shoulder, torso twisted away | wide slash across, coat flaring |
| Backhand (brute) | arm swung across the chest, fist cocked beside the far shoulder, torso rotated hard | arm whipped out across the body at shoulder height |
| Ground slam | both fists raised high | hunched, fists smashed into the ground, sparks |
| Spell from the sky | (standing sprite is fine) | both arms raised, stars/light streaking down |

**A weak wind-up is the most common failure.** "Arm drawn back" came back as an idle stance three
times; naming the end position of the fist and the torso rotation fixed it. Try two candidates
(different seed or wording) for wind-ups.

Also check: hands/props didn't swap sides, no invented props, colours held, facing kept.

## The dynamic layer (Pro-quality poses from Pro Flash)

Tested 2026-10-13 on the same warrior attack + skill: plain pose wording in Pro Flash gave stiff
poses; Pro (`edit_image`, ~10/pose) gave clearly more dynamic ones; Pro Flash **with the four
additions below** matched Pro's dynamism at 9 per pose (6 on a ≤200 px canvas, where Pro still
costs ~10). Add all four to every key pose:

1. **`dynamic exaggerated pose`** - say it outright.
2. **Stance depth** - wind-up: "deep low stance, knees bent, weight on the back foot, back arched";
   hit: "extremely deep lunge, front knee bent low, back leg stretched straight".
3. **Torso** - "torso leaning far forward" (hit) / "body twisted away" (wind-up, coil).
4. **Secondary motion** - the character's own soft parts from the look line (tabard, cape, robe,
   scarf, hair, coat tails) "flaring / swinging back / flaring forward with the motion".

Template:
```
The same <look>, <pose core>, dynamic exaggerated pose: <stance depth>, <torso>, <secondary motion>,
<facing>. Same size, same colours and pixel style, <feet|back foot> in the same place, no background.
```
Verbatim (warrior, the tested set):
```
The same young warrior with brown hair, steel breastplate, red tabard, round wooden shield and sword, in a dynamic exaggerated wind-up: sword raised high above and far behind his head, back arched, deep low stance with knees bent and weight on the back foot, shield thrust forward, red tabard and scarf swinging back with the motion, facing right. Same size, same colours and pixel style, feet in the same place, no background.
```
```
The same young warrior with brown hair, steel breastplate, red tabard, round wooden shield and sword, at the very end of a heavy downward slash, dynamic exaggerated pose: an extremely deep lunge to the right with the front knee bent low and the back leg stretched straight, torso leaning far forward, the sword in his rear hand swung down and out in front near the ground, the round shield still strapped on his front arm, red tabard and scarf flaring forward with the motion. Same size, same colours and pixel style, back foot in the same place, no background.
```
```
The same young warrior with brown hair, steel breastplate, red tabard, round wooden shield and sword, in a dynamic coiled crouch ready to explode forward: knees deeply bent, body twisted away from the right, shield pulled in tight to his chest, sword drawn back low behind him, red tabard swinging with the motion, facing right. Same size, same colours and pixel style, feet in the same place, no background.
```
```
The same young warrior with brown hair, steel breastplate, red tabard, round wooden shield and sword, exploding forward in a powerful shield bash, dynamic exaggerated pose: shield arm fully extended to the right, deep lunge with the front knee bent and the back leg straight, torso leaning far into the blow, sword held back low, red tabard and scarf flaring back with the motion. Same size, same colours and pixel style, back foot in the same place, no background.
```

**The trade-off: more dramatic poses → more flashes in the swing.** `animate_image` paints white
swooshes / colour-shifted frames on 1-3 in-betweens of a big swing. Handle them, don't prompt them away:
- Keep the swing `action` short and motion-only. **Don't add "no effects / no white lines / no motion
  trails"** - tested 2026-10-13, it made the flashes *worse* (naming them invites them).
- `qa.py <raw>/*.png --anim` → `scrub.py <raw> <flagged frames> --keep-main` (clears off-palette
  pixels, specks and anything floating away from the character) → drop frames whose colours shifted
  (the character turns lighter/oranger) or that scrub leaves broken. Keep at least 4 frames + the stance.
- One re-roll of the swing (new seed) if fewer than 4 usable frames remain.

**Tool rule:** Pro Flash + the dynamic layer is the default for key poses. Use Pro (`edit_image`,
same text, `no_background: true`, ~10/pose) for showpiece moves or when a move still flashes after
one re-roll - its in-betweens came out cleaner in the test (attack: no flashes at all).
**pixflux can't do pose edits** (img2img kept the standing pose and returned an opaque background).

## Interpolate (`animate_image`)

```
first_frame_url = <pose A download URL>
last_frame_url  = <pose B download URL>
frame_count     = 6
no_background   = true
action          = "<verb> <weapon/limb> <path> in one fast <heavy|wide> <blow>, <body lean>, <one secondary motion>"
```
Motion only - never re-describe the character. Examples:
- `brings the raised sword down and forward in one heavy fast slash, stepping into a deep lunge behind the shield`
- `uncoils and whips the cocked arm out across its body in one fast wide backhand to the left, torso turning with the swing`
- `swings the flaming greatsword across in one fast wide horizontal swing at waist height, fire trailing`
- `lifts the head from prayer and flings both arms up and outward, palms opening to the sky, robe lifting`

## Swing length, timing and the slash (current house process, 2026-10-13)

Playtest feedback on the first hero swings: *"it keeps freezing on frames… looks low fps"*. Two causes,
both fixed:

- **More frames.** Generate the swing with **`frame_count: 10`** (11 frames incl. both key poses)
  and keep every good frame. 7 frames left only 2-3 drawings for the fast part. Cost:
  192×256 → 8 (was 5 for 6 frames), 192×200 → 6 (was 4). (`animate_image` allows W×H×frames ≤ 524,288,
  so 192×256 takes up to 10 frames.)
- **Light holds, not boss holds.** Every frame ~60 ms; only a short hold on the wind-up (160 ms) and
  the hit (140 ms), 120 ms settle. The long boss holds (4× wind-up, 3.2× hit) read as freezing on
  heroes. `make_sheet.py --beat light`, `preview_gif.py` (light is its default).

**Motion only - even for a flaming or glowing weapon.** Naming the fire in the action ("flames
streaking along the blade") made the generator light the whole body: pale-pink, then white-hot
in-betweens, two re-rolls in a row (tested on a fire-sword boss, 256², 9 frames). The same move with
a motion-only action ("brings the raised greatsword down … cape swinging with the motion") kept the
body's colours and still drew the fire arc, because the key poses already show the burning blade.
A palette snap (`apply_palette.py` to the key poses' colours) doesn't fix that: the pale colours are
the fire's own. Re-roll instead.

**256×256 canvases cap at 9 frames** (`frame_count` 8: 256 × 256 × 8 = 524,288). To reach 11 on a big
canvas, **splice**: take a good 9-frame take, find its fastest two-step span (most pixels changed),
and `animate_image` between the frames on either side of it with `frame_count` 4 (4 gens at 256²):
its 3 new in-betweens replace the 1 frame in the middle → 11 frames, the extra drawings exactly where
the motion is fastest. If a segment smears (a flat washed-out arc over the body, or the body re-lit),
re-roll once, then try the next span along - the span that already carries the effect arc worked when
the one before it smeared twice (tested on a fire-sword boss: 3 moves, 5 segments, 20 gens).

**Keep a character's moves at the same frame count** (all 11). The eye compares how far the body
moves per frame, so a 7-frame move next to an 11-frame one looks choppy.

**If a 10-frame swing goes off-script**, first re-roll with the path pinned in the action (where the
weapon/shield stays and the one direction of travel: "stays low and drives the shield straight forward,
the shield kept at chest height the whole time") and a new seed - that fixed the warrior's bash, whose
first 10-frame swing stood up and lifted the shield overhead halfway (a pose in neither key pose).
Only if the re-roll wanders too, fall back to a 6-frame swing for **all** of that character's moves.

**Generator streaks vs the slash.** In the swing's fast frames the generator paints effects:
off-palette white/cyan/cream swooshes, and streaks in the character's own hue drawn in brighter,
purer colours than the sprite has (a (250,6,5) smear next to a (121,23,20) tabard). Thin streaks read
as *elemental* magic; a big crescent reads as a *weapon cut*. House look for weapon swings: **a
crescent slash in a pale "air" ramp**, behind the character:

1. Generate a 6-frame swing of the same two poses as well (5 at 192×256) - it usually draws one big
   crescent on its mid-cleave frame. `scrub.py <raw6> 3 4 --keep-main` separates it from the body.
2. `slash_layer.py extract <raw6>/3.png <raw6>/3_s.png crescent.png --to air` (and the faint
   follow-through from frame 4) - the slash alone, depth-shaded: blue rim, white core, dithered body.
3. Clean the 11-frame swing: `recolor_trail.py <raw10> 1 … 9 --hue <character hue> --to none --ref
   <standing sprite>` deletes same-hue streaks; `scrub.py <raw10> <flagged> --keep-main` removes the rest
   (scrub uses frame 0 and the last frame as the key-pose palette).
4. Lay the crescent behind the character on the mid-cleave frames:
   `slash_layer.py apply <frame> crescent.png <out> --behind` (full on the frame where the blade is
   mid-cleave, `--fade 0.3` on the next, the small follow-through arc on the one after).
   Both swings share the key poses, so the slash lands where the blade passes.

**The 6-frame swing doesn't always draw a crescent** (the rogue's and cleric's didn't; the warrior's and
the rogue's *throw* did). If none comes, recolour the weapon's own streaks into the air ramp instead
(thin cuts suit daggers) or skip the slash for blunt weapons (flails, maces, shields).
**Trails in the character's own colours** (a dark-red crescent next to a dark-red cloak):
`recolor_trail.py <raw10> 2 … 9 --hue 330,25 --to air --outside-keys --body-gap 2 --above <y>` - only
pixels outside both key poses' silhouettes, not touching the body, above the cloak/robe tails; a
`LO,HI` hue range keeps brown boots out of "red".

**Ground every frame.** Generated poses are often drawn up to ~20 px above the standing sprite's feet
line (kneels, lunges, crouches), so the character hops in-game. Check and fix before export:
`ground_snap.py <sprite> <pad_x,pad_y> <frames…> --check`, then without `--check` (grounded moves only;
not for jumps or flyers). If a lunge's back leg runs off the canvas edge, re-pad wider with more room
behind (208×252 at 40,52 still fits 10 frames: 208×252×10 ≤ 524,288).

Alternatives: `recolor_trail.py … --to air|fire|arcane|holy|shadow` keeps the generator's own streaks but
recolours them (fine for spells, reads elemental); `recolor_trail.py <raw6> 3 4 --from-scrub --to air`
puts a scrubbed crescent back recoloured on the 6-frame swing itself.

Cost of a melee move this way: poses 9 + 9, 10-frame swing 8, 6-frame swing for the crescent 5
= **31** at 192×256 (22 at 192×200). Non-weapon moves (casts, prayers, shots) skip step 1.

## Shots (guns, bows, wands): no crescent (tested 2026-10-13 on a rifle knight)

A shot reaches forward only and has no blade:
- **Canvas 192×200** (room in front, poses 6 each); a levelled long gun needs ~70 px in front of a
  96 px hero, which the default pad (sprite at x=24) gives.
- **Pose A = the aim**, not a coil: "rifle shouldered, stock pressed to the shoulder, barrel levelled
  to the right, braced stance with the front knee bent, head down along the barrel". Dynamic layer:
  stance depth, a slight forward lean, cape/tabard hanging still.
- **Pose B = the recoil**: "the shot's recoil: shoulder and rifle jolted back, barrel kicked up,
  torso rocked back onto the braced back foot, tabard flaring forward with the motion".
- **Action**: "fires: the rifle kicks back and up from the recoil, the body rocks back on the back foot".
  A big recoil from a kneel needs the path pinned - "stays low on bent legs, the front foot slides
  forward, he never falls over" - or the in-betweens throw him flat on his back (tested).
- If a frame's flash is painted *into* the barrel (scrub deletes half the gun), reuse the previous
  frame in its slot: a short hold on the shot reads as weight and keeps the frame count.
- **No crescent swing, no `slash_layer`.** The generator paints its own muzzle flash on the first 1-3
  frames, in front of the barrel and with a white core the colour test keeps (armour has white):
  `scrub.py <raw> 1 2 --keep-main --clear-right <barrel tip x>` (`--clear-left` for left-facing shooters).
  The barrel kicks back during the recoil, so use each frame's own tip if the flash sits closer.
- **Paint the flash in `vfx_workbench`** (free): `muzzle_flash` part (core) + a `smoke_puff` at ~0.6 size
  from 0.15, scaled 1.5, fit_canvas, 7 frames @ 12 fps (~51×40) for a regular shot; a big shot =
  `muzzle_flash` ×2.6 + `fire_blast` ×0.8 30 px ahead + `sparks_shower` (~86×66, 12 frames). The bullet's
  hit on the target is a separate strike. Preview it on the frames:
  `preview_gif.py out.gif <sprite> <frames…> --offset X,Y --vfx <export>.png --vfx-at <tip x>,<tip y> --vfx-on 1`.
- **Energy weapons (lasers, plasma, magic bolts): name the flash colour** - "the laser gun fires a cyan
  flash" - or the generator paints an orange-yellow gunpowder flash (tested on a laser pistol). Better still,
  scrub it and bake your own `vfx_workbench` flash.
- **Don't colour-scrub a frame where the flash lights the sprite.** The flash also brightens nearby hair and
  skin; `scrub.py`'s colour test then strips them too (a pink-haired shooter came out with grey hair).
  Use `--clear-right`/`--clear-left` at the barrel tip only, or reuse the previous frame.
- **A first take that drops the gun to the hip mid-shot** (a pose in neither key pose) - re-roll once with
  the path pinned: "her arms stay extended the whole time and the gun never drops below shoulder height".
- **The damage moment is the first motion frame**, not the frame before last: `make_sheet.py --hit 1`.
- Cost at 192×200: 6 + 6 + 6 = **18**.

## 8 directions (top-down): rotate, animate, finish (tested 2026-10-14 on a laser-pistol shot)

For a top-down / 3/4 game you need the move in 8 facings. Two routes:

| Route | How | Cost per direction (96×200 sprite) | Aim |
|---|---|---|---|
| **Cheap** | `create_character` v3 rotates the sprite, `animate_character` v3 animates each direction from text | ~7 | loose - the generator picks the arm angle |
| **Exact** | per direction: aim + recoil (or wind-up + hit) key poses on that rotation, then animate between them | ~18 | precise |

Generate **5 directions** (S, SE, E, NE, N) and **mirror** E→W, SE→SW, NE→NW: ~40% cheaper. The weapon
switches hands on the mirrored side - fine for most games; generate all 8 if not.

1. **Front-facing reference first** (Pro Flash edit, ~6): "the same <look>, now standing straight-on facing
   the viewer, front view, symmetric relaxed stance, <weapon> held at her side. Same size, same colours and
   pixel style, feet in the same place", `use_color_palette_correction: true`. **Whatever the reference faces
   becomes south** - a side-view reference mislabels all 8 directions.
2. **Rotate**: `create_character(mode="v3", reference_image_url=<front>, n_directions=8, view="low top-down")`
   (3 for a 96×200 sprite; ~4 min). `get_character` → rotation URLs. **Check all 8 on one sheet before
   animating** (hair, back details, boots, weapon in hand) - a drifted direction is cheapest to fix here.
3. **Animate**: `animate_character(mode="v3", action_description=…, frame_count=8, directions=[…])`.
   - **Cost is billed on the generated canvas, not the sprite**: a 96×200 sprite animates on ~224×224 →
     ceil(224·224·8/65,536) = **7 per direction**. Use 64-128 px characters for 8-direction games (1-3).
   - **Never write "forward"**: the model reads it as screen-right in every direction (tested: S, SE, NE and N
     all fired to the right; only E was right). Make one call per direction and name the aim on screen:

     | Direction | Words that worked |
     |---|---|
     | south | "keeps facing the viewer and raises the <gun> straight toward the viewer, arm extended toward the bottom of the screen" |
     | north | "keeps her back to the viewer and raises the <gun> straight ahead away from the viewer toward the top of the screen" |
     | south-east | "keeps facing down-right and raises the <gun> toward the bottom-right of the screen, arm extended diagonally down-right" |
     | north-east | "keeps her back half-turned and raises the <gun> toward the top-right of the screen, arm extended diagonally up-right away from the viewer" |
     | east | "raises the <gun> with her arm extended straight to the right" |

     Even then text-only aim is loose: south came out right, north aimed up-right, the diagonals aimed fairly
     flat. For exact angles use the key-pose route.
4. **Finish (free, local)**:
   - `scripts/find_muzzle.py <dir>` - the generator paints its own (wrong-coloured) flash on the shot, right at
     the muzzle: it reports the shot frame and the muzzle point. Check it on the frame (it misses when the flash
     covers the body or overlaps the gun).
   - Write a small spec per direction (shot frame, muzzle, angle, boxes to clear, frames to replace) and run
     `scripts/dir8_finish.py spec.json`: clears the generator's flashes, removes detached specks, bakes your
     `vfx_workbench` flash rotated to each direction (anchor on the muzzle), pads every direction to one frame
     count (holding the last pose - the flash needs room when the shot is the last frame), mirrors the west side.
   - A flash painted over the body: replace that frame with the previous one (a hold on the shot reads as
     weight) - don't erase it.
   - `make_sheet.py <out> <frames…> --beat light --hit <shot frame>` per direction; one GIF with all 8 in a
     compass grid to compare them.
5. **Cost of the tested run**: front 6 + rotations 3 + 5 directions × 7 + 4 re-rolled × 7 = **72**.

## Pick frames

Download indices 0-10 (`scripts/fetch.py <job> <dir> --frames 11`), then `scripts/qa.py <dir>/*.png --anim`
finds flash frames automatically. 0 = A, 10 = B, 1-9 generated.

- **Keep every good frame** (11). Clean rather than drop.
- Drop only a smeared or blob frame that can't be cleaned (a solid coloured smear over the body
  happens about 1 in 10); the engine should accept 5-12.
- The generator likes to paint flashes, starbursts and swoosh lines on the fastest in-between.
  - Off-palette (cyan, yellow on a purple rogue): `scripts/scrub.py <dir> 2 3 4` clears every pixel
    whose colour isn't near a colour of pose A or B.
  - In a colour the character already has (white highlights): can't be scrubbed - drop the frame.
  The effect belongs to the VFX layer anyway.

## Timing (the house rhythm)

Hold the wind-up, swing fast, hold the hit, settle - in beat units × a base step (~0.05-0.07 s in a
fight, ~0.1 s in a showcase GIF):

| Frames shown (incl. standing sprite) | Beats |
|---|---|
| 5 (boss legacy) | 0.6, 3.0, 0.6, 3.2, 0.8 |
| n > 5 (padded, bosses) | 0.6 (stand), **4.0 (wind-up)**, 0.8 … 0.8, **3.2 (hit = frame before last)**, 1.4 (settle) |
| heroes (current, `--beat light`) | 60 ms each, **160 ms wind-up**, **140 ms hit**, 120 ms settle |

Fire the impact (damage numbers, hit flash, VFX, projectile release) on the hit frame
(index n-2), not after the animation - except shots, which fire on the first motion frame (`--hit 1`).

## Other actions

- **Idle loop**: `first_frame_url = last_frame_url = sprite`, 4 frames, *"<who> idle breathing loop:
  shoulders and chest rise slightly then settle back, a gentle 1 to 2 pixel up and down body bob, same
  pose, same facing, keeps holding the same <weapon>, body motion only, no effects, no glow, no new
  objects, same colours"*.
- **Death**: edit a "defeated" pose as the last frame, 4 frames, *"is struck down: staggers, knees
  buckle, drops to one knee and slumps forward…, body motion only, no effects…"*.
- **Hurt / hit reaction** (tested 2026-10-15, body only, no effects): only the **peak pose** needs
  painting (the standing sprite is the other key). Pad the standing sprite with room behind (96x200 -> 144x200,
  x=40 for a right-facing hero), make **one** peak pose with `edit_image_pro_flash` (dynamic layer: *"thrown
  backward, head snapped back, shoulders rocked back, arms lifted a little from the sides, open empty hands,
  tabard flaring, feet planted in the same place, nothing in the air around him"*; two seeds, pick one), then two 6-frame
  `animate_image` clips: stand -> peak ("jolts backward ... in one fast snap") and peak -> stand ("catches
  himself and straightens back up"), each with `first_frame_url` + `last_frame_url`, ~3 gens each, 13 frames,
  drop the duplicate peak. Hold ~60 ms/frame, 200 ms on the peak, 300 ms standing. ~33 gens with the base.
  Pitfalls: (1) the generator painted yellow swipe arcs on 2 of the 7 hit-clip frames even though the pose
  was clean - `qa.py --anim` flags them, `scrub.py --keep-main` fixes one, drop a frame that comes out with
  holes; (2) the peak pose and recovery frames came out ~15-20% **brighter** than the standing sprite - a
  visible colour shift mid-move: run `scripts/colormatch.py <standing> <frames>` before the sheet/GIF.
  Old prompt-only version (no key poses):
  *"recoiling backward from a heavy hit, flinching and staggering, then steadying, body motion only,
  colours unchanged, no light effects"*.
- **Kick / any 3-part move from a smooth cartoon reference** (tested 2026-10-15, 19 frames, ~55 gens): a
  high-res non-pixel reference -> `image_to_pixelart` (1 gen, 128x128, `faithful: true`, strength 150 beat
  250 and non-faithful for colour) -> flood-fill the grey background from the corners (it comes back opaque)
  -> pad (192x144) -> two poses (chamber, extended kick; 2 seeds for the extension) -> THREE clips: stand ->
  chamber (6), chamber -> kick, kick -> stand (6). The 10-frame chamber -> kick clip retracted the leg and
  kicked twice (non-monotonic) and painted a white swipe at the foot; the **6-frame clip with the path pinned**
  (*"the raised knee stays up, then the lower leg unfolds and snaps out; the foot never goes back to the
  ground"*) was clean. Shorter clips for a two-pose snap, pin "never goes back". Then `ground_snap.py`
  (needs `x,y` pad offset as one argument) and `colormatch.py`.
- **Walk**: prompt-only, 8 frames, `last_frame = first frame` for a clean loop, often from a 64 px copy.
- Props mutate between frames → add *"keeps holding the same <prop> in the same hand, unchanged in
  shape and size"*. Brightness flicker on glows → *"keep exactly the same colour and brightness in
  every frame"* + seed 7.
