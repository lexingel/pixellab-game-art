"""profile.py - read or change one project setting in pixellab.json. Stdlib only.

  python profile.py get <key>
  python profile.py set <key> <value>      # value: true/false, a number, null, or text
Options: --profile <path> (default ./pixellab.json; created if missing).
Use it for plain project settings (beginner, output, max_cost, engine, out, tier) - styles have
style.py and sharing has share.py.
"""
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
args = sys.argv[1:]
if not args or args[0] in ('-h', '--help'):
    sys.exit(__doc__)
path = 'pixellab.json'
if '--profile' in args:
    i = args.index('--profile')
    if i + 1 >= len(args):
        sys.exit('--profile needs a path')
    path = args[i + 1]
    del args[i:i + 2]
prof = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
KEYS = ('beginner', 'output', 'max_cost', 'engine', 'out', 'tier', 'game', 'seed')
if args[0] == 'get' and len(args) == 2:
    print(json.dumps(prof.get(args[1])))
elif args[0] == 'set' and len(args) == 3:
    key, raw = args[1], args[2]
    if key not in KEYS:
        sys.exit('unknown setting %s (known: %s; styles -> style.py, sharing -> share.py)' % (key, ', '.join(KEYS)))
    try:
        val = json.loads(raw)
    except ValueError:
        val = raw
    prof[key] = val
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(prof, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print('%s = %s' % (key, json.dumps(val)))
else:
    sys.exit(__doc__)
