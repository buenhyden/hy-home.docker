#!/usr/bin/env bash
set -euo pipefail

# POL-0095: prepare only versioned public policy inputs, then run the declared job.
mode="all"
if [[ $# -eq 2 && $1 == "--mode" ]]; then
  mode=$2
elif [[ $# -ne 0 ]]; then
  echo "usage: $0 [--mode verify|corpus|all]" >&2
  exit 2
fi
case "$mode" in
  verify|corpus|all) ;;
  *) echo "usage: $0 [--mode verify|corpus|all]" >&2; exit 2 ;;
esac

root="$(git rev-parse --show-toplevel)"
cd "$root"
compose=(docker compose -p hyhome-conftest-gate -f infra/11-quality/conftest/docker-compose.yml --profile policy-check)
temporary=""
attempted=0
cleanup() {
  status=$?
  trap - EXIT
  if [[ $attempted -eq 1 ]]; then
    "${compose[@]}" down --remove-orphans >/dev/null 2>&1 || echo "WARNING: Conftest job cleanup failed." >&2
  fi
  if [[ -n $temporary ]]; then
    if [[ -d $temporary/inputs && ! -L $temporary/inputs ]]; then
      chmod 0700 -- "$temporary/inputs"
    fi
    rm -rf -- "$temporary"
  fi
  exit "$status"
}
trap cleanup EXIT

if [[ $mode != verify ]]; then
  umask 077
  temporary=$(mktemp -d /tmp/hyhome-conftest.XXXXXX)
  python3 - "$root" "$temporary" <<'PY'
import hashlib
import json
import os
import pathlib
import stat
import sys

root, target = map(pathlib.Path, sys.argv[1:])
sys.path.insert(0, str(root))
from scripts.lib.document_governance.operations_catalog import (
    MAX_FILE_BYTES, OperationsAuthorityError, conftest_source_context,
)


def write(name, chunks, mode):
    path = target / name
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    total = 0
    try:
        with os.fdopen(descriptor, "wb") as stream:
            for chunk in chunks:
                total += len(chunk)
                if total > MAX_FILE_BYTES:
                    raise ValueError("prepared policy input exceeds its bound")
                stream.write(chunk)
            stream.flush()
            os.fsync(stream.fileno())
            os.fchmod(stream.fileno(), mode)
    except BaseException:
        path.unlink(missing_ok=True)
        raise
    return path


try:
    info = target.lstat()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid()
            or stat.S_IMODE(info.st_mode) != 0o700 or target.resolve() != target):
        raise ValueError("unsafe prepared input directory")
    context = conftest_source_context(root)
    if set(context["overlay_inputs"]) != set(context["overlays"]):
        raise ValueError("overlay input set differs from canonical overlays")
    (target / "inputs").mkdir(mode=0o700)
    mounts = []
    environment = {}
    for kind, key in (("compose", "compose"), ("dockerfile", "dockerfiles")):
        paths = context[key]
        if not paths or len(set(paths)) != len(paths):
            raise ValueError("empty or duplicate policy corpus")
        data = b"".join(path.as_posix().encode() + b"\0" for path in paths)
        write(f"inputs/{kind}.paths0", (data,), 0o444)
        environment[f"HYHOME_CONFTEST_{kind.upper()}_SHA256"] = hashlib.sha256(data).hexdigest()
    for index, (relative, document) in enumerate(sorted(context["overlay_inputs"].items())):
        chunks = (chunk.encode() for chunk in json.JSONEncoder(allow_nan=False).iterencode(document))
        path = write(f"overlay-{index}.json", chunks, 0o444)
        mounts.append({"type": "bind", "source": str(path),
                       "target": "/project/" + relative.as_posix().replace("$", "$$"),
                       "read_only": True, "bind": {"create_host_path": False}})
    os.chmod(target / "inputs", 0o555)
    mounts.append({"type": "bind", "source": str(target / "inputs"),
                   "target": "/project/.conftest-source-inputs", "read_only": True,
                   "bind": {"create_host_path": False}})
    document = {"services": {"conftest": {"volumes": mounts, "environment": environment}}}
    chunks = (chunk.encode() for chunk in json.JSONEncoder(allow_nan=False).iterencode(document))
    write("job.json", chunks, 0o600)
except (OperationsAuthorityError, ValueError, OSError) as error:
    print(f"ERROR: Conftest source preparation failed: {error}", file=sys.stderr)
    sys.exit(2)
PY
  compose+=(-f "$temporary/job.json")
fi

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker is required for the Conftest policy check." >&2
  exit 2
fi
attempted=1
"${compose[@]}" run --rm conftest "$mode"
