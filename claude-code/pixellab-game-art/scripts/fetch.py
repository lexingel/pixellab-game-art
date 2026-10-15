"""fetch.py - wait for PixelLab image/animation jobs, download them, log them. Stdlib only.

One job:
  python fetch.py <job_id> <out.png>                        # a single image
  python fetch.py <job_id> <out_dir> --frames 7             # an animation: <out_dir>/0.png .. 6.png
  python fetch.py <tileset_id> <out.png> --tileset          # a top-down tileset: the sheet + <out>.json metadata
Many jobs at once (a batch - polled together, so total wait = the slowest job):
  python fetch.py --jobs jobs.txt --out <dir>               # lines: "<name> <job_id> [frames|tileset]"
Logging (one JSON line per finished job, for re-rolls and cost reports - see cost_report.py):
  --log pixellab_out/log.jsonl --meta-file meta.json        # meta.json = {"cmd":"pga-char","tool":"create_image_pixflux","prompt":"...","params":{...},"cost":1}
  --log pixellab_out/log.jsonl --meta -                     # same JSON read from stdin (a heredoc / pipe)
  --log pixellab_out/log.jsonl --meta '{"cmd":"pga-char","cost":1}'   # inline: fine in bash, breaks in PowerShell and on apostrophes - prefer --meta-file
  (with --jobs, put per-job meta as a JSON object at the end of each line instead)
Each logged line also gets "waited_s": seconds this run waited for that job. A job id that is already
in --log (any line that is not an "outcome" line) is not logged again, so re-running is safe.
Options: --timeout 100 (seconds; keep it under your shell tool's own limit, usually 120 s), --every 15 (poll interval).
Exit 0 = all downloaded; 2 = some failed (PixelLab refunds failed jobs - resubmit); 3 = timed out:
the TIMEOUT lines list the jobs still running - run the SAME command again, nothing is lost or double-logged.
HTTP 404 counts as "still waiting" during the first 60 s of a run (a just-submitted job can 404 briefly);
a 404 after that, and a 410 at any time, = failed.
python fetch.py --selftest runs offline checks (no network).
Download URLs need no auth (the job id is the key).
"""
import argparse
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.request
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE = 'https://api.pixellab.ai/mcp/images/%s/download'
GRACE_404 = 60    # seconds after the script started during which a 404 still means "not registered yet"


def get(job, index=None):
    """('ok', bytes) | ('wait', None) | ('notfound', None) for a 404 | ('failed', None) for a 410."""
    url = BASE % job + ('?index=%d' % index if index is not None else '')
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read()
            return ('ok', data) if data[:4] == b'\x89PNG' or data[:3] == b'GIF' else ('wait', None)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return ('notfound', None)
        return ('failed', None) if e.code == 410 else ('wait', None)   # 423/425/5xx: still working
    except Exception:
        return ('wait', None)


def try_tileset(tid, out):
    """Top-down tileset: sheet PNG + metadata JSON (both answer 423 while generating)."""
    base = 'https://api.pixellab.ai/mcp/tilesets/%s/' % tid
    try:
        with urllib.request.urlopen(base + 'image?inline=true', timeout=30) as r:
            png = r.read()
        with urllib.request.urlopen(base + 'metadata', timeout=30) as r:
            meta = r.read()
    except urllib.error.HTTPError as e:
        return 'notfound' if e.code == 404 else 'failed' if e.code == 410 else 'wait'
    except Exception:
        return 'wait'
    if png[:4] != b'\x89PNG':
        return 'wait'
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'wb') as f:
        f.write(png)
    with open(os.path.splitext(out)[0] + '.json', 'wb') as f:
        f.write(meta)
    return 'ok'


def try_job(job, out, frames):
    """Returns 'ok', 'wait', 'notfound' or 'failed'; writes files when ok. frames -1 = a tileset."""
    if frames == -1:
        return try_tileset(job, out)
    if not frames:
        st, data = get(job)
        if st == 'ok':
            os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
            with open(out, 'wb') as f:
                f.write(data)
        return st
    got = []
    for i in range(frames):
        st, data = get(job, i)
        if st != 'ok':
            return st
        got.append(data)
    os.makedirs(out, exist_ok=True)
    for i, d in enumerate(got):
        with open(os.path.join(out, '%d.png' % i), 'wb') as f:
            f.write(d)
    return 'ok'


def settle(st, elapsed):
    """404 is 'still waiting' for the first GRACE_404 seconds of the run, a real failure after that."""
    if st == 'notfound':
        return 'wait' if elapsed < GRACE_404 else 'failed'
    return st


def logged_jobs(path):
    """Job ids already in the log (outcome lines from outcome.py don't count)."""
    seen = set()
    if path and os.path.exists(path):
        with open(path, encoding='utf-8-sig') as f:
            for line in f:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                if isinstance(r, dict) and 'outcome' not in r and r.get('job'):
                    seen.add(r['job'])
    return seen


def log(path, job, out, meta, seen):
    """Appends one line unless this job id is already logged. Returns True when it wrote."""
    if not path or job in seen:
        return False
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    rec = {'time': datetime.datetime.now().isoformat(timespec='seconds'), 'job': job, 'out': out}
    rec.update(meta or {})
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    seen.add(job)
    return True


def read_json(text, what):
    meta = json.loads(text.lstrip('﻿').strip() or '{}')
    if not isinstance(meta, dict):
        raise ValueError('%s must be a JSON object' % what)
    return meta


def load_meta(a):
    """--meta-file <path|-> wins over --meta <json|->; '-' reads stdin."""
    try:
        if a.meta_file and a.meta_file != '-':
            with open(a.meta_file, encoding='utf-8-sig') as f:
                return read_json(f.read(), a.meta_file)
        if a.meta_file == '-' or a.meta == '-':
            return read_json(sys.stdin.buffer.read().decode('utf-8-sig'), 'stdin')
        return read_json(a.meta, '--meta')
    except (ValueError, OSError) as e:
        sys.exit('fetch.py: cannot read the meta JSON (%s). On Windows use --meta-file meta.json or --meta - (stdin).' % e)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('job', nargs='?')
    ap.add_argument('out', nargs='?')
    ap.add_argument('--frames', type=int, default=0)
    ap.add_argument('--tileset', action='store_true', help='the id is a top-down tileset (create_topdown_tileset)')
    ap.add_argument('--jobs')
    ap.add_argument('--out', dest='outdir', help='with --jobs: where to save (default: next to the jobs file)')
    ap.add_argument('--log')
    ap.add_argument('--meta', default='{}', help="inline JSON, or '-' to read it from stdin")
    ap.add_argument('--meta-file', help="path to a JSON file with the meta (safe on Windows); '-' = stdin")
    ap.add_argument('--timeout', type=int, default=100, help='seconds (default 100: under the usual 120 s shell-tool limit)')
    ap.add_argument('--every', type=int, default=15)
    ap.add_argument('--selftest', action='store_true', help='offline checks, no network')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    todo = []   # (name, job, out, frames, meta)
    if a.jobs:
        base = a.outdir or os.path.dirname(os.path.abspath(a.jobs))
        with open(a.jobs, encoding='utf-8-sig') as f:
            lines = f.read().splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            meta = {}
            if '{' in line:
                line, js = line.split('{', 1)
                meta = json.loads('{' + js)
            p = line.split()
            fr = (-1 if p[2] == 'tileset' else int(p[2])) if len(p) > 2 else 0   # "<name> <id> tileset"
            todo.append((p[0], p[1], os.path.join(base, p[0] if fr > 0 else p[0] + '.png'), fr, meta))
    else:
        if not (a.job and a.out):
            ap.error('give <job_id> <out> or --jobs file')
        todo.append((os.path.basename(a.out), a.job, a.out, -1 if a.tileset else a.frames, load_meta(a)))
    started = time.time()
    end = started + a.timeout
    seen = logged_jobs(a.log)
    failed = []
    while True:
        left = []
        for t in todo:
            waited = int(round(time.time() - started))
            st = settle(try_job(t[1], t[2], t[3]), time.time() - started)
            if st == 'ok':
                print('OK', t[0], t[2])
                if not log(a.log, t[1], t[2], dict(t[4], name=t[0], waited_s=waited), seen) and a.log:
                    print('  (already in the log - not counted twice)')
            elif st == 'failed':
                print('FAILED', t[0], t[1], '(refunded by PixelLab - resubmit)')
                log(a.log, t[1], t[2], dict(t[4], name=t[0], status='failed', cost=0, waited_s=waited), seen)
                failed.append(t)
            else:
                left.append(t)
        todo = left
        if not todo or time.time() >= end:
            break
        time.sleep(max(0, min(a.every, end - time.time())))
    for t in todo:
        print('TIMEOUT %s %s - still running at PixelLab, run the same command again' % (t[0], t[1]))
    sys.exit(3 if todo else 2 if failed else 0)


def selftest():
    import contextlib
    import io
    import tempfile
    assert settle('notfound', 5) == 'wait' and settle('notfound', 181) == 'failed'
    assert settle('failed', 5) == 'failed' and settle('ok', 999) == 'ok' and settle('wait', 999) == 'wait'
    tmp = tempfile.mkdtemp()
    logp = os.path.join(tmp, 'sub', 'log.jsonl')
    os.makedirs(os.path.dirname(logp))
    with open(logp, 'w', encoding='utf-8') as f:
        f.write(json.dumps({'job': 'aaa', 'cost': 1}) + '\n')
        f.write(json.dumps({'job': 'bbb', 'outcome': 'kept'}) + '\n')   # outcome lines never count as logged
        f.write('not json\n')
    assert logged_jobs(logp) == {'aaa'}, logged_jobs(logp)
    script = {'aaa': 'ok', 'bbb': 'ok', 'ccc': 'wait', 'ddd': 'failed'}
    real_try = globals()['try_job']
    globals()['try_job'] = lambda job, out, frames: script[job]

    def run(*extra):
        buf = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(buf):
            try:
                main(['--log', logp, '--timeout', '0', '--every', '0'] + list(extra))
            except SystemExit as e:
                code = e.code
        return code, buf.getvalue()
    try:
        code, out = run('aaa', os.path.join(tmp, 'a.png'))   # already logged -> no new line
        assert code == 0 and 'not counted twice' in out, out
        code, out = run('bbb', os.path.join(tmp, 'b.png'), '--meta', '{"cost": 2}')   # only an outcome line -> logged
        assert code == 0 and 'not counted twice' not in out, out
        code, out = run('bbb', os.path.join(tmp, 'b.png'), '--meta', '{"cost": 2}')   # re-run -> not again
        assert 'not counted twice' in out, out
        code, out = run('ccc', os.path.join(tmp, 'c.png'))
        assert code == 3 and 'TIMEOUT c.png ccc - still running at PixelLab, run the same command again' in out, out
        code, out = run('ddd', os.path.join(tmp, 'd.png'))
        assert code == 2 and 'FAILED' in out, out
        with open(logp, encoding='utf-8') as f:
            recs = [json.loads(x) for x in f if x.startswith('{')]
        assert [r['job'] for r in recs] == ['aaa', 'bbb', 'bbb', 'ddd'], recs
        assert recs[2]['cost'] == 2 and recs[2]['waited_s'] >= 0 and recs[3]['status'] == 'failed'
        mf = os.path.join(tmp, 'm.json')
        with open(mf, 'w', encoding='utf-8-sig') as f:
            f.write('{"prompt": "it\'s a knight", "cost": 1}')   # BOM + apostrophe, like PowerShell writes
        assert load_meta(argparse.Namespace(meta_file=mf, meta='{}')) == {'prompt': "it's a knight", 'cost': 1}
        assert load_meta(argparse.Namespace(meta_file=None, meta='{"cost": 3}')) == {'cost': 3}
    finally:
        globals()['try_job'] = real_try
    print('selftest OK')


if __name__ == '__main__':
    main()
