# Task pga-normal

Run when the user asks for `pga-normal` (with or without a slash) or describes this job in plain words.
Input: <sprite.png | frame files | anim.gif | character:<id>:<dir>[:<anim>]> [--engine godot|unity|phaser|unreal] [--dry]

Read only the files named below plus `<skill>/references/prompt_improver.md` (the shared loop: setup check, profile, show every call with its parameters, never ask permission, never repeat a call, results table).

User's request: **(the user's request)**

`create_normal_map(image=…, convention=…)` - 0.5 generation, 15-70 s, any colours, each frame
8-512 px, up to 32 frames. `convention`: `directx` for Unreal, `opengl` for everything else
(profile `engine`, or `--engine`).

1. **Input.** A PixelLab id passes straight in (`character:<id>:<dir>[:<anim>]`, `job:<id>`).
   A local sprite: `get_upload_url` → `upload.py` → `upload:<id>`. Animation frames:
   `python <skill>/scripts/normal_map.py gif <out>/up.gif <frames…>` then upload the GIF - a PNG strip is
   read as ONE image (refused over 1024 px).
2. **Split clips at big pose changes.** One call plans the shapes on the first frame and carries
   them to the rest: idles and walks are fine whole; an attack whose pose changes a lot gets
   horizontal bands on the frames far from frame 1 (tested: an 11-frame lunge banded its last 4
   frames; the same 4 frames sent alone came out clean). Cut the clip where the silhouette changes
   (wind-up / strike / recover) and send one GIF per segment, all in the same turn.
3. **Download:** `fetch.py <job> <out>/<name>_n.png --log …` (a clip comes back as a strip), then
   `python <skill>/scripts/normal_map.py split <strip_n.png> <the segment's frames…>` → `<frame>_n.png`
   next to each frame.
4. **QA:** `python <skill>/scripts/normal_map.py preview <out>/<name>_lit.gif <sprite or strip> <map> [--frames N]`
   and look at `<name>_lit_lights.png` once (rows = light from left, top, right): every part should
   get brighter on the lit side. Bands or flat patches → re-run that segment with fewer frames.
5. **Engine** (tell the user the steps for theirs):
   - Godot 4: a `CanvasTexture` with the sprite as Diffuse and the map as Normal (per frame in
     SpriteFrames for animations) + a `PointLight2D` / `DirectionalLight2D`.
   - Unity (URP 2D): Sprite Editor → Secondary Textures → `_NormalMap` = the map; Sprite-Lit material + 2D lights.
   - Phaser 3: `this.load.image('k', ['k.png', 'k_n.png'])`, `sprite.setPipeline('Light2D')`, `this.lights.enable()`.
   - Unreal (Paper2D): `directx` maps, a lit sprite material.

`--dry` stops after the plan (segments, calls, cost). Report as in §8.
