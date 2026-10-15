"""normal_map.py - the local half of create_normal_map (the PixelLab call itself is 0.5 generation).

  gif <out.gif> <frame1.png> <frame2.png> ...     pack animation frames into one GIF to upload: the MCP
                                                  tool reads a GIF's frames, but takes a PNG strip as ONE image
  split <strip_n.png> <frame1.png> <frame2.png> ...  cut the returned strip and save <frame>_n.png next to each frame
  preview <out.gif> <sprite.png> <normal.png> [--frames N] [--scale 2]
                                                  a light circling the sprite (strip: N frames, the animation
                                                  plays while it circles) - the way to judge a map; flat or
                                                  banded areas show up as parts that don't change with the light

  python normal_map.py gif up.gif anim/brute_attack_*.png
  python normal_map.py split brute_n.png anim/brute_attack_*.png
  python normal_map.py preview lit.gif brute_strip.png brute_n.png --frames 11
"""
import math
import os
import re
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if len(sys.argv) < 3 or sys.argv[1] not in ('gif', 'split', 'preview'):
    sys.exit(__doc__)
import glob
import numpy as np
from PIL import Image


def _expand(paths):
    """cmd/PowerShell pass *.png literally: expand * and ? here (natural order, so 2.png comes before 10.png)."""
    out = []
    for p in paths:
        hits = glob.glob(p) if ('*' in p or '?' in p) else []
        out += sorted(hits, key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]) or [p]
    return out


def _flag(args, name, default):
    if name in args:
        i = args.index(name)
        v = args[i + 1]
        del args[i:i + 2]
        return int(v)
    return default


cmd, args = sys.argv[1], sys.argv[2:]

if cmd == 'gif':
    out, frames = args[0], [Image.open(f).convert('RGBA') for f in _expand(args[1:])]
    w, h = frames[0].size
    if any(f.size != (w, h) for f in frames):
        sys.exit('frames differ in size - pad them to one canvas first (pad_sprite.py)')
    pal = []
    for f in frames:   # GIF alpha is on/off: index 255 = transparent, the rest = up to 255 colours
        p = f.convert('RGB').quantize(255)
        p.paste(255, mask=Image.fromarray(((np.asarray(f)[..., 3] < 128) * 255).astype(np.uint8)))
        pal.append(p)
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=100, loop=0, disposal=2, transparency=255,
                optimize=False)   # optimize remaps the palette and loses the transparent index
    print('%s  %d frames %dx%d - upload it and pass upload:<id> as image' % (out, len(frames), w, h))

elif cmd == 'split':
    strip, names = Image.open(args[0]).convert('RGBA'), _expand(args[1:])
    w = strip.width // len(names)
    if w * len(names) != strip.width:
        sys.exit('strip is %d px wide, not a multiple of %d frames' % (strip.width, len(names)))
    for i, n in enumerate(names):
        dst = os.path.splitext(n)[0] + '_n.png'
        strip.crop((i * w, 0, (i + 1) * w, strip.height)).save(dst)
        print(dst)

else:
    scale = _flag(args, '--scale', 2)
    n = _flag(args, '--frames', 1)
    out, sprite, normal = args[0], Image.open(args[1]).convert('RGBA'), Image.open(args[2]).convert('RGBA')
    if sprite.size != normal.size:
        sys.exit('sprite %s and map %s differ in size' % (sprite.size, normal.size))
    alb = np.asarray(sprite, dtype=np.float32) / 255
    nrm = np.asarray(normal, dtype=np.float32)[..., :3] / 127.5 - 1    # opengl: x right, y up, z out
    nrm /= np.maximum(np.linalg.norm(nrm, axis=2, keepdims=True), 1e-6)
    fw = sprite.width // n

    def shade(a):
        """The whole strip lit from angle a (0 = right, pi/2 = top), on a dark ground."""
        light = np.array([math.cos(a), math.sin(a), 0.6])
        light /= np.linalg.norm(light)
        lit = np.clip(nrm @ light, 0, 1) * 0.85 + 0.25                  # lambert + ambient
        img = np.dstack([np.clip(alb[..., :3] * lit[..., None], 0, 1), alb[..., 3:]]) * 255
        bg = Image.new('RGBA', sprite.size, (40, 40, 48, 255))
        bg.alpha_composite(Image.fromarray(img.astype(np.uint8), 'RGBA'))
        return bg.convert('RGB')

    steps = max(24, n * 3)
    gifs = []
    for s in range(steps):
        f = s * n // steps
        frame = shade(2 * math.pi * s / steps).crop((f * fw, 0, (f + 1) * fw, sprite.height))
        gifs.append(frame.resize((fw * scale, sprite.height * scale), Image.NEAREST))
    gifs[0].save(out, save_all=True, append_images=gifs[1:], duration=80, loop=0)
    # one still to look at: rows = light from the left, top, right; columns = frames
    rows = [shade(a) for a in (math.pi, math.pi / 2, 0)]
    sheet = Image.new('RGB', (sprite.width, sprite.height * 3))
    for i, r in enumerate(rows):
        sheet.paste(r, (0, i * sprite.height))
    still = os.path.splitext(out)[0] + '_lights.png'
    sheet.save(still)
    print('%s  %d steps, light circles once\n%s  rows: light from left, top, right' % (out, steps, still))
