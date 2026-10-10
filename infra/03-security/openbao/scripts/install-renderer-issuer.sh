#!/bin/sh
# Bootstrap this installer itself from the approved Git blob into a private directory.
# Public inputs only: repository, approved full commit SHA, new absolute install path.
# Extract exact reviewed Git blobs; credentials and source checkout permissions are irrelevant.
set +x
set -eu
exec >/dev/null 2>&1
[ "$#" -eq 3 ] || exit 1
exec /usr/bin/python3 -I - "$@" <<'PY'
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile

BASE = 'infra/03-security/openbao/scripts/'
FILES = {'issue-renderer-secret-id.sh': 0o500, 'renderer-issuance.py': 0o400}

def run(argv):
    done = subprocess.run(['/usr/bin/git', '--no-pager', *argv], stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10)
    if done.returncode:
        raise ValueError()
    return done.stdout

def install(repository, revision, target):
    if not re.fullmatch(r'[a-f0-9]{40}', revision):
        raise ValueError()
    repo = Path(repository)
    destination = Path(target)
    if (not repo.is_absolute() or not destination.is_absolute()
            or repo.resolve(strict=True) != repo
            or destination.parent.resolve(strict=True) != destination.parent):
        raise ValueError()
    info = destination.parent.lstat()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid()
            or stat.S_IMODE(info.st_mode) != 0o700 or os.path.lexists(destination)):
        raise ValueError()
    if run(['-C', str(repo), 'cat-file', '-t', revision]).strip() != b'commit':
        raise ValueError()
    blobs = {name: run(['-C', str(repo), 'show', revision + ':' + BASE + name])
             for name in FILES}
    if any(not blob or len(blob) > 100000 for blob in blobs.values()):
        raise ValueError()
    receipt = {'source_revision': revision,
               'sha256': {name: hashlib.sha256(blob).hexdigest() for name, blob in blobs.items()}}
    staged = Path(tempfile.mkdtemp(prefix='.sec01-issuer-', dir=destination.parent))
    try:
        content = {**blobs, 'source-receipt.json': json.dumps(receipt, sort_keys=True).encode()}
        for name, blob in content.items():
            fd = os.open(staged / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                         FILES.get(name, 0o400))
            with os.fdopen(fd, 'wb') as stream:
                stream.write(blob)
                stream.flush()
                os.fsync(stream.fileno())
        directory_fd = os.open(staged, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        # Linux renameat2 NOREPLACE prevents replacing even an empty unknown directory.
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.renameat2(-100, os.fsencode(staged), -100, os.fsencode(destination), 1):
            raise OSError(ctypes.get_errno())
        parent_fd = os.open(destination.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(parent_fd)
        finally:
            os.close(parent_fd)
    finally:
        if staged.exists():
            shutil.rmtree(staged)

try:
    install(*sys.argv[1:])
except Exception:
    sys.exit(1)
PY
