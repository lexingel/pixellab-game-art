"""recolor_like.py <source_still> <new_still> <frame.png>... --out DIR [--keep-thin REDRAWN_DIR]
Recolours frames drawn in the source still's colours into the new still's (both stills in the same pose):
each source colour takes the hue/saturation of what the new still has at the same spot and the lightness of
the colour at its brightness rank, so the result keeps the source's contrast. Shades the still doesn't use
take their nearest mapped colour; colours the stills don't share keep the rank map.
--keep-thin REDRAWN_DIR: instead of the recoloured frame, write the same-named frame from REDRAWN_DIR (a redraw)
with the recoloured frame's thin parts pasted over it (blades, staffs, fingers: what a 5 px opening removes
from the silhouette), dropping redrawn pixels just around them that the source doesn't have.
Also prints frames that repeat an earlier one (draw those once).

  python recolor_like.py old/still.png new/still.png old/attack_*.png --out new_colours
  python recolor_like.py old/still.png new/still.png old/attack_*.png --out fixed --keep-thin redrawn
"""
import os
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if len(sys.argv) < 4 or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
import glob
import re

import cv2
import numpy as np
from PIL import Image

ALPHA, MAP_MIN, MAP_DIST, THIN, BAND = 128, 6, 90, 2, 3


def _expand(paths):
    """cmd/PowerShell pass *.png literally: expand * and ? here (natural order, so 2.png comes before 10.png)."""
    out = []
    for p in paths:
        hits = glob.glob(p) if ('*' in p or '?' in p) else []
        out += sorted(hits, key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]) or [p]
    return out


def _lum(a):
    return a @ [0.299, 0.587, 0.114]


def _lab(rgb):
    return cv2.cvtColor(np.ascontiguousarray(rgb.astype(np.uint8)), cv2.COLOR_RGB2LAB)


def still_map(src, new):
    """{source colour: median new colour under it}, stills aligned feet to feet and centre to centre."""
    a, b = np.array(src.convert('RGBA')), np.array(new.convert('RGBA'))
    ba, bb = src.getbbox(), new.getbbox()
    if not ba or not bb:
        return {}
    dx, dy = round((bb[0] + bb[2] - ba[0] - ba[2]) / 2), bb[3] - ba[3]
    ys, xs = np.nonzero(a[..., 3] >= ALPHA)
    ty, tx = ys + dy, xs + dx
    ok = (ty >= 0) & (ty < b.shape[0]) & (tx >= 0) & (tx < b.shape[1])
    ys, xs, ty, tx = ys[ok], xs[ok], ty[ok], tx[ok]
    ok = b[ty, tx, 3] >= ALPHA
    s, d = a[ys[ok], xs[ok], :3].astype(int), b[ty[ok], tx[ok], :3].astype(int)
    key = (s[:, 0] << 16) | (s[:, 1] << 8) | s[:, 2]
    return {((k >> 16) & 255, (k >> 8) & 255, k & 255): np.median(d[key == k], axis=0)
            for k in np.unique(key) if (key == k).sum() >= MAP_MIN}


def recolour(img, src, new):
    def ranked(im):
        x = np.array(im.convert('RGBA')).reshape(-1, 4)
        x = x[x[:, 3] >= ALPHA][:, :3].astype(float)
        return x[np.argsort(_lum(x))]
    old, nw = ranked(src), ranked(new)
    x = np.array(img.convert('RGBA')).astype(float)
    on = x[..., 3] >= ALPHA
    if not on.any() or not len(old) or not len(nw):
        return img.convert('RGBA')
    q = np.searchsorted(_lum(old), _lum(x[on][:, :3])) / len(old)
    x[on, :3] = nw[np.clip((q * len(nw)).astype(int), 0, len(nw) - 1)]
    by_rank = x.copy()
    cmap = still_map(src, new)
    if cmap:
        keys, vals = np.array(list(cmap), float), np.array(list(cmap.values()))
        orig = np.array(img.convert('RGBA'))[..., :3].astype(float)
        cols, inv = np.unique(orig[on], axis=0, return_inverse=True)
        d = np.abs(cols[:, None, :] - keys[None]).sum(-1)
        near = d.argmin(1)
        use = d[np.arange(len(cols)), near] <= MAP_DIST
        px, sel = x[on], use[inv.ravel()]
        px[sel, :3] = vals[near[inv.ravel()][sel]]
        x[on] = px
        lab = _lab(x[..., :3])
        lab[..., 0] = _lab(by_rank[..., :3])[..., 0]
        x[on, :3] = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)[on]
    return Image.fromarray(x.astype(np.uint8), 'RGBA')


def keep_thin(drawn, guide, search=3):
    d, g = np.array(drawn.convert('RGBA')), np.array(guide.convert('RGBA'))
    if d.shape != g.shape:
        return drawn
    da, ga = d[..., 3] > 0, g[..., 3] > 0
    best = (-1.0, 0, 0)
    for dy in range(-search, search + 1):
        for dx in range(-search, search + 1):
            s = np.roll(np.roll(ga, dy, 0), dx, 1)
            iou = (s & da).sum() / max(1, (s | da).sum())
            if iou > best[0]:
                best = (iou, dx, dy)
    g = np.roll(np.roll(g, best[2], 0), best[1], 1)
    ga = g[..., 3] > 0
    thin = ga & ~(cv2.morphologyEx(ga.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2 * THIN + 1,) * 2, np.uint8)) > 0)
    thin = (cv2.dilate(thin.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) & ga
    band = cv2.dilate(thin.astype(np.uint8), np.ones((2 * BAND + 1,) * 2, np.uint8)) > 0
    d[band & ~ga & ~(cv2.dilate((ga & ~thin).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0)] = 0
    d[thin] = g[thin]
    return Image.fromarray(d, 'RGBA')


args = sys.argv[1:]
opts = {}
for flag in ('--out', '--keep-thin'):
    if flag in args:
        i = args.index(flag)
        opts[flag] = args[i + 1]
        del args[i:i + 2]
if '--out' not in opts:
    sys.exit('--out DIR is required')
src, new = Image.open(args[0]), Image.open(args[1])
os.makedirs(opts['--out'], exist_ok=True)
seen = {}
for f in _expand(args[2:]):
    a = np.asarray(Image.open(f).convert('RGBA'), dtype=np.int16)
    rep = next((p for p, b in seen.items() if b.shape == a.shape and np.abs(a - b).mean() < 1.0), None)
    if rep:
        print('repeat: %s = %s (draw once)' % (os.path.basename(f), os.path.basename(rep)))
    else:
        seen[f] = a
    rec = recolour(Image.open(f), src, new)
    name = os.path.basename(f)
    if '--keep-thin' in opts:
        rec = keep_thin(Image.open(os.path.join(opts['--keep-thin'], name)), rec)
    rec.save(os.path.join(opts['--out'], name))
    print('wrote', os.path.join(opts['--out'], name))
