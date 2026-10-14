"""outcome.py - record how a generated job turned out, next to its line in log.jsonl. Stdlib only.

  python outcome.py <log.jsonl> <job_id> --verdict keep|reroll|reject|reused|failed
                    [--qa "flag1;flag2"] [--reason "gun in the wrong hand"] [--est 9] [--seconds 410]
                    [--style '{"setting":"cozy","density":"mid"}']

Appends {"job": id, "outcome": {...}} to the same log. This stays on the user's machine; it is
what the skill learns from, and what share.py sends only if the user opted in.
Call it once per job after QA and the visual check, and again if the user reacts ("bad: …" →
--verdict reject --reason "…"); the latest outcome for a job wins.
"""
import argparse
import datetime
import json

ap = argparse.ArgumentParser()
ap.add_argument('log')
ap.add_argument('job')
ap.add_argument('--verdict', required=True, choices=['keep', 'reroll', 'reject', 'reused', 'failed'])
ap.add_argument('--qa', default='')
ap.add_argument('--reason', default='')
ap.add_argument('--est', type=float)
ap.add_argument('--seconds', type=float)
ap.add_argument('--style', default='')
a = ap.parse_args()
o = {'verdict': a.verdict, 'qa': [q.strip() for q in a.qa.split(';') if q.strip()]}
if a.reason:
    o['reason'] = a.reason
if a.est is not None:
    o['est_cost'] = a.est
if a.seconds is not None:
    o['seconds'] = a.seconds
if a.style:
    o['style'] = json.loads(a.style)
with open(a.log, 'a', encoding='utf-8') as f:
    f.write(json.dumps({'time': datetime.datetime.now().isoformat(timespec='seconds'), 'job': a.job, 'outcome': o},
                       ensure_ascii=False) + '\n')
print('outcome', a.job, a.verdict)
