"""dir8_finish.py <spec.json>: finish a multi-direction shot/attack - clean the generator's flashes, bake your
own vfx_workbench effect at the muzzle (rotated to each direction), pad every direction to one frame count,
mirror the other side, write <out>/<direction>/0..N.png.

spec.json:
{
  "out": "final",                       # output folder (relative to the spec)
  "total": 12,                          # every direction padded to this many frames (holds the last frame)
  "speck": 40,                          # remove detached pixel blobs smaller than this (before the flash goes on)
  "flash": {"sheet": "vfx/flash.png", "json": "vfx/flash.json", "anchor": [3, 14]},
                                        # a vfx_workbench export (sheet + JSON); anchor = the effect's origin, it points right
  "dirs": {
    "east":  {"src": "anim/east",  "shot": 6, "muzzle": [186, 67], "angle": 0,
              "clear": {"6": [[187, 38, 224, 96]]}},           # boxes to erase on a frame (the generator's own flash)
    "south": {"src": "anim/south", "shot": 8, "muzzle": [124, 58], "angle": 90,
              "replace": {"8": 7}}                             # frame 8 = frame 7 (when a flash covers the body)
  },
  "mirror": {"west": "east", "south-west": "south-east", "north-west": "north-east"}
}
angle: degrees, + = clockwise on screen (90 = pointing down / at the camera, -90 = up).
Find "shot" and "muzzle" with find_muzzle.py. The effect plays from the shot frame, one effect frame per frame."""
import json
import os
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage

spec_path = os.path.abspath(sys.argv[1])
base = os.path.dirname(spec_path)
spec = json.load(open(spec_path))
P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
TOTAL = int(spec.get('total', 12))
SPECK = int(spec.get('speck', 40))
out_root = P(spec.get('out', 'final'))

fl = spec.get('flash')
flash_frames, anchor = [], (0, 0)
if fl:
    sheet = Image.open(P(fl['sheet'])).convert('RGBA')
    anchor = tuple(fl.get('anchor', [0, 0]))
    if fl.get('json'):
        for f in json.load(open(P(fl['json'])))['frames']:
            r = f['frame']
            flash_frames.append(sheet.crop((r['x'], r['y'], r['x'] + r['w'], r['y'] + r['h'])))
    else:   # a horizontal strip of square-ish frames of the given width
        fw = int(fl['frame_w'])
        flash_frames = [sheet.crop((x, 0, x + fw, sheet.height)) for x in range(0, sheet.width, fw)]


def rotated(img, angle):
    s = 2 * max(img.size) + 8
    c = Image.new('RGBA', (s, s))
    c.paste(img, (s // 2 - anchor[0], s // 2 - anchor[1]), img)
    return c.rotate(-angle, resample=Image.NEAREST), s // 2


def despeck(im):
    a = np.array(im)
    lab, n = ndimage.label(a[..., 3] > 0, structure=np.ones((3, 3)))
    if n > 1:
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        a[~np.isin(lab, [k + 1 for k, sz in enumerate(sizes) if sz >= SPECK])] = 0
    return Image.fromarray(a)


for d, c in spec['dirs'].items():
    src = P(c['src'])
    n = 0
    while os.path.exists(os.path.join(src, '%d.png' % n)):
        n += 1
    frames = [Image.open(os.path.join(src, '%d.png' % i)).convert('RGBA') for i in range(n)]
    for f, fr in c.get('replace', {}).items():
        frames[int(f)] = frames[int(fr)].copy()
    for f, boxes in c.get('clear', {}).items():
        a = np.array(frames[int(f)])
        for x0, y0, x1, y1 in boxes:
            a[y0:y1, x0:x1] = 0
        frames[int(f)] = Image.fromarray(a)
    frames = [despeck(f) for f in frames]
    while len(frames) < TOTAL:
        frames.append(frames[-1].copy())
    shot, (mx, my), ang = int(c['shot']), c['muzzle'], float(c.get('angle', 0))
    for k, ff in enumerate(flash_frames):
        if shot + k >= len(frames):
            break
        img, ctr = rotated(ff, ang)
        frames[shot + k].alpha_composite(img, (int(mx) - ctr, int(my) - ctr)) if mx - ctr >= 0 and my - ctr >= 0 \
            else frames[shot + k].paste(img, (int(mx) - ctr, int(my) - ctr), img)
    od = os.path.join(out_root, d)
    os.makedirs(od, exist_ok=True)
    for i, f in enumerate(frames):
        f.save(os.path.join(od, '%d.png' % i))
    print(d, len(frames), 'frames, shot', shot)

for w, e in spec.get('mirror', {}).items():
    od = os.path.join(out_root, w)
    os.makedirs(od, exist_ok=True)
    i = 0
    while os.path.exists(os.path.join(out_root, e, '%d.png' % i)):
        ImageOps.mirror(Image.open(os.path.join(out_root, e, '%d.png' % i))).save(os.path.join(od, '%d.png' % i))
        i += 1
    print(w, '= mirrored', e)
