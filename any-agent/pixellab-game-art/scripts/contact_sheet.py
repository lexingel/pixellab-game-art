"""contact_sheet.py <out.png> a.png b.png c.png [--row d.png e.png ...] [--scale 0.5]
(old form still works: comma-joined rows "a.png,b.png c.png,d.png" - but avoid it on Windows Git Bash,
which mangles comma-joined C:/ paths)
One row per comma list, frames left to right on a neutral grey, to eyeball a batch
(e.g. the 7 raw frames of an animate_image job, or old vs new frames).

  python contact_sheet.py sheet.png hero_pad.png,poseA.png,poseB.png  raw/0.png,raw/1.png,raw/2.png
"""
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

from PIL import Image

args = sys.argv[2:]
if not args or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
scale = 1.0
if '--scale' in args:   # review at half size: a quarter of the image tokens
    i = args.index('--scale')
    scale = float(args[i + 1])
    del args[i:i + 2]
if '--row' in args or not any(',' in x for x in args):   # space-separated, rows split by --row
    groups, cur = [], []
    for x in args:
        if x == '--row':
            groups.append(cur)
            cur = []
        else:
            cur.extend(_expand([x]))
    groups.append(cur)
    rows = [[Image.open(p).convert('RGBA') for p in g] for g in groups if g]
else:
    rows = [[Image.open(p).convert('RGBA') for p in _expand(r.split(','))] for r in args]
cw = max(i.width for r in rows for i in r)
ch = max(i.height for r in rows for i in r)
out = Image.new('RGBA', (cw * max(len(r) for r in rows), ch * len(rows)), (60, 60, 70, 255))
for y, r in enumerate(rows):
    for x, im in enumerate(r):
        out.alpha_composite(im, (x * cw, y * ch + ch - im.height))
if scale != 1.0:
    out = out.resize((max(1, int(out.width * scale)), max(1, int(out.height * scale))), Image.NEAREST)
out.save(sys.argv[1])
print(sys.argv[1], out.size)
