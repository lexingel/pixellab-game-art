"""cost_report.py [log.jsonl] - generations spent, from the job log fetch.py writes
(default pixellab_out/log.jsonl): totals per command, per tool and per day, plus failed jobs.

  python cost_report.py pixellab_out/log.jsonl
"""
import collections
import json
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if sys.argv[1:2] in (['-h'], ['--help']):
    sys.exit(__doc__)

path = sys.argv[1] if len(sys.argv) > 1 else 'pixellab_out/log.jsonl'
by = {k: collections.Counter() for k in ('cmd', 'tool', 'day')}
n = failed = 0
total = 0.0
seen = set()   # one count per job id: a job logged twice (re-run) is spent once
for line in open(path, encoding='utf-8-sig'):
    if not line.strip():
        continue
    try:
        r = json.loads(line)
    except ValueError:
        continue
    if not isinstance(r, dict) or 'outcome' in r:   # outcome.py lines record a verdict, not a spend
        continue
    if r.get('job'):
        if r['job'] in seen:
            continue
        seen.add(r['job'])
    n += 1
    if r.get('status') == 'failed':
        failed += 1
        continue
    c = float(r.get('cost') or 0)
    total += c
    by['cmd'][r.get('cmd', '?')] += c
    by['tool'][r.get('tool', '?')] += c
    by['day'][str(r.get('time', '?'))[:10]] += c
print('%d jobs, %d failed (refunded), %.1f generations' % (n, failed, total))
for k, title in (('cmd', 'by command'), ('tool', 'by tool'), ('day', 'by day')):
    print('\n' + title)
    for name, c in by[k].most_common():
        print('  %-28s %7.1f' % (name, c))
