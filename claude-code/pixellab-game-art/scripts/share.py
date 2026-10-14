"""share.py - opt-in sharing of generation outcomes with the skill's authors. Stdlib only.

  python share.py status                      # this project's level + this machine's install id
  python share.py set off|stats|prompts       # the user's choice (asked at setup); default off
  python share.py send --log <log.jsonl> [--agent NAME] [--preview]
                                              # send what's new or changed since the opt-in (nothing at "off");
                                              # --preview prints it instead of sending
  python share.py forget                      # delete everything this machine sent, start a new id, sharing off
Options: --profile <path> (default ./pixellab.json).
Environment: PIXELLAB_SKILL_NO_TELEMETRY=1 never sends anything; PIXELLAB_SKILL_FEEDBACK_URL overrides the server.

Levels:
  off      nothing leaves this machine (default)
  stats    task, tool, numeric/enum parameters, style summary (setting, density, view, outline,
           shading, colours), cost vs estimate, seconds waited, status, QA flags, keep/reroll/reject
  prompts  stats + the prompt text and the user's reason for a verdict - prompts may contain names
           you typed (characters, places); don't pick it for secret projects
Never sent at any level: the PixelLab token, file paths, URLs, uploads, images, the game's name, job ids
(each job is sent as a one-way hash so a changed verdict replaces its earlier record).
Only jobs logged after you opted in are sent. The install id is random and per machine
(~/.pixellab-skill/id.json); "forget" deletes its records on the server and makes a new one.
"""
import datetime
import hashlib
import json
import os
import sys
import urllib.request
import uuid

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ENDPOINT = os.environ.get('PIXELLAB_SKILL_FEEDBACK_URL', 'https://pixellab-skill-feedback.lexingel.workers.dev')
try:
    SKILL_VERSION = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'VERSION'), encoding='utf-8').read().strip()
except OSError:
    SKILL_VERSION = 'unknown'
CHUNK, MAX_BYTES = 50, 48 * 1024
PARAM_KEYS = ['width', 'height', 'seed', 'frame_count', 'n_frames', 'no_background', 'mode', 'view',
              'outline', 'shading', 'detail', 'direction', 'n_directions', 'size', 'max_colors',
              'text_guidance_scale', 'use_color_palette_correction']
STYLE_KEYS = ['setting', 'density', 'view', 'outline', 'shading', 'colors', 'dither', 'light']
ID_FILE = os.path.join(os.path.expanduser('~'), '.pixellab-skill', 'id.json')

args = sys.argv[1:]
if not args or args[0] in ('-h', '--help'):
    sys.exit(__doc__)


def opt(name, default=None):
    if name not in args:
        return default
    i = args.index(name)
    if i + 1 >= len(args):
        sys.exit('%s needs a value' % name)
    return args[i + 1]


path = opt('--profile', 'pixellab.json')
prof = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
share = prof.get('share') or {}
level = share.get('level', 'off')


def save():
    share.pop('install_id', None)   # the id lives per machine now (older profiles kept it here)
    prof['share'] = share
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(prof, f, indent=2, ensure_ascii=False)
        f.write('\n')


def machine_id(create):
    if os.path.exists(ID_FILE):
        return json.load(open(ID_FILE, encoding='utf-8')).get('install_id')
    if (prof.get('share') or {}).get('install_id'):   # migrate an older per-project id
        iid = prof['share']['install_id']
    elif create:
        iid = str(uuid.uuid4())
    else:
        return None
    os.makedirs(os.path.dirname(ID_FILE), exist_ok=True)
    json.dump({'install_id': iid}, open(ID_FILE, 'w', encoding='utf-8'))
    return iid


def post(route, body):
    req = urllib.request.Request(ENDPOINT + route, data=json.dumps(body).encode('utf-8'), method='POST',
                                 headers={'content-type': 'application/json',
                                          'user-agent': 'pixellab-game-art-skill/' + SKILL_VERSION})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf-8'))


def clean(d, keys):
    out = {}
    for k in keys:
        v = (d or {}).get(k)
        if isinstance(v, (bool, int, float)) or (isinstance(v, str) and len(v) <= 24 and not any(c in v for c in '/\\:')):
            out[k] = v
    return out


def ref_of(job):
    return hashlib.sha256(job.encode('utf-8')).hexdigest()[:16]


def records(log_path, sent, since):
    jobs, outcomes = {}, {}
    for line in open(log_path, encoding='utf-8'):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if 'outcome' in r:
            outcomes[r.get('job')] = r['outcome']
        elif r.get('job') and r['job'] not in jobs:
            jobs[r['job']] = r
    style_now = (prof.get('styles') or {}).get(prof.get('active_style') or '', {})
    out = []
    for job, r in jobs.items():
        if since and str(r.get('time', '')) < since:
            continue                                   # logged before the opt-in
        o = outcomes.get(job, {})
        sig = hashlib.sha256(json.dumps([o, level], sort_keys=True).encode('utf-8')).hexdigest()[:12]
        if sent.get(job) == sig:
            continue                                   # already sent, nothing changed
        params = r.get('params') or {}
        p = clean(params, PARAM_KEYS)
        p.update({'has_style_image': any(k.startswith('style_image') for k in params),
                  'has_reference': any('reference' in k for k in params),
                  'has_first_frame': 'first_frame_url' in params, 'has_last_frame': 'last_frame_url' in params})
        rec = {'ref': ref_of(job), 'task': r.get('cmd'), 'tool': r.get('tool'), 'params': p,
               'style': clean(o.get('style') or style_now, STYLE_KEYS),
               'cost': r.get('cost'), 'est_cost': o.get('est_cost'), 'seconds': o.get('seconds', r.get('waited_s')),
               'status': r.get('status', 'ok'), 'qa': o.get('qa', []), 'verdict': o.get('verdict', 'unknown')}
        if level == 'prompts':
            rec['prompt'] = (r.get('prompt') or '')[:800]
            rec['reason'] = (o.get('reason') or '')[:200]
        out.append((job, sig, rec))
    return out


def chunks(items, body_base):
    batch = []
    for it in items:
        trial = batch + [it]
        size = len(json.dumps(dict(body_base, records=[x[2] for x in trial])).encode('utf-8'))
        if batch and (len(trial) > CHUNK or size > MAX_BYTES):
            yield batch
            batch = [it]
        else:
            batch = trial
    if batch:
        yield batch


cmd = args[0]
if cmd == 'status':
    iid = machine_id(False)
    off_env = os.environ.get('PIXELLAB_SKILL_NO_TELEMETRY') == '1'
    print('sharing: %s%s%s' % (level, ' (since %s)' % share.get('since') if level != 'off' and share.get('since') else '',
                               ' - disabled by PIXELLAB_SKILL_NO_TELEMETRY' if off_env else ''))
    print('install id: %s' % (iid or 'none yet'))
elif cmd == 'set':
    if len(args) < 2 or args[1] not in ('off', 'stats', 'prompts'):
        sys.exit('usage: share.py set off|stats|prompts')
    new = args[1]
    if new != 'off' and level == 'off':
        share['since'] = datetime.datetime.now().isoformat(timespec='seconds')
        machine_id(True)
    share['level'] = new
    save()
    print('sharing: %s' % new)
elif cmd == 'send':
    log_path = opt('--log')
    if not log_path or not os.path.exists(log_path):
        sys.exit('no log: give --log <out>/log.jsonl')
    if os.environ.get('PIXELLAB_SKILL_NO_TELEMETRY') == '1' and '--preview' not in args:
        print('Shared: nothing (PIXELLAB_SKILL_NO_TELEMETRY=1)')
        sys.exit(0)
    if level == 'off' and '--preview' not in args:
        print('Shared: nothing (sharing is off)')
        sys.exit(0)
    sent_path = log_path + '.shared'
    sent = {}
    if os.path.exists(sent_path):
        for line in open(sent_path, encoding='utf-8'):
            parts = line.split()
            if len(parts) == 2:
                sent[parts[0]] = parts[1]
    items = records(log_path, sent, share.get('since', ''))
    base = {'install': machine_id(False) or '<made when you opt in>', 'level': level if level != 'off' else 'stats',
            'skill_version': SKILL_VERSION, 'agent': opt('--agent', 'unknown'), 'tier': prof.get('tier')}
    if '--preview' in args:
        print(json.dumps(dict(base, records=[x[2] for x in items]), indent=2, ensure_ascii=False))
        print('(preview only - %d record(s), nothing sent)' % len(items))
        sys.exit(0)
    if not items:
        print('Shared: nothing new')
        sys.exit(0)
    done = 0
    for batch in chunks(items, base):
        try:
            r = post('/v1/records', dict(base, records=[x[2] for x in batch]))
        except Exception as e:
            print('Shared: %d record(s); the rest not sent (%s) - retried next run' % (done, e.__class__.__name__))
            sys.exit(0)
        stored = set(r.get('refs') or [])
        with open(sent_path, 'a', encoding='utf-8') as f:
            for job, sig, rec in batch:
                if rec['ref'] in stored:
                    f.write('%s %s\n' % (job, sig))
                    done += 1
    print('Shared: %d record(s) (%s)' % (done, level))
elif cmd == 'forget':
    iid = machine_id(False)
    if not iid:
        sys.exit('nothing was ever shared from this machine')
    try:
        r = post('/v1/forget', {'install': iid})
    except Exception as e:
        sys.exit('could not reach the server (%s) - try again later' % e.__class__.__name__)
    if os.path.exists(ID_FILE):
        os.remove(ID_FILE)
    share['level'] = 'off'
    share.pop('since', None)
    save()
    print('deleted %s record(s) on the server; sharing is off; a new id is made if you opt in again' % r.get('deleted', 0))
else:
    sys.exit(__doc__)
