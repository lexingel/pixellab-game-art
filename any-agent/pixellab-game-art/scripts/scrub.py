"""scrub.py <dir> <frame>... [--keep-main] [--tol 40]: in an animate_image raw folder (0.png .. N.png), clear pixels whose colour is far
from every colour of the first and last frame (the key poses): the flashes/streaks the generator paints in. Writes <i>_s.png.
--clear-right X / --clear-left X: also clear every pixel right (left) of column X - for shots, where the generator paints
its own muzzle flash in front of the barrel partly in colours the sprite has (armour white), which the colour test keeps.
X = the barrel tip in the aim pose; the barrel only kicks back from there."""
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
from PIL import Image
import numpy as np
from scipy import ndimage
def _frames(d, names):
    """Frame names like 3 or 0* (cmd/PowerShell don't expand globs): expand against <d>/<name>.png, numeric order."""
    import glob
    import os
    import re
    out = []
    for n in names:
        if '*' in n or '?' in n:
            hits = [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(d, (n[:-4] if n.endswith('.png') else n) + '.png'))]
            keep = [h for h in hits if h.isdigit() or n.endswith(('_s', '_t'))]   # plain '*' = the raw frames only
            out += sorted(keep, key=lambda h: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', h)]) or [n]
        else:
            out.append(n)
    return out

SPECK = 12   # detached clusters smaller than this many pixels are cleared too
argv = sys.argv[1:]
TOL = 40   # colour distance to the key poses' palette; lower (20-25) catches trails in the character's own hues
if '--tol' in argv:
    i = argv.index('--tol'); TOL = float(argv[i + 1]); del argv[i:i + 2]
CLR = {}
for k in ('--clear-right', '--clear-left'):
    if k in argv:
        i = argv.index(k); CLR[k] = int(argv[i + 1]); del argv[i:i + 2]
args = [a for a in argv if a != '--keep-main']
KEEP_MAIN = '--keep-main' in sys.argv
d = args[0]
pal = set()
import glob, os, re
last = max(int(m.group(1)) for m in (re.match(r'(\d+)\.png$', os.path.basename(q)) for q in glob.glob(os.path.join(d, '*.png'))) if m)
for k in (0, last):   # the two key poses: first and last frame (7-frame swings: 6, 11-frame: 10)
    a = np.array(Image.open('%s/%d.png' % (d, k)).convert('RGBA'))
    pal |= {tuple(p[:3]) for p in a.reshape(-1, 4) if p[3] > 0}
P = np.array(sorted(pal), dtype=np.int32)
for f in _frames(d, args[1:]):
    a = np.array(Image.open('%s/%s.png' % (d, f)).convert('RGBA'))
    m = a[..., 3] > 0
    px = a[m][:, :3].astype(np.int32)
    dist = np.min(((px[:, None, :] - P[None, :, :]) ** 2).sum(-1), axis=1)
    keep = dist < TOL ** 2
    al = a[..., 3].copy(); al[m] = np.where(keep, al[m], 0)
    if '--clear-right' in CLR:
        al[:, CLR['--clear-right'] + 1:] = 0
    if '--clear-left' in CLR:
        al[:, :CLR['--clear-left']] = 0
    lab, n = ndimage.label(al > 0, structure=np.ones((3, 3)))
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    al[np.isin(lab, np.nonzero(sizes < SPECK)[0] + 1)] = 0
    if KEEP_MAIN and n:
        near = ndimage.binary_dilation(lab == int(np.argmax(sizes)) + 1, iterations=6)
        for c in range(1, n + 1):
            if not (near & (lab == c)).any():
                al[lab == c] = 0
    a[..., 3] = al
    Image.fromarray(a).save('%s/%s_s.png' % (d, f))
    print(f, 'cleared', int((~keep).sum()), 'of', int(m.sum()))
