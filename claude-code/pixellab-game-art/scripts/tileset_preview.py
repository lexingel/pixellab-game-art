"""tileset_preview.py <out.png> <sheet.png> [<sheet2.png> ...] [--cells 24] [--seed 1] [--scale 2]
Paints a random test map from top-down Wang tilesets the way an engine autotiles them, so seams,
wrong corners and a chain that doesn't match show up before the tiles go into a game.
Each sheet needs its metadata next to it as <sheet>.json - `fetch.py <tileset_id> <sheet.png> --tileset` saves both.
Several tilesets = a chain in order (sea>beach, then beach>grass made with the beach base tile id):
the map gets one more terrain level per tileset, and each border uses the tileset for its two levels.
Also writes <out>_tiles.png: every tile of each sheet cut by its bounding_box, with its corners -
look at the diagonal tiles 0110 / 1001 there; a random map rarely uses them.

  python tileset_preview.py map.png sea_beach.png beach_grass.png
"""
import json
import os
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if len(sys.argv) < 4 or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
import numpy as np
from PIL import Image, ImageDraw

args = sys.argv[1:]


def _flag(name, default):
    if name in args:
        i = args.index(name)
        v = args[i + 1]
        del args[i:i + 2]
        return int(v)
    return default


cells, seed, scale = _flag('--cells', 24), _flag('--seed', 1), _flag('--scale', 2)
out, sheets = args[0], args[1:]

sets = []   # per tileset: {(NW,NE,SW,SE) as 0/1: tile image}
for sheet in sheets:
    meta = os.path.splitext(sheet)[0] + '.json'
    img = Image.open(sheet).convert('RGBA')
    tiles = json.load(open(meta, encoding='utf-8'))['tileset_data']['tiles']
    if any('transition' in t['corners'].values() for t in tiles):
        # ponytail: 16-tile sets only; 25-tile cliff sets need the wall-row rule (a wall fills the cell below)
        sys.exit('%s is a 25-tile cliff set (transition_size 0.5/1.0) - this preview handles 16-tile sets' % meta)
    lut = {}
    for t in tiles:
        b, c = t['bounding_box'], t['corners']
        key = tuple(int(c[k] == 'upper') for k in ('NW', 'NE', 'SW', 'SE'))
        lut.setdefault(key, img.crop((b['x'], b['y'], b['x'] + b['width'], b['y'] + b['height'])))
    missing = [k for k in np.ndindex(2, 2, 2, 2) if k not in lut]
    if missing:
        sys.exit('%s lacks corner combos %s' % (meta, missing))
    sets.append(lut)

tw, th = sets[0][(0, 0, 0, 0)].size
levels = len(sets) + 1
rng = np.random.default_rng(seed)
coarse = rng.random((cells // 6 + 2, cells // 6 + 2))
field = np.asarray(Image.fromarray((coarse * 255).astype(np.uint8)).resize((cells + 1, cells + 1), Image.BICUBIC),
                   dtype=np.float32) / 255
v = np.clip((field * levels).astype(int), 0, levels - 1)
for _ in range(levels):   # neighbouring corners may differ by one level only (one tileset per cell)
    p = np.pad(v, 1, mode='edge')
    nb = np.min([p[1 + dy:p.shape[0] - 1 + dy, 1 + dx:p.shape[1] - 1 + dx]
                 for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
    v = np.minimum(v, nb + 1)

m = Image.new('RGBA', (cells * tw, cells * th))
for y in range(cells):
    for x in range(cells):
        c = (v[y, x], v[y, x + 1], v[y + 1, x], v[y + 1, x + 1])
        low = min(min(c), levels - 2)
        m.paste(sets[low][tuple(int(k > low) for k in c)], (x * tw, y * th))
m = m.resize((m.width * scale, m.height * scale), Image.NEAREST)
m.save(out)

pad = 14
sheet = Image.new('RGBA', (16 * (tw + 4) + 4, len(sets) * (th + pad + 4) + 4), (40, 40, 48, 255))
d = ImageDraw.Draw(sheet)
for r, lut in enumerate(sets):
    for i, k in enumerate(sorted(lut)):
        x, y = 4 + i * (tw + 4), 4 + r * (th + pad + 4)
        sheet.paste(lut[k], (x, y))
        d.text((x, y + th + 1), ''.join(map(str, k)), fill=(220, 220, 220, 255))
tiles_png = os.path.splitext(out)[0] + '_tiles.png'
sheet.resize((sheet.width * scale, sheet.height * scale), Image.NEAREST).save(tiles_png)
print('%s  %dx%d cells, %d terrain levels\n%s  corners NW NE SW SE (1 = upper)' % (out, cells, cells, levels, tiles_png))
