"""slash_layer.py - lift a generated slash/crescent out of one animation and lay it on another.

  python slash_layer.py extract <raw_frame.png> <scrubbed_frame.png> <out_effect.png> [--to air]
      the effect = pixels scrub.py removed from that frame, recoloured (recolor_trail ramps) and
      depth-shaded (rim, light core, dithered body) - an image with only the slash on it
  python slash_layer.py apply <frame.png> <effect.png> <out.png> [--behind] [--fade 0.5]
      lays the effect on a frame (in front by default; --behind puts the character on top);
      --fade thins it with an ordered-dither mask for a trailing frame

Both swings must share the same canvas and key poses (e.g. a 7-frame and an 11-frame animate_image
from the same A/B poses) so the slash lands where the blade passes. Needs Pillow, numpy, scipy.
"""
import argparse
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
import numpy as np
from PIL import Image
from scipy import ndimage

RAMPS = {'air': ['#5a7896', '#8fb4d8', '#bcd8f0', '#e8f4ff', '#ffffff'],
         'fire': ['#6e1409', '#b3260e', '#e8561a', '#f8a531', '#ffe08a'],
         'arcane': ['#2d0f4a', '#5a1f86', '#8f45c4', '#c48af0', '#f0d8ff'],
         'holy': ['#4a3410', '#b29352', '#debd77', '#fff2c4', '#ffffff'],
         'shadow': ['#0a0a12', '#1c1a2e', '#34304f', '#57527a', '#8a84b0']}
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0

ap = argparse.ArgumentParser()
ap.add_argument('mode', choices=['extract', 'apply'])
ap.add_argument('a')
ap.add_argument('b')
ap.add_argument('out')
ap.add_argument('--to', default='air', choices=list(RAMPS))
ap.add_argument('--behind', action='store_true')
ap.add_argument('--fade', type=float, default=0.0)
a = ap.parse_args()

if a.mode == 'extract':
    raw = np.array(Image.open(a.a).convert('RGBA'))
    sc = np.array(Image.open(a.b).convert('RGBA'))
    m = (raw[..., 3] > 0) & (sc[..., 3] == 0)
    ramp = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in RAMPS[a.to]])
    depth = ndimage.distance_transform_cdt(m, metric='chessboard')
    out = np.zeros_like(raw)
    q = np.clip(depth, 1, len(ramp) - 1)
    out[..., :3][m] = ramp[q[m]]
    out[..., 3][m] = 255
    yy, xx = np.indices(m.shape)
    out[..., 3][m & (depth > 4) & ((yy + xx) % 2 == 0)] = 0
    Image.fromarray(out).save(a.out)
    print('effect', int(m.sum()), 'px ->', a.out)
else:
    fr = Image.open(a.a).convert('RGBA')
    fx = np.array(Image.open(a.b).convert('RGBA'))
    if a.fade > 0:
        h, w = fx.shape[:2]
        thr = np.tile(BAYER, (h // 4 + 1, w // 4 + 1))[:h, :w]
        fx[..., 3][thr < a.fade] = 0
    fx = Image.fromarray(fx)
    base = Image.new('RGBA', fr.size)
    if a.behind:
        base.alpha_composite(fx)
        base.alpha_composite(fr)
    else:
        base.alpha_composite(fr)
        base.alpha_composite(fx)
    base.save(a.out)
    print('->', a.out)
