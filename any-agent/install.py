"""Install the PixelLab game-art agent skill (Codex, Gemini CLI, Cursor, Copilot, Claude Code, ...).

    python install.py                  # all your projects: ~/.agents/skills (the shared Agent Skills folder)
    python install.py --project        # only the project in the current folder: ./.agents/skills + AGENTS.md
    python install.py --to <folder>    # your agent's own skills folder, if it doesn't read .agents/skills
    python install.py --pip            # also install the Python packages (pillow numpy scipy)
    python install.py --agent codex    # also add one subagent per task, each on the model set for it in
                                       # models.json: codex · gemini · cursor · opencode · copilot · claude
                                       # (cheap model for text-only tasks; add --project for this project only)
    python install.py --uninstall      # remove what this installer installed: the pixellab-game-art folder,
                                       # with --project the AGENTS.md section, with --agent X that agent's
                                       # pga-* subagent files (same --project / --to as when you installed)

Run it from the unzipped folder (on macOS/Linux: python3 install.py). Running it again updates an
older install. Python 3.8+, no packages needed to run it. Your pixellab.json and anything you
generated are never touched.
"""
import hashlib
import json
import os
import re
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

AGENT_DIRS = {   # (user-level, project-level) subagent folders
    'codex': ('~/.codex/agents', '.codex/agents'),
    'gemini': ('~/.gemini/agents', '.gemini/agents'),
    'cursor': ('~/.cursor/agents', '.cursor/agents'),
    'opencode': ('~/.config/opencode/agents', '.opencode/agents'),
    'copilot': (None, '.github/agents'),
    'claude': ('~/.claude/agents', '.claude/agents'),
}
USAGE = 'Usage: python install.py [--project] [--to <folder>] [--pip] [--agent %s] [--uninstall]  (see --help)' % '|'.join(AGENT_DIRS)


def value_of(flag):
    """The word after a flag, or a clear usage error."""
    i = args.index(flag)
    if i + 1 >= len(args) or args[i + 1].startswith('-'):
        sys.exit('%s needs a value.\n%s' % (flag, USAGE))
    return args[i + 1]


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


def agents_note():
    """The AGENTS.md section --project adds, exactly as written."""
    note = open(os.path.join(here, 'AGENTS.md'), encoding='utf-8').read()
    return note.replace('`pixellab-game-art/', '`.agents/skills/pixellab-game-art/').replace('This folder contains', 'This project has')


def agent_dir(agent):
    user_dir, proj_dir = AGENT_DIRS[agent]
    return os.path.join(os.getcwd(), proj_dir) if ('--project' in args or not user_dir) else os.path.expanduser(user_dir)


def subagents(agent, skill_dir):
    with open(os.path.join(here, 'models.json'), encoding='utf-8') as f:
        m = json.load(f)
    d = agent_dir(agent)
    os.makedirs(d, exist_ok=True)
    skill = skill_dir.replace(os.sep, '/')
    picks = []
    for task, tier in m['tiers'].items():
        if task in m.get('main_only', []):
            for ext in ('.toml', '.md', '.agent.md'):   # an older install may have made one: remove it
                old = os.path.join(d, task + ext)
                if os.path.isfile(old):
                    os.remove(old)
            continue   # asks the user questions: the main agent runs it
        pick = m['agents'][agent][tier]
        desc = 'pixellab-game-art task %s: %s' % (task, m['descriptions'][task])
        body = ('You run the `%s` task of the pixellab-game-art skill (skill folder: %s).\n'
                'Read %s/references/tasks/%s.md, then %s/references/prompt_improver.md, and follow them for the request '
                'you were given. Run scripts as `python %s/scripts/<name>.py`. Print every PixelLab call with its '
                'parameters and cost before submitting, never ask for permission, never repeat a call, and end with the '
                'results table. If the job cannot run without an answer from the user (e.g. no sprite given), stop and '
                'return that one question to the main agent instead of guessing.\n' % (task, skill, skill, task, skill, skill))
        if agent == 'codex':
            model, effort = pick.get('model', ''), pick.get('effort', '')
            text = 'name = %s\ndescription = %s\n' % (json.dumps(task), json.dumps(desc))
            text += ('model = %s\n' % json.dumps(model)) if model else ''
            text += ('model_reasoning_effort = %s\n' % json.dumps(effort)) if effort else ''
            text += 'developer_instructions = """\n%s"""\n' % body
            path = os.path.join(d, task + '.toml')
            picks.append('%s %s/%s' % (task, model or 'inherit', effort or '-'))
        else:
            fm = ['---']
            if agent != 'opencode':
                fm.append('name: ' + task)
            fm.append('description: ' + json.dumps(desc))
            if agent == 'opencode':
                fm.append('mode: subagent')
            if pick and pick != 'inherit':
                fm.append('model: ' + pick)
            elif agent in ('claude', 'gemini', 'cursor'):
                fm.append('model: inherit')
            fm.append('---')
            text = '\n'.join(fm) + '\n\n' + body
            path = os.path.join(d, task + ('.agent.md' if agent == 'copilot' else '.md'))
            picks.append('%s %s' % (task, pick or 'inherit'))
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
    print('Added %d %s subagents in %s' % (len(m['tiers']), agent, d))
    print('  models: ' + ' | '.join(picks))
    print('  change them in models.json and run this again (empty = your current model)')


def uninstall(target, agent):
    removed = []
    if os.path.isdir(target):
        shutil.rmtree(target)
        removed.append('folder ' + target)
    if '--project' in args:
        path = os.path.join(os.getcwd(), 'AGENTS.md')
        if os.path.isfile(path):
            with open(path, encoding='utf-8', newline='') as f:
                raw = f.read()
            text, note = raw.replace('\r\n', '\n'), agents_note()
            nl = '\r\n' if '\r\n' in raw else '\n'
            if text.strip() == note.strip():   # the installer wrote the whole file
                os.remove(path)
                removed.append('AGENTS.md (it only held the PixelLab section)')
            elif note.strip() in text:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(text.replace('\n\n' + note, '', 1).replace(note, '', 1).rstrip('\n').replace('\n', nl) + nl)
                removed.append('the PixelLab section of ' + path)
            elif 'pixellab-game-art' in text:
                print('AGENTS.md mentions pixellab-game-art but not as this installer wrote it - remove that section by hand.')
    if agent:
        d = agent_dir(agent)
        for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if re.match(r'^pga-[a-z0-9-]+(\.agent)?\.(md|toml)$', name):
                os.remove(os.path.join(d, name))
                removed.append('subagent ' + os.path.join(d, name))
    print('Removed:\n  ' + '\n  '.join(removed) if removed else 'Nothing to remove (already uninstalled in this scope).')
    print('Kept: pixellab.json, your generated files, and the PixelLab connection in your agent settings.')


for flag in ('--to', '--agent'):
    if flag in args:
        value_of(flag)   # fails early with a usage error
agent = value_of('--agent') if '--agent' in args else None
if agent and agent not in AGENT_DIRS:
    sys.exit('--agent must be one of: ' + ', '.join(AGENT_DIRS))

if '--to' in args:
    dest = os.path.abspath(os.path.expanduser(value_of('--to')))
elif '--project' in args:
    dest = os.path.join(os.getcwd(), '.agents', 'skills')
else:
    dest = os.path.join(os.path.expanduser('~'), '.agents', 'skills')
target = os.path.join(dest, 'pixellab-game-art')
source = os.path.join(here, 'pixellab-game-art')

if '--to' in args and os.path.isdir(os.path.join(dest, 'pga-help')):
    sys.exit('Refusing: %s holds the Claude Code version of this skill (a pga-help folder next to pixellab-game-art).\n'
             'Update or remove that one with the Claude Code package\'s own install.py; this installer is for other agents.' % dest)
if inside(target, source) or inside(source, target):   # same folder, or one inside the other: rmtree would delete the source
    sys.exit('Refusing: the install folder (%s) is the same as, or inside, the folder this installer runs from (%s).\n'
             'Re-installing would delete the files it copies from. Run install.py from the unzipped download, '
             'not from the destination.' % (dest, here))

if '--uninstall' in args:
    uninstall(target, agent)
    sys.exit(0)

def version_of(folder):
    try:
        return open(os.path.join(folder, 'VERSION'), encoding='utf-8').read().strip()
    except OSError:
        return None


os.makedirs(dest, exist_ok=True)
old_v, new_v = version_of(target), version_of(source)
if os.path.exists(target):
    shutil.rmtree(target)
shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
files = {}   # what was installed - scripts/update.py uses it to keep files you edit
for root, dirs, names in os.walk(target):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for n in names:
        p = os.path.join(root, n)
        with open(p, 'rb') as f:
            files[os.path.relpath(p, target).replace(os.sep, '/')] = hashlib.sha256(f.read()).hexdigest()
iargs = ['--project'] if '--project' in args else []
if '--to' in args:
    iargs += ['--to', dest]
if agent:
    iargs += ['--agent', agent]
with open(os.path.join(here, 'models.json'), encoding='utf-8') as f:
    picks = {agent: json.load(f)['agents'].get(agent)} if agent else {}
with open(os.path.join(target, '.install.json'), 'w', encoding='utf-8') as f:
    json.dump({'version': new_v, 'pkg': 'any-agent', 'args': iargs, 'cwd': os.getcwd(), 'models': picks, 'files': files}, f, indent=1)
was ='' if old_v is None else (' (was %s)' % old_v if old_v != new_v else ' (same version, refreshed)')
print('Installed pixellab-game-art %s into %s%s' % (new_v or '', dest, was))
py = python_name()
print('Run the skill\'s scripts with: %s   (e.g. %s %s)' % (py, py, os.path.join(target, 'scripts', 'check_setup.py')))
if '--project' in args:
    agents = os.path.join(os.getcwd(), 'AGENTS.md')
    note = agents_note()
    if os.path.exists(agents):
        if 'pixellab-game-art' not in open(agents, encoding='utf-8').read():
            with open(agents, 'a', encoding='utf-8') as f:
                f.write('\n\n' + note)
            print('Added the PixelLab section to your AGENTS.md')
    else:
        with open(agents, 'w', encoding='utf-8') as f:
            f.write(note)
        print('Wrote AGENTS.md (for agents that read it instead of skills)')

if agent:
    subagents(agent, target)

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
Last step - connect PixelLab to your agent (once):
  1. Get your API token: https://api.pixellab.ai/mcp (sign in to PixelLab)
  2. Save it as an environment variable PIXELLAB_TOKEN, then add the server with the line for your
     agent in README.md -> "Connect PixelLab" (Codex, Gemini CLI, Cursor, VS Code/Copilot, OpenCode,
     Claude Code). By hand: MCP server "pixellab", URL https://api.pixellab.ai/mcp, HTTP transport,
     header  Authorization: Bearer <token>
  3. Restart the agent in your game's folder and ask it: pga-doctor (checks everything, prints any fix)
If your agent doesn't find the skill, it uses its own skills folder - check its docs and run:
  python install.py --to <that folder>
""")
