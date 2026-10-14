"""ground_snap.py <standing_sprite.png> <pad_x,pad_y> <frame.png>... [--out DIR] [--check]

Generated key poses and their in-betweens are often drawn a few to ~20 px higher on the padded
canvas than the standing sprite (kneels, lunges, crouches), so in the game the character hops off
the ground. For grounded moves (a foot or knee always on the floor) this moves each frame down so
its lowest opaque pixel sits exactly on the standing sprite's feet line (pad_y + sprite height - 1).
Frames already on or below the line are left alone. Writes in place unless --out is given.
--check only prints each frame's gap (negative = floating) and changes nothing.
Don't use it on jumps, leaps or flying characters.

  python ground_snap.py hero.png 24,56 out/hero_attack_*.png --check
  python ground_snap.py hero.png 24,56 out/hero_attack_*.png
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

import os
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('sprite')
ap.add_argument('pad')
ap.add_argument('frames', nargs='+')
ap.add_argument('--out')
ap.add_argument('--check', action='store_true')
a = ap.parse_args()
a.frames = _expand(a.frames)
st = np.array(Image.open(a.sprite).convert('RGBA'))[..., 3] > 0
pad_y = int(a.pad.split(',')[1])
feet = pad_y + int(np.nonzero(st.any(1))[0].max())
for f in a.frames:
    im = Image.open(f).convert('RGBA')
    al = np.array(im)[..., 3] > 0
    if not al.any():
        print('EMPTY', f)
        continue
    low = int(np.nonzero(al.any(1))[0].max())
    gap = low - feet
    print('%+4d  %s' % (gap, f))
    if a.check or gap >= 0:
        continue
    out = Image.new('RGBA', im.size)
    out.alpha_composite(im, (0, -gap))
    dst = os.path.join(a.out, os.path.basename(f)) if a.out else f
    out.save(dst)
