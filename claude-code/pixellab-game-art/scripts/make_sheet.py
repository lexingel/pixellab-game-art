"""make_sheet.py - pack animation frames into an engine-ready spritesheet.

  python make_sheet.py <out_base> <frame1.png> <frame2.png> ... [options]

Writes <out_base>.png (frames in a row, or --cols N per row) and <out_base>.json in the
Aseprite "array" format (frames[].frame {x,y,w,h} + duration ms; meta.size/image) that Unity,
Godot (Aseprite importers) and most engines read, plus "meta.pixellab" with the extra data an
engine needs for the house-style swings: pad offset, facing, hit frame. --godot also writes
<out_base>.tres (a SpriteFrames resource with per-frame durations).

Timing (pick one):
  --durations 600,4000,800,...   milliseconds per frame
  --beat light                   the house rhythm for heroes: 60 ms a frame, 160 ms wind-up, 140 ms hit, 120 ms settle
  --beat swing --step 60         the heavier boss rhythm (long holds on wind-up and hit) × step ms
  --fps 12                       even timing
Extras: --pad X,Y (where the standing sprite's top-left sits on these frames) --facing right|left
        --hit N (the damage frame; default the frame before last, shots use 1)
"""
import argparse
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def _expand(paths):
    """cmd/PowerShell pass *.png literally: expand * and ? here (natural order, so 2.png comes before 10.png)."""
    import glob
    import re
    out = []
    for p in paths:
        hits = glob.glob(p) if ('*' in p or '?' in p) else []
        out += sorted(hits, key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]) or [p]
    return out

import json
import os
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('out')
ap.add_argument('frames', nargs='+')
ap.add_argument('--cols', type=int, default=0)
ap.add_argument('--durations')
ap.add_argument('--beat', choices=['swing', 'light'])
ap.add_argument('--step', type=float, default=60)
ap.add_argument('--fps', type=float, default=12)
ap.add_argument('--pad')
ap.add_argument('--facing', choices=['left', 'right'])
ap.add_argument('--godot', action='store_true')
ap.add_argument('--hit', type=int)
a = ap.parse_args()
a.frames = _expand(a.frames)

ims = [Image.open(f).convert('RGBA') for f in a.frames]
w = max(i.width for i in ims)
h = max(i.height for i in ims)
n = len(ims)
cols = a.cols or n
rows = (n + cols - 1) // cols
if a.durations:
    dur = [int(float(x)) for x in a.durations.split(',')]
    assert len(dur) == n, 'need one duration per frame'
elif a.beat == 'light':
    dur = [60] * n
    dur[0], dur[n - 2], dur[n - 1] = 160, 140, 120
elif a.beat == 'swing':
    b = [0.8] * n
    b[0], b[min(1, n - 1)], b[max(n - 2, 0)], b[n - 1] = 0.6, 4.0, 3.2, 1.4
    dur = [int(x * a.step) for x in b]
else:
    dur = [int(1000 / a.fps)] * n
sheet = Image.new('RGBA', (w * cols, h * rows))
frames = []
for k, im in enumerate(ims):
    x, y = (k % cols) * w, (k // cols) * h
    sheet.alpha_composite(im, (x + (w - im.width) // 2, y + h - im.height))   # bottom-centred: feet stay put
    frames.append({'filename': os.path.basename(a.frames[k]), 'frame': {'x': x, 'y': y, 'w': w, 'h': h},
                   'rotated': False, 'trimmed': False, 'spriteSourceSize': {'x': 0, 'y': 0, 'w': w, 'h': h},
                   'sourceSize': {'w': w, 'h': h}, 'duration': dur[k]})
png = a.out + '.png'
sheet.save(png)
extra = {'frame_count': n, 'hit_frame': max(n - 2, 0) if a.hit is None else a.hit}
if a.pad:
    px, py = (int(v) for v in a.pad.split(','))
    extra['pad_offset'] = {'x': px, 'y': py}
if a.facing:
    extra['facing'] = a.facing
meta = {'app': 'pixellab-game-art make_sheet.py', 'image': os.path.basename(png), 'format': 'RGBA8888',
        'size': {'w': sheet.width, 'h': sheet.height}, 'scale': '1', 'pixellab': extra}
json.dump({'frames': frames, 'meta': meta}, open(a.out + '.json', 'w'), indent=1)
print(png, a.out + '.json', '%d frames %dx%d' % (n, w, h))

if a.godot:
    base = min(dur)
    lines = ['[gd_resource type="SpriteFrames" load_steps=%d format=3]' % (n + 2), '',
             '[ext_resource type="Texture2D" path="res://%s" id="1"]' % os.path.basename(png).replace('\\', '/'), '']
    for k, f in enumerate(frames):
        r = f['frame']
        lines += ['[sub_resource type="AtlasTexture" id="f%d"]' % k, 'atlas = ExtResource("1")',
                  'region = Rect2(%d, %d, %d, %d)' % (r['x'], r['y'], r['w'], r['h']), '']
    anim = ', '.join('{"duration": %.3f, "texture": SubResource("f%d")}' % (d / base, k) for k, d in enumerate(dur))
    name = os.path.basename(a.out)
    lines += ['[resource]', 'animations = [{"frames": [%s], "loop": false, "name": &"%s", "speed": %.3f}]'
              % (anim, name, 1000.0 / base)]
    open(a.out + '.tres', 'w').write('\n'.join(lines) + '\n')
    print(a.out + '.tres', '(put the .png next to it in your Godot project; fix the res:// path if needed)')
