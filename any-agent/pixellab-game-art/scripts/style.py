"""style.py - named art styles in pixellab.json. Stdlib only.

  python style.py list                         # saved styles, the active one marked *
  python style.py show <name>                  # one style's fields as JSON
  python style.py save <name> [--from file.json] [--use]
        # save a style: from a JSON file of style fields, or (no --from) from the profile's current
        # top-level style fields; --use also makes it the active style. Overwrites a style of that name.
  python style.py use <name>                   # make it the active style (every command uses it)
  python style.py rename <old> <new>
  python style.py delete <name>
  python style.py anchor <family> <image.png> [--style <name>]
        # approve an image as the style's reference art for one asset family (heroes, monsters,
        # backgrounds, scenes, buildings, icons, ui); default: the active style
Options: --profile <path> (default ./pixellab.json; created if missing).

pixellab.json keeps project fields at the top (game, tier, out, engine, max_cost, seed) and art
styles under "styles": {"<name>": {<style fields>}} with "active_style": "<name>". A command's
effective style = top-level style fields, overlaid by the active style (or --style <name>).
"""
import json
import os
import sys

STYLE_KEYS = ['setting', 'density', 'look', 'palette', 'palette_hex', 'colors', 'outline', 'shading',
              'dither', 'light', 'view', 'facing', 'sizes', 'negatives', 'rules', 'anim', 'anchors',
              'seed', 'reference', 'analysed_from', 'notes']

args = sys.argv[1:]
if not args or args[0] in ('-h', '--help'):
    sys.exit(__doc__)
path = 'pixellab.json'
if '--profile' in args:
    i = args.index('--profile')
    path = args[i + 1]
    del args[i:i + 2]
prof = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
styles = prof.setdefault('styles', {})
cmd, rest = args[0], args[1:]


def save_profile():
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(prof, f, indent=2, ensure_ascii=False)
        f.write('\n')


def need(name):
    if name not in styles:
        sys.exit('no style "%s" - saved: %s' % (name, ', '.join(sorted(styles)) or 'none'))


if cmd == 'list':
    if not styles:
        print('no saved styles (top-level fields only)' if any(k in prof for k in STYLE_KEYS) else 'no saved styles')
    for n in sorted(styles):
        s = styles[n]
        print('%s %s  - %s' % ('*' if prof.get('active_style') == n else ' ', n,
                               ', '.join(str(s[k]) for k in ('setting', 'density', 'view', 'outline', 'shading') if k in s)))
elif cmd == 'show':
    need(rest[0])
    print(json.dumps(styles[rest[0]], indent=2, ensure_ascii=False))
elif cmd == 'save':
    name = rest[0]
    if '--from' in rest:
        src = json.load(open(rest[rest.index('--from') + 1], encoding='utf-8'))
    else:
        src = prof
    style = {k: src[k] for k in STYLE_KEYS if k in src}
    if not style:
        sys.exit('nothing to save: no style fields found')
    styles[name] = style
    if '--use' in rest or not prof.get('active_style'):
        prof['active_style'] = name
    save_profile()
    print('saved style "%s" (%d fields)%s -> %s' % (name, len(style), ', active' if prof['active_style'] == name else '', path))
elif cmd == 'use':
    need(rest[0])
    prof['active_style'] = rest[0]
    save_profile()
    print('active style: %s' % rest[0])
elif cmd == 'anchor':
    if len(rest) < 2:
        sys.exit('usage: style.py anchor <family> <image.png> [--style <name>]')
    family, img = rest[0], rest[1]
    families = ('heroes', 'monsters', 'backgrounds', 'scenes', 'buildings', 'icons', 'ui')
    if family not in families:
        sys.exit('family must be one of: ' + ', '.join(families))
    if not os.path.isfile(img):
        sys.exit('no such image: ' + img)
    name = rest[rest.index('--style') + 1] if '--style' in rest else prof.get('active_style')
    if not name:
        sys.exit('no active style - save one first (/pga-init) or pass --style <name>')
    need(name)
    styles[name].setdefault('anchors', {})[family] = img.replace(os.sep, '/')
    save_profile()
    try:
        from PIL import Image
        w, h = Image.open(img).size
        note = '' if max(w, h) <= 256 or family in ('backgrounds', 'scenes') else ' - note: %dx%d is over 256 px; sprite tools need <= 256' % (w, h)
    except Exception:
        note = ''
    print('anchor for %s in style "%s": %s%s' % (family, name, img, note))
elif cmd == 'rename':
    old, new = rest[0], rest[1]
    need(old)
    styles[new] = styles.pop(old)
    if prof.get('active_style') == old:
        prof['active_style'] = new
    save_profile()
    print('renamed %s -> %s' % (old, new))
elif cmd == 'delete':
    need(rest[0])
    del styles[rest[0]]
    if prof.get('active_style') == rest[0]:
        prof['active_style'] = sorted(styles)[0] if styles else None
    save_profile()
    print('deleted %s; active: %s' % (rest[0], prof.get('active_style')))
else:
    sys.exit(__doc__)
