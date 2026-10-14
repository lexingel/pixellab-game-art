"""upload.py <upload_url> <file.png> [more.png ...] - send local images to PixelLab and print one
"<file> upload:<id>" line each. Get <upload_url> from the get_upload_url tool (valid 15 min, any
number of files); pass the upload:<id> wherever a tool takes an image URL. Uploads last 3 days.
Stdlib only (no curl needed)."""
import json
import os
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
import urllib.request
import uuid


def upload(url, path):
    boundary = uuid.uuid4().hex
    body = (('--%s\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\n'
             'Content-Type: image/png\r\n\r\n') % (boundary, os.path.basename(path))).encode()
    body += open(path, 'rb').read() + ('\r\n--%s--\r\n' % boundary).encode()
    req = urllib.request.Request(url, data=body, method='POST',
                                 headers={'Content-Type': 'multipart/form-data; boundary=' + boundary})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())['ref']


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    for p in sys.argv[2:]:
        print(p, upload(sys.argv[1], p))
