"""update.py - get the weekly skill update and merge it into this install. Stdlib only.

    python update.py                 # update: back up, install the new version, keep files you changed
    python update.py check           # is a newer version out? (one line)
    python update.py check --weekly  # same, but asks the internet at most once a week (setup check uses this)
    python update.py rollback        # put the install from before the last update back
    python update.py --from <zip|folder>   # update from a download (the repo ZIP or an unzipped copy)
    python update.py --force         # reinstall even when the version is the same

Your pixellab.json, styles, logs and generated files live outside the skill folder and are never
touched. Files you edited inside the skill folder are kept; when the update changed the same file,
its new version is put next to yours as <file>.from-update for your assistant to merge.
PIXELLAB_SKILL_UPDATE_URL = another ZIP to update from; PIXELLAB_SKILL_NO_UPDATE_CHECK=1 = no weekly check.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

REPO = 'https://github.com/lexingel/pixellab-game-art'
ZIP_URL = os.environ.get('PIXELLAB_SKILL_UPDATE_URL', REPO + '/archive/refs/heads/main.zip')
VERSION_URL = 'https://raw.githubusercontent.com/lexingel/pixellab-game-art/main/claude-code/pixellab-game-art/VERSION'
SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the installed pixellab-game-art folder
HOME = os.path.join(os.path.expanduser('~'), '.pixellab-skill')
MANIFEST = '.install.json'
UA = {'User-Agent': 'pixellab-game-art-skill-updater'}


def vtuple(v):
    return tuple(int(x) for x in re.findall(r'\d+', v or '0'))


def version_of(folder):
    try:
        return open(os.path.join(folder, 'VERSION'), encoding='utf-8').read().strip()
    except OSError:
        return None


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def tree(folder):
    """{relative path: sha256} of every file, skipping caches and the manifest."""
    out = {}
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for f in files:
            if f == MANIFEST or f.endswith('.pyc'):
                continue
            p = os.path.join(root, f)
            out[os.path.relpath(p, folder).replace(os.sep, '/')] = sha(p)
    return out


def manifest():
    try:
        return json.load(open(os.path.join(SKILL, MANIFEST), encoding='utf-8'))
    except (OSError, ValueError):
        return None


def guess_install():
    """For installs made before manifests existed: which package, which installer options, which folder."""
    parent = os.path.dirname(SKILL)
    pkg = 'any-agent' if os.path.isdir(os.path.join(SKILL, 'references', 'tasks')) else 'claude-code'
    home = os.path.expanduser('~')
    if pkg == 'claude-code':
        if os.path.normcase(parent) == os.path.normcase(os.path.join(home, '.claude', 'skills')):
            return pkg, [], home
        return pkg, ['--project'], os.path.dirname(os.path.dirname(parent))
    if os.path.normcase(parent) == os.path.normcase(os.path.join(home, '.agents', 'skills')):
        return pkg, [], home
    if os.path.basename(parent) == 'skills' and os.path.basename(os.path.dirname(parent)) == '.agents':
        return pkg, ['--project'], os.path.dirname(os.path.dirname(parent))
    return pkg, ['--to', parent], home


def latest_version():
    with urllib.request.urlopen(urllib.request.Request(VERSION_URL, headers=UA), timeout=5) as r:
        return r.read().decode('utf-8').strip()


def check(weekly):
    have = version_of(SKILL)
    state_path = os.path.join(HOME, 'update_check.json')
    try:
        state = json.load(open(state_path, encoding='utf-8'))
    except (OSError, ValueError):
        state = {}
    if weekly and (os.environ.get('PIXELLAB_SKILL_NO_UPDATE_CHECK') or time.time() - state.get('checked', 0) < 7 * 86400):
        latest = state.get('latest')   # use last week's answer, no network
    else:
        try:
            latest = latest_version()
        except Exception as e:
            if not weekly:
                print('update  could not check (%s) - offline, or the repository is not public yet' % e)
            latest = None
        os.makedirs(HOME, exist_ok=True)
        json.dump({'checked': time.time(), 'latest': latest or state.get('latest')}, open(state_path, 'w', encoding='utf-8'))
    if latest and vtuple(latest) > vtuple(have):
        print('update  %s is out (you have %s) - say pga-update to get it' % (latest, have))
    elif not weekly and latest:
        print('update  up to date (%s)' % have)


def fetch(src, work):
    """Download/unpack the update; return the folder that holds claude-code/ and any-agent/."""
    if src and os.path.isdir(src):
        return src
    z = os.path.join(work, 'update.zip')
    if src and os.path.isfile(src):
        shutil.copy(src, z)
    else:
        url = src or ZIP_URL
        print('downloading', url)
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r, open(z, 'wb') as f:
            shutil.copyfileobj(r, f)
    out = os.path.join(work, 'unzipped')
    with zipfile.ZipFile(z) as zf:
        for name in zf.namelist():   # refuse paths that would land outside the folder
            if name.startswith(('/', '\\')) or '..' in name.replace('\\', '/').split('/'):
                sys.exit('refusing: the download holds an unsafe path (%s)' % name)
        zf.extractall(out)
    for root, dirs, _ in os.walk(out):
        if 'claude-code' in dirs or 'any-agent' in dirs:
            return root
        if os.path.isfile(os.path.join(root, 'install.py')) and os.path.isdir(os.path.join(root, 'pixellab-game-art')):
            return os.path.dirname(root)   # a single package zip
    sys.exit('the download does not look like the pixellab-game-art repository (no claude-code/ or any-agent/ folder)')


def changelog_since(pkg_dir, old):
    try:
        text = open(os.path.join(pkg_dir, 'CHANGELOG.md'), encoding='utf-8').read()
    except OSError:
        return ''
    keep = []
    for block in re.split(r'(?m)^(?=## )', text):
        m = re.match(r'## (\d+\.\d+\.\d+)', block)
        if m and vtuple(m.group(1)) > vtuple(old):
            keep.append(block.strip())
    return '\n\n'.join(keep)


def backup(old):
    dst = os.path.join(HOME, 'backups', '%s-%s' % (old or 'unknown', time.strftime('%Y%m%d-%H%M%S')))
    parent = os.path.dirname(SKILL)
    names = ['pixellab-game-art'] + sorted(d for d in os.listdir(parent) if d.startswith('pga-') and os.path.isdir(os.path.join(parent, d)))
    for d in names:
        shutil.copytree(os.path.join(parent, d), os.path.join(dst, d), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    json.dump({'parent': parent, 'folders': names}, open(os.path.join(dst, 'backup.json'), 'w', encoding='utf-8'))
    return dst


def rollback():
    root = os.path.join(HOME, 'backups')
    found = sorted(os.listdir(root)) if os.path.isdir(root) else []
    if not found:
        sys.exit('no backup to restore (one is made before every update)')
    src = os.path.join(root, found[-1])
    info = json.load(open(os.path.join(src, 'backup.json'), encoding='utf-8'))
    for d in os.listdir(info['parent']):   # commands the update added
        if d.startswith('pga-') and d not in info['folders'] and os.path.isfile(os.path.join(info['parent'], d, 'SKILL.md')):
            shutil.rmtree(os.path.join(info['parent'], d))
    for d in info['folders']:
        t = os.path.join(info['parent'], d)
        if os.path.exists(t):
            shutil.rmtree(t)
        shutil.copytree(os.path.join(src, d), t)
    shutil.rmtree(src)
    print('restored version %s into %s - restart your assistant' % (version_of(os.path.join(info['parent'], 'pixellab-game-art')), info['parent']))
    # ponytail: subagent files written by install.py --agent stay at the newer version; re-run the old installer if that matters


def update(src, force):
    old = version_of(SKILL)
    m = manifest()
    pkg, iargs, cwd = (m['pkg'], m['args'], m['cwd']) if m else guess_install()
    work = tempfile.mkdtemp(prefix='pga-update-')
    try:
        root = fetch(src, work)
        new_pkg = os.path.join(root, pkg)
        new = version_of(os.path.join(new_pkg, 'pixellab-game-art'))
        if not new:
            sys.exit('the download has no %s/pixellab-game-art/VERSION' % pkg)
        if vtuple(new) <= vtuple(old) and not force:
            print('up to date: you have %s, the download is %s (--force reinstalls)' % (old, new))
            return
        # what the user changed since the last install (needs the manifest that install wrote)
        now = tree(SKILL)
        was = (m or {}).get('files', {})
        upstream = tree(os.path.join(new_pkg, 'pixellab-game-art'))
        edited = [r for r, h in now.items() if r in was and was[r] != h]
        added = [r for r in now if was and r not in was]
        saved = os.path.join(work, 'mine')
        for r in edited + added:
            os.makedirs(os.path.dirname(os.path.join(saved, r)), exist_ok=True)
            shutil.copy(os.path.join(SKILL, r), os.path.join(saved, r))
        bak = backup(old)
        if pkg == 'any-agent' and m and m.get('models'):   # keep the model names the user set for their agent
            mp = os.path.join(new_pkg, 'models.json')
            mj = json.load(open(mp, encoding='utf-8'))
            mj['agents'].update(m['models'])
            json.dump(mj, open(mp, 'w', encoding='utf-8'), indent=2)
        r = subprocess.run([sys.executable, os.path.join(new_pkg, 'install.py')] + iargs, cwd=cwd,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        if r.returncode:
            print(r.stdout)
            sys.exit('the installer failed - nothing was lost: python update.py rollback restores %s' % bak)
        print(r.stdout.split('\n\nLast step')[0].strip())
        merge = []
        for rel in edited + added:
            dst = os.path.join(SKILL, rel)
            if rel in upstream and upstream[rel] != was.get(rel):   # both sides changed (or both added) it
                shutil.copy(dst, dst + '.from-update')
                merge.append(rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(os.path.join(saved, rel), dst)
        print('\nUpdated %s -> %s' % (old, new))
        notes = changelog_since(new_pkg, old)
        if notes:
            print("\nWhat's new:\n" + notes)
        if edited or added:
            print('\nKept your changes: %d file(s)' % len(edited + added))
        for rel in merge:
            print('MERGE  %s  (yours) + %s.from-update  (the update) -> merge into %s, then delete the .from-update file' % (rel, rel, rel))
        if not m:
            print('(first update of an older install: files you edited could not be told apart - the backup has them)')
        print('Backup: %s  (undo: python update.py rollback)' % bak)
        print('Restart your assistant so new or changed commands load.')
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '-h' in a or '--help' in a:
        sys.exit(__doc__)
    if a[:1] == ['check']:
        check('--weekly' in a)
    elif a[:1] == ['rollback']:
        rollback()
    else:
        src = a[a.index('--from') + 1] if '--from' in a and a.index('--from') + 1 < len(a) else None
        update(src, '--force' in a)
