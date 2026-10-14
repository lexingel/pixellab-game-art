"""history.py - past generations from the job log, newest first. Stdlib only.

  python history.py [log.jsonl] [--n 15] [--cmd pga-char] [--find <text>] [--json]

Default log: pixellab_out/log.jsonl. One line per job: when, command, tool, cost, verdict, name,
files, job id. --find matches the prompt, name or file path; --json prints the full records (for a
re-roll: tool, prompt, params, seed). Ends with the total spent in the listed jobs.
"""
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

args = sys.argv[1:]
if args[:1] in (['-h'], ['--help']):
    sys.exit(__doc__)


def opt(name, default=None):
    if name in args:
        i = args.index(name)
        if i + 1 >= len(args):
            sys.exit('%s needs a value' % name)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return default


n = int(opt('--n', '15'))
only_cmd = opt('--cmd')
find = (opt('--find') or '').lower()
as_json = '--json' in args
if as_json:
    args.remove('--json')
path = args[0] if args else os.path.join('pixellab_out', 'log.jsonl')
if not os.path.exists(path):
    sys.exit('no log at %s - nothing generated here yet (or pass the log path)' % path)

jobs, outcomes, order = {}, {}, []
for line in open(path, encoding='utf-8-sig'):
    try:
        r = json.loads(line)
    except ValueError:
        continue
    if not isinstance(r, dict) or not r.get('job'):
        continue
    if 'outcome' in r:
        outcomes[r['job']] = r['outcome']
    elif r['job'] not in jobs:
        jobs[r['job']] = r
        order.append(r['job'])

rows = []
for job in reversed(order):
    r = jobs[job]
    if only_cmd and r.get('cmd') != only_cmd:
        continue
    hay = ' '.join(str(r.get(k, '')) for k in ('prompt', 'name', 'out')).lower()
    if find and find not in hay:
        continue
    r = dict(r, outcome=outcomes.get(job, {}))
    rows.append(r)
    if len(rows) >= n:
        break

if as_json:
    print(json.dumps(rows, indent=2, ensure_ascii=False))
    sys.exit(0)
if not rows:
    print('no matching jobs')
    sys.exit(0)
total = 0.0
for r in rows:
    cost = r.get('cost') or 0
    total += float(cost) if r.get('status', 'ok') != 'failed' else 0
    print('%-19s %-12s %-24s %5s  %-7s %-18s %s  [%s]' % (
        str(r.get('time', ''))[:19], r.get('cmd') or '?', (r.get('tool') or '?')[:24],
        'refnd' if r.get('status') == 'failed' else cost, r['outcome'].get('verdict', '-'),
        (r.get('name') or '')[:18], r.get('out', ''), str(r['job'])[:8]))
print('%d job(s), %.0f generations' % (len(rows), total))
