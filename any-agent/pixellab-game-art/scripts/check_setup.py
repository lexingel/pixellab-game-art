"""check_setup.py [command]: checks the local tools a pga-* task command needs and prints how to fix
what's missing. Stdlib only, so it runs before anything is installed. (The PixelLab connection
itself is checked by the agent calling the get_balance tool - a script can't see MCP servers.)

  python check_setup.py pga-anim          (macOS/Linux: python3 check_setup.py pga-anim)
"""
import importlib.util
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

STDLIB = ('pga-help', 'pga-prompt', 'pga-style', 'pga-feedback', 'pga-tech', 'pga-doctor', 'pga-history')   # no local packages at all
IMAGE = ('pga-init', 'pga-analyze', 'pga-reroll', 'pga-start', 'pga-char', 'pga-bg', 'pga-scene', 'pga-building', 'pga-icon', 'pga-vfx', 'pga-batch')
NEEDS = {c: [] for c in STDLIB}   # what each command uses locally besides the PixelLab MCP server (downloads/uploads are stdlib)
NEEDS.update({c: ['pillow', 'numpy'] for c in IMAGE})   # pga-init / pga-analyze run analyze_style.py
NEEDS['pga-anim'] = ['pillow', 'numpy', 'scipy']
IMPORT = {'pillow': 'PIL'}
if sys.argv[1:2] in (['-h'], ['--help']):
    sys.exit(__doc__)
cmd = (sys.argv[1] if len(sys.argv) > 1 else 'pga-anim').lstrip('/')
need = NEEDS.get(cmd, [])   # unknown name: stdlib only
missing, pkgs = [], []
ok = sys.version_info >= (3, 8)
print('python  %s  %s  (%s)' % ('OK' if ok else 'TOO OLD', sys.version.split()[0], sys.executable))
if not ok:
    missing.append('python 3.8+ (https://www.python.org/downloads/)')
for n in need:
    found = importlib.util.find_spec(IMPORT.get(n, n)) is not None
    print('%-7s %s' % (n, 'OK' if found else 'MISSING'))
    if not found:
        pkgs.append(n)
if pkgs:
    py = '"%s"' % sys.executable if ' ' in sys.executable else sys.executable
    missing.append('%s -m pip install %s' % (py, ' '.join(pkgs)))
    missing.append('(on macOS/Linux run the scripts with python3; if pip says "externally-managed-environment", '
                   'see install.py --pip for the options)')
if missing:
    print('\nTO FIX:')
    for m in missing:
        print('  - ' + m)
    sys.exit(1)
print('\nALL_OK')
