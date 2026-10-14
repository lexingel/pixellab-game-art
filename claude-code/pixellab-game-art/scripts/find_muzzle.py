"""find_muzzle.py <frames_dir> [--min 60]: finds the shot frame and the muzzle in a generated shooting
animation (0.png .. N.png), using the generator's own flash as a locator.

animate_image / animate_character paint a flash of their own on the shot (white orb, yellow star,
beam lines, cyan sparks). It is usually the wrong colour, but it sits right at the muzzle. This script
lists the bright blobs on every frame and guesses:
  shot frame = the frame with the biggest bright blob (>= --min px),
  muzzle     = where that blob meets the gun (its pixels closest to the character's light pixels).
It prints a spec line for dir8_finish.py; check it on the frame before using it - the guess is off when the
flash covers the body or overlaps the gun (then read the muzzle off the frame by eye)."""
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
from PIL import Image
from scipy import ndimage

d = sys.argv[1]
MIN = int(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 60
n = 0
while os.path.exists(os.path.join(d, '%d.png' % n)):
    n += 1
if n == 0:
    sys.exit('no 0.png .. N.png frames in ' + d)


def bright_mask(a):
    rgb, al = a[..., :3], a[..., 3] > 0
    white = rgb.min(-1) > 200
    yellow = (rgb[..., 0] > 200) & (rgb[..., 1] > 170) & (rgb[..., 2] < 140)
    cyan = (rgb[..., 1] > 200) & (rgb[..., 2] > 200) & (rgb[..., 0] < 160)
    return al & (white | yellow | cyan)


best = None   # (size, frame, labels, label id, alpha)
for i in range(n):
    a = np.array(Image.open(os.path.join(d, '%d.png' % i)).convert('RGBA')).astype(int)
    lab, k = ndimage.label(bright_mask(a), structure=np.ones((3, 3)))
    blobs = []
    for j in range(1, k + 1):
        ys, xs = np.nonzero(lab == j)
        if len(xs) >= 6:
            blobs.append((len(xs), j, int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())))
    blobs.sort(reverse=True)
    print(i, [(b[0], 'x%d-%d' % (b[2], b[3]), 'y%d-%d' % (b[4], b[5])) for b in blobs[:3]])
    if blobs and blobs[0][0] >= MIN and (best is None or blobs[0][0] > best[0]):
        best = (blobs[0][0], i, lab, blobs[0][1], a)

if best is None:
    print('no flash >= %d px: pick the shot frame by eye (the frame where the arm is fully extended)' % MIN)
    sys.exit(0)
size, shot, lab, j, a = best
flash = lab == j
body = (a[..., 3] > 0) & ~ndimage.binary_dilation(flash, iterations=2)
blab, bn = ndimage.label(body, structure=np.ones((3, 3)))   # the character = the biggest piece, not stray sparks
if bn > 1:
    body = blab == (int(np.argmax(ndimage.sum(np.ones_like(blab), blab, range(1, bn + 1)))) + 1)
light = body & (a[..., :3].min(-1) > 120)                   # light pixels: the gun (white / metal) if it has any
target = light if light.sum() >= 4 else body
dist = ndimage.distance_transform_edt(~target)  # distance of every pixel to the nearest gun pixel
fy, fx = np.nonzero(flash)
fd = dist[fy, fx]
near = fd <= fd.min() + 1.0                     # the flash pixels touching the gun
mx, my = int(np.median(fx[near])), int(np.median(fy[near]))
ys, xs = np.nonzero(flash)
print('\nshot frame %d (flash %d px), muzzle ~(%d, %d)' % (shot, size, mx, my))
print('spec: {"shot": %d, "muzzle": [%d, %d], "angle": <deg, + = down>, "clear": {"%d": [[%d, %d, %d, %d]]}}'
      % (shot, mx, my, shot, int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
print('if the flash covers the body, use "replace": {"%d": %d} instead of a clear box' % (shot, max(0, shot - 1)))
