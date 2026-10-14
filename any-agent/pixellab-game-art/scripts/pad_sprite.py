"""pad_sprite.py <sprite.png> <out.png> <canvas_w> <canvas_h> <x> [y]
Pastes a standing sprite onto a bigger transparent canvas so a swing has room. y defaults to
"feet on the bottom edge". Prints the offset to record for the engine (where the sprite's
top-left sits on the padded frames). Then upload <out.png> with PixelLab's get_upload_url + curl.

  python pad_sprite.py hero.png hero_pad.png 192 256 24        # hero: 72 px in front, room above
  python pad_sprite.py boss.png boss_pad.png 256 256 80        # boss facing left: room on the left
"""
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
from PIL import Image

src, out, w, h, x = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
im = Image.open(src).convert('RGBA')
y = int(sys.argv[6]) if len(sys.argv) > 6 else h - im.height
assert x + im.width <= w and y + im.height <= h, 'sprite does not fit the canvas'
c = Image.new('RGBA', (w, h))
c.alpha_composite(im, (x, y))
c.save(out)
print('offset', x, y)
