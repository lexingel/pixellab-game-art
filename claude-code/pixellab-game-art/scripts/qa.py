"""qa.py - automatic checks on generated images BEFORE anyone looks at them, so only flagged
images need a visual review (images are the most expensive thing for Claude to read).

  python qa.py out/*.png                         # sprites/icons: expect a transparent background
  python qa.py bg.png --opaque                    # scenes/backgrounds
  python qa.py raw/*.png --anim                   # animation frames: also flags flashes vs first/last frame
  python qa.py new.png --anchor approved.png      # palette drift against an approved asset
  ... --sheet flagged.png                         # contact sheet of the flagged images only

Checks: empty image · background not transparent (or not opaque with --opaque) · subject touching
the canvas edge (likely cropped) · colours far from the anchor's palette · (--anim) off-palette
flash pixels and size changes between frames. Prints one line per image ("OK" or "FLAG: …") and a
summary; exit code is always 0 (it informs, it doesn't block).
Needs Pillow + numpy.
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

import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('files', nargs='+')
ap.add_argument('--opaque', action='store_true')
ap.add_argument('--anim', action='store_true')
ap.add_argument('--anchor')
ap.add_argument('--sheet')
ap.add_argument('--drift', type=float, default=0.08, help='flag if more than this share of pixels is off the anchor palette')
a = ap.parse_args()
a.files = _expand(a.files)


def palette(arrs, cap=4000):
    px = np.concatenate([x[x[..., 3] > 0][:, :3] for x in arrs]).astype(np.int32)
    px = np.unique(px, axis=0)
    if len(px) > cap:
        px = px[np.linspace(0, len(px) - 1, cap).astype(int)]
    return px


def off_share(arr, pal, thr=40):
    px = arr[arr[..., 3] > 0][:, :3].astype(np.int32)
    if len(px) == 0:
        return 0.0, 0
    off = 0
    for i in range(0, len(px), 4000):   # chunks keep memory small
        d = ((px[i:i + 4000, None, :] - pal[None, :, :]) ** 2).sum(-1).min(1)
        off += int((d > thr * thr).sum())
    return off / len(px), off


imgs = [(f, np.array(Image.open(f).convert('RGBA'))) for f in a.files]
anchor_pal = palette([np.array(Image.open(a.anchor).convert('RGBA'))]) if a.anchor else None
anim_pal = palette([imgs[0][1], imgs[-1][1]]) if a.anim and len(imgs) > 1 else None
flagged = []
for i, (f, x) in enumerate(imgs):
    why = []
    alpha = x[..., 3]
    h, w = alpha.shape
    if (alpha > 0).sum() < 0.002 * w * h:
        why.append('almost empty')
    edge = np.concatenate([alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]])
    if a.opaque:
        if (alpha < 255).mean() > 0.01:
            why.append('has transparent pixels (expected an opaque scene)')
    else:
        if (edge > 0).mean() > 0.6:
            why.append('background not transparent')
        elif (edge > 0).sum() >= 3:
            why.append('touches the canvas edge (%d px) - maybe cropped' % int((edge > 0).sum()))
    if anchor_pal is not None:
        share, _ = off_share(x, anchor_pal)
        if share > a.drift:
            why.append('%.0f%% of pixels off the anchor palette' % (share * 100))
    if anim_pal is not None and 0 < i < len(imgs) - 1:
        if x.shape != imgs[0][1].shape:
            why.append('frame size differs from frame 0')
        else:
            share, n = off_share(x, anim_pal)
            if n > 60 and share > 0.01:
                why.append('flash: %d px (%.1f%%) not in the first/last frame colours - scrub.py or drop' % (n, share * 100))
    print(('FLAG: ' + '; '.join(why) if why else 'OK') + '  ' + f)
    if why:
        flagged.append(x)
print('\n%d checked, %d flagged' % (len(imgs), len(flagged)))
if a.sheet and flagged:
    cw = max(x.shape[1] for x in flagged)
    ch = max(x.shape[0] for x in flagged)
    out = Image.new('RGBA', (cw * len(flagged), ch), (60, 60, 70, 255))
    for k, x in enumerate(flagged):
        out.alpha_composite(Image.fromarray(x), (k * cw, ch - x.shape[0]))
    out.save(a.sheet)
    print('flagged sheet:', a.sheet)
