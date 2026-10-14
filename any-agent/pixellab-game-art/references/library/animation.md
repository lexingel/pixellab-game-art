# Animation actions (`animate_image`)


### CURRENT house style (latest boss work, 2026-10-13): two key poses, then interpolate

Pipeline for each attack or skill move:
1. Pad the idle sprite onto a fixed canvas: **256x256 for bosses**, **192x256 for heroes**. The
   sprite is bottom-anchored so the feet line never moves.
2. Make two key poses with `edit_image_pro_flash` (§8): **A = wind-up/coil** and
   **B = follow-through/hit**.
3. `animate_image` with `first_frame_url = A`, `last_frame_url = B`, **`frame_count: 10`** (11 frames; see
   ../animation.md "Swing length, timing and the slash"), `no_background: true`. 256² boss canvases
   take at most 8 frames (pixel cap); the bosses shipped at 6 with the heavy boss beat. The action is a single short verb phrase that describes the motion
   between the two poses. Do not re-describe the character.

Action template:
```
<brings / swings / thrusts / lunges / slams> <the weapon or limb> <path of motion> in one fast <heavy|wide> <blow|arc|thrust>, <body lean>, <one secondary motion: cloak/flames/robes>
```

Verbatim (latest calls):
```
swings the flaming greatsword down from high overhead in one fast wide forward arc, leaning into the cleave, flames streaking along the blade
```
```
brings both raised stone fists crashing down into the ground in one heavy slam
```
```
the serpent strikes forward and down fast with jaws wide open, neck uncoiling
```
```
explodes forward into a deep fencing lunge, rapier thrusting out fast
```
```
sweeps the flaming greatsword across in one fast wide horizontal swing at waist height, fire trailing
```
```
raises the trident high as a great wave of water rises and curls in front of her
```
```
uncoils and whips the cocked arm out across its body in one fast wide backhand to the left, torso turning with the swing
```
```
raises both arms to the sky as gold stars streak down and the crescent moon flares
```

Idle loop (current): `first_frame_url = last_frame_url = idle sprite`, `frame_count: 4`,
`no_background: true`.
```
hero idle breathing loop: shoulders and chest rise slightly then settle back, a gentle 1 to 2 pixel up and down body bob, same pose, same facing, keeps holding the same sword and shield, body motion only, no effects, no glow, no new objects, same colours
```
```
skeletal lich in green robes idle breathing loop: shoulders rise slightly then settle back, a gentle 1 to 2 pixel up and down body bob, robe hem sways slightly, same pose, same facing, keeps holding the same staff, body motion only, no effects, no glow, no new objects, same colours
```
Death (current): `last_frame_url` = an edited "defeated" pose, 4 frames.
```
hero is struck down: staggers, knees buckle, drops to one knee and slumps forward to the ground, still holding the same daggers, body motion only, no effects, no glow, no new objects, same colours
```

Why it replaced prompt-only animation: with only a first frame the model invents the pose, so
weapons change shape, glows and flashes appear, and the move is weak. Locking both ends with edited
key poses gives a big readable wind-up-to-hit; 10 in-between frames keep the fast part smooth.

### Parameters across all 2,100 calls
- `frame_count`: 4 (1,500), 8 (558; walks and "big dramatic" moves), 6 (42; current keyframe moves
  and the VFX one-shots).
- `last_frame_url` set in 592 calls. In 369 of them it equals the first frame, giving a seamless loop
  for idle and walk.
- `no_background: true` in 1,201 calls. `seed` was rarely set (7 when it was).
- `animate_object` (78 calls, 4 frames) for early `create_1_direction_object` monsters, for example
  `lunging forward and slashing with long claws` and `rattling backward from a hit, then recovering`.

### Pitfalls (retries of the same move)
- **Props mutate between frames.** The fix was a clause naming the prop and its constancy:
  `keeps holding the same crystal staff in the same hand, unchanged in shape and size`,
  `The lantern stays hanging at the top end of the staff in every frame`,
  `any arrow is only on the string in the hand, never floating beside the body`.
- **The model adds VFX you don't want** (beams, rings, white flashes, rectangles). On idle, walk,
  hurt and death loops add `body motion only, no effects, no glow, no new objects, same colours`, or
  target the specific artefact: `no beams, no rectangles`, `no white flash, no outlines`. **Not on
  padded key-pose swings** (attacks, skills): there it makes the flashes worse - clean them with
  `scrub.py` instead ([../animation.md](../animation.md) → "Swing length, timing and the slash").
  Draw the VFX separately (§9).
- **Brightness flicker** on glowing staff heads. The fix was `exact same brightness`,
  `keep exactly the same colour and brightness in every frame`, plus `seed: 7`.
- **Facing drift.** Add `stays facing left` / `stays turned toward the right` / `stays facing the viewer`.
- **Weak motion.** The prefix `big dramatic attack: … exaggerated motion … then recovering` helped
  on 4–8 frame prompt-only moves. Keyframes made it unnecessary.

### Legacy / superseded (still useful for walks)
Walk cycles are still prompt-only. They used 8 frames, often `last_frame = first_frame`, and
small 64px copies for the hamlet:
```
walking forward to the right, one full looping walk cycle, side view, body motion only, colours unchanged, no effects
```
```
walking forward to the left, slow heavy lumbering walk cycle, keep every colour exactly the same
```
```
creeping forward to the left, low crouched stalking walk cycle
```
Superseded 4-frame prompt-only hurt and attack moves (kept as a reference for vocabulary):
```
recoiling backward from a heavy hit, flinching and staggering, then steadying, body motion only, colours unchanged, no light effects
```
```
fire-winged wyvern gets hit: recoils backward, head snaps back, wings flinch and fold in a little, staggers, then recovers. Same orange-red wings, same horn and head shape, tail flame attached to the tail tip. Clear body motion, no effects, no new objects
```
```
big dramatic move: dropping to one knee and drawing the bow to full, then loosing a powerful shot to the right, exaggerated motion, body motion only, no effects, then rising
```
