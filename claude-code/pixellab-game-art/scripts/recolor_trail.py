"""recolor_trail.py <dir> <frame>... [--hue red|orange|yellow|green|cyan|blue|purple|any] [--to air|fire|arcane|holy|shadow|none]
                   [--ref standing_sprite.png] [--from-scrub] [--outside-keys] [--body-gap 4] [--thick 5]

animate_image often paints a swing trail in the character's own colours (a red smear behind a red
tabard), which no colour filter can scrub. Instead of deleting it, turn it into an effect: finds the
trail - pixels of the chosen hue that are thin strokes (not a solid area like a tabard) and lie
away from the rest of the body - and recolours it by brightness into an effect ramp ("air" = a
pale cut through the air). Writes <frame>_t.png next to the input. Works on _s.png frames too
(pass "3_s").

With --ref (recommended): the trail is every pixel of the hue whose colour isn't in the standing
sprite's palette - generators paint trails brighter/purer than the character's own colours (a
(250,6,5) smear next to a (121,23,20) tabard), so this separates them cleanly.

  python recolor_trail.py raw 3 4 5 6 7 8 --hue red --to air --ref hero.png
  python recolor_trail.py raw 3 4 --from-scrub --to air   # after scrub.py: whatever scrub removed IS the slash -
                                                        # put it back recoloured (works for white/cream swooshes)
Needs Pillow, numpy, scipy.
"""
import argparse
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
import colorsys
import numpy as np
from PIL import Image
from scipy import ndimage

RAMPS = {   # dark -> bright
    'air': ['#5a7896', '#8fb4d8', '#bcd8f0', '#e8f4ff', '#ffffff'],
    'fire': ['#6e1409', '#b3260e', '#e8561a', '#f8a531', '#ffe08a'],
    'arcane': ['#2d0f4a', '#5a1f86', '#8f45c4', '#c48af0', '#f0d8ff'],
    'holy': ['#4a3410', '#b29352', '#debd77', '#fff2c4', '#ffffff'],
    'shadow': ['#0a0a12', '#1c1a2e', '#34304f', '#57527a', '#8a84b0'],
}
HUES = {'red': (330, 20), 'orange': (15, 45), 'yellow': (40, 70), 'green': (70, 170),
        'cyan': (170, 200), 'blue': (200, 255), 'purple': (255, 330)}

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


ap = argparse.ArgumentParser()
ap.add_argument('dir')
ap.add_argument('frames', nargs='+')
ap.add_argument('--hue', default='red', help='a named range, any, or LO,HI degrees (e.g. 330,3 = crimson without brown)')
ap.add_argument('--to', default='air', choices=list(RAMPS) + ['none'], help='none = delete the trail')
ap.add_argument('--ref', help='the standing sprite: hue pixels not in its palette are the trail')
ap.add_argument('--tol', type=float, default=30)
ap.add_argument('--outside-keys', action='store_true', help='trail = hue pixels outside the silhouettes of the two key poses (frame 0 and the last frame), grown by --body-gap; for trails drawn in the character own colours')
ap.add_argument('--above', type=int, default=0, help='only rows above this y count (keeps low cloak/robe tails out of a high arc)')
ap.add_argument('--from-scrub', action='store_true', help='trail = pixels scrub.py removed (needs <frame>_s.png)')
ap.add_argument('--body-gap', type=int, default=4, help='trail pixels must be at least this far from non-hue body pixels')
ap.add_argument('--thick', type=int, default=5, help='solid areas of the hue at least this thick are kept (tabards, capes)')
a = ap.parse_args()
a.frames = _frames(a.dir, a.frames)
lo, hi = tuple(float(v) for v in a.hue.split(',')) if ',' in a.hue else HUES.get(a.hue, (0, 360))
if a.hue == 'any' and not a.ref and not a.from_scrub:
    ap.error('--hue any needs --ref (the standing sprite)')
refpal = None
if a.ref:
    r = np.array(Image.open(a.ref).convert('RGBA'))
    refpal = np.unique(r[r[..., 3] > 0][:, :3], axis=0).astype(np.int32)
keys = None
if a.outside_keys:
    import glob, os, re
    nums = [int(m.group(1)) for m in (re.match(r'(\d+)\.png$', os.path.basename(q)) for q in glob.glob(os.path.join(a.dir, '*.png'))) if m]
    k0 = np.array(Image.open('%s/0.png' % a.dir).convert('RGBA'))[..., 3] > 0
    k1 = np.array(Image.open('%s/%d.png' % (a.dir, max(nums))).convert('RGBA'))[..., 3] > 0
    keys = ndimage.binary_dilation(k0 | k1, iterations=a.body_gap)
ramp = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in RAMPS.get(a.to, RAMPS['air'])])

for f in a.frames:
    path = '%s/%s.png' % (a.dir, f)
    x = np.array(Image.open(path).convert('RGBA'))
    op = x[..., 3] > 0
    rgb = x[..., :3].astype(float) / 255
    h = np.zeros(op.shape)
    s = np.zeros(op.shape)
    v = np.zeros(op.shape)
    for (yy, xx) in zip(*np.nonzero(op)):
        h[yy, xx], s[yy, xx], v[yy, xx] = colorsys.rgb_to_hsv(*rgb[yy, xx])
    deg = h * 360
    if a.hue == 'any':
        inhue = op.copy()
    else:
        inhue = op & (s > 0.35) & ((deg >= lo) & (deg <= hi) if lo < hi else ((deg >= lo) | (deg <= hi)))
    solid = ndimage.binary_opening(inhue, structure=np.ones((a.thick, a.thick)))
    solid = ndimage.binary_dilation(solid, iterations=2) & inhue        # keep the whole tabard, not just its core
    body = ndimage.binary_dilation(op & ~inhue, iterations=a.body_gap)  # skin, armour, hair, sword...
    trail = inhue & ~solid & ~body
    if refpal is not None:   # colour test against the original sprite beats the shape test
        px = x[..., :3][inhue].astype(np.int32)
        d = np.min(((px[:, None, :] - refpal[None, :, :]) ** 2).sum(-1), axis=1)
        trail = np.zeros_like(inhue)
        trail[inhue] = d > a.tol ** 2
    if keys is not None:
        trail = inhue & ~keys & ~body   # outside both key poses and not touching the rest of the body
    if a.from_scrub:
        sc = np.array(Image.open('%s/%s_s.png' % (a.dir, f)).convert('RGBA'))
        trail = op & (sc[..., 3] == 0)
    if a.above:
        trail[a.above:] = False
    # a trail stroke touching the body keeps its far part only; thin hue strokes fully inside body reach stay
    lum = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2])
    if trail.any() and a.to == 'none':
        x[..., 3][trail] = 0
    elif trail.any():
        lv = lum[trail]
        if np.percentile(lv, 90) - np.percentile(lv, 10) > 0.15:   # the trail has its own shading: map it onto the ramp
            q = np.clip(((lv - lv.min()) / (lv.max() - lv.min()) * (len(ramp) - 1)).round().astype(int), 0, len(ramp) - 1)
            x[..., :3][trail] = ramp[q]
        else:   # a flat smear: shade by depth - rim in the ramp's mid tone, white core, dithered deep inside
            depth = ndimage.distance_transform_cdt(trail, metric='chessboard')
            q = np.clip(depth, 1, len(ramp) - 1)
            x[..., :3][trail] = ramp[q[trail]]
            yy, xx = np.indices(trail.shape)
            airy = trail & (depth > 4) & ((yy + xx) % 2 == 0)
            x[..., 3][airy] = 0
    Image.fromarray(x).save('%s/%s_t.png' % (a.dir, f))
    print(f, 'recoloured', int(trail.sum()), 'px')
