"""colormatch.py <standing.png> <frames...> [--out DIR]
Fixes the colour shift of generated key poses and in-betweens: each frame's mean brightness is scaled to the
standing sprite's, then every opaque pixel is snapped to the standing sprite's own colours. Free, in place
unless --out is given. Run it AFTER scrub.py / dropping flash frames, BEFORE building the sheet or GIF.

  python colormatch.py hero.png frames/hit_*.png
"""
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
import glob
import os
import numpy as np
from PIL import Image

args = sys.argv[1:]
out = None
if '--out' in args:
    i = args.index('--out')
    out = args[i + 1]
    del args[i:i + 2]
    os.makedirs(out, exist_ok=True)
ref = np.array(Image.open(args[0]).convert('RGBA'))
pal = np.unique(ref[ref[..., 3] > 0][:, :3], axis=0).astype(float)
target = ref[ref[..., 3] > 0][:, :3].mean()
files = [f for p in args[1:] for f in (sorted(glob.glob(p)) if '*' in p or '?' in p else [p])]
for f in files:
    a = np.array(Image.open(f).convert('RGBA')).astype(float)
    m = a[..., 3] > 0
    if not m.any():
        continue
    k = target / a[m][:, :3].mean()
    px = np.clip(a[m][:, :3] * k, 0, 255)
    a[m, :3] = pal[((px[:, None, :] - pal[None]) ** 2).sum(2).argmin(1)]
    dst = os.path.join(out, os.path.basename(f)) if out else f
    Image.fromarray(a.astype('uint8')).save(dst)
    print('%s x%.2f' % (os.path.basename(f), k))
