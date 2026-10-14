"""Install the PixelLab game-art skill + /pga-* commands for Claude Code.

    python install.py              # all your projects (~/.claude/skills)
    python install.py --project    # only the project in the current folder (./.claude/skills)
    python install.py --pip        # also install the Python packages (pillow numpy scipy)
    python install.py --uninstall  # remove what this installer installed (add --project for that scope)

Run it from the unzipped folder (on macOS/Linux: python3 install.py). Running it again updates an
older install. Python 3.8+, no packages needed to run it. Your pixellab.json and anything you
generated are never touched.
"""
import os
import shutil
import subprocess
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

here = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
if '-h' in args or '--help' in args:
    sys.exit(__doc__)
if sys.version_info < (3, 8):
    sys.exit('Python 3.8 or newer is needed: https://www.python.org/downloads/')
for a in args:
    if a not in ('--project', '--pip', '--uninstall'):
        sys.exit('Unknown option %s. Options: --project  --pip  --uninstall  (see --help)' % a)


def real(p):
    return os.path.normcase(os.path.realpath(p))


def inside(path, folder):
    """True when path is folder itself or somewhere below it."""
    try:
        return os.path.commonpath([real(path), real(folder)]) == real(folder)
    except ValueError:   # different drives
        return False


def python_name():
    if os.name == 'nt':
        return 'python' if shutil.which('python') else 'py'
    return 'python' if shutil.which('python') else 'python3'


def quote(p):
    return '"%s"' % p if ' ' in p else p


def pip_install():
    cmd = [sys.executable, '-m', 'pip', 'install', 'pillow', 'numpy', 'scipy']
    shown = ' '.join([quote(cmd[0])] + cmd[1:])   # the exact command, for the retry hint
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        out, code = p.stdout or '', p.returncode
    except OSError as e:
        out, code = str(e), 1
    print(out.rstrip())
    if code == 0:
        print('Python packages: OK')
    elif 'externally-managed-environment' in out:
        print('Python packages: this Python is managed by your system, so pip refuses. Pick one:')
        print('  macOS (Homebrew):  brew install pillow numpy scipy')
        print('  Debian / Ubuntu:   sudo apt install python3-pil python3-numpy python3-scipy')
        print('  last resort:       %s -m pip install --user --break-system-packages pillow numpy scipy' % quote(sys.executable))
    else:
        print('Python packages: pip failed. Fix the error above, then retry:\n  ' + shown)


dest = os.path.join(os.getcwd(), '.claude', 'skills') if '--project' in args else os.path.join(os.path.expanduser('~'), '.claude', 'skills')
folders = sorted(d for d in os.listdir(here) if os.path.isfile(os.path.join(here, d, 'SKILL.md')))
for d in folders:   # a target that is, holds or sits inside its own source would be deleted or copied into itself
    if inside(os.path.join(dest, d), os.path.join(here, d)) or inside(os.path.join(here, d), os.path.join(dest, d)):
        sys.exit('Refusing: the install folder (%s) is the same as, or inside, the folder this installer runs from (%s).\n'
                 'Re-installing would delete the files it copies from. Run install.py from the unzipped download, '
                 'not from the destination.' % (dest, here))

if '--uninstall' in args:
    gone = []
    for d in folders:
        t = os.path.join(dest, d)
        if os.path.isdir(t):
            shutil.rmtree(t)
            gone.append(t)
    print('Removed %d folders from %s' % (len(gone), dest) if gone else 'Nothing to remove in %s' % dest)
    for t in gone:
        print('  ' + t)
    print('Kept: pixellab.json, your generated files, and the PixelLab connection (claude mcp remove pixellab removes that).')
    sys.exit(0)

def version_of(folder):
    try:
        return open(os.path.join(folder, 'VERSION'), encoding='utf-8').read().strip()
    except OSError:
        return None


os.makedirs(dest, exist_ok=True)
old_v = version_of(os.path.join(dest, 'pixellab-game-art'))
new_v = version_of(os.path.join(here, 'pixellab-game-art'))
for d in folders:
    target = os.path.join(dest, d)
    if os.path.exists(target):
        shutil.rmtree(target)
    shutil.copytree(os.path.join(here, d), target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
for d in os.listdir(dest):   # commands an older version had and this one dropped
    if d.startswith('pga-') and d not in folders and os.path.isfile(os.path.join(dest, d, 'SKILL.md')):
        shutil.rmtree(os.path.join(dest, d))
        print('Removed old command %s (not in this version)' % d)
was = '' if old_v is None else (', was %s' % old_v if old_v != new_v else ', same version refreshed')
print('Installed %d folders (version %s%s) into %s' % (len(folders), new_v or '?', was, dest))
py = python_name()
print('Run the skill\'s scripts with: %s   (e.g. %s %s)' % (py, py, os.path.join(dest, 'pixellab-game-art', 'scripts', 'check_setup.py')))

if '--pip' in args:
    pip_install()
else:
    missing = []
    for m in ('PIL', 'numpy', 'scipy'):
        try:
            __import__(m)
        except ImportError:
            missing.append({'PIL': 'pillow'}.get(m, m))
    print('Python packages: ' + ('OK' if not missing else 'missing %s - run: %s install.py --pip' % (' '.join(missing), py)))

print("""
Last step - connect PixelLab (once):
  1. Get your API token: https://api.pixellab.ai/mcp (sign in to PixelLab)
  2. Run (paste your token in place of YOUR_TOKEN):
     claude mcp add --transport http --scope user pixellab https://api.pixellab.ai/mcp --header "Authorization: Bearer YOUR_TOKEN"
  3. Restart Claude Code (in your game's folder) and type /pga-doctor - it checks everything and prints any fix
""")
