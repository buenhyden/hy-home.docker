#!/usr/bin/env python3
"""Install one immutable, root-owned Hermes Publisher release from a commit.

Run as root with `python3 -I`. The input is `git archive --format=tar <commit>
-- <workload>`: the commit id in its pax header names the release, only the
tracked publisher modules, key store and hash lock are taken from it, and the
lock is installed with --require-hashes into a fresh venv. Nothing is ever
overwritten; rollback points the runner at an earlier release.
"""

import argparse
import hashlib
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
from pathlib import Path

WORKLOAD = "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/"
MEMBER = re.compile(
    re.escape(WORKLOAD)
    + r"(publisher/[a-z_]+\.py|publisher/producer-keys\.json|requirements\.lock)\Z"
)
COMMIT = re.compile(r"[0-9a-f]{40}\Z")


def _fail(message):
    print(f"install: {message}", file=sys.stderr)
    raise SystemExit(1)


def _members(archive):
    with tarfile.open(archive, "r:") as tar:
        commit = tar.pax_headers.get("comment", "")
        if not COMMIT.fullmatch(commit):
            _fail("archive has no commit id; use git archive <commit>")
        files = {}
        for member in tar.getmembers():
            match = MEMBER.fullmatch(member.name)
            if match and member.isfile():
                files[match.group(1)] = tar.extractfile(member).read()
    if "requirements.lock" not in files or "publisher/trust.py" not in files:
        _fail("archive lacks the publisher workload")
    return commit, files


def _run(*command):
    # stdout carries only the release path.
    subprocess.run(
        command, check=True, env={"PATH": "/usr/bin:/bin"}, stdout=sys.stderr
    )


def _seal(path):
    """root:root and no group/other write; execute bits are kept."""
    os.lchown(path, 0, 0)
    if not path.is_symlink():
        path.chmod(stat.S_IMODE(path.lstat().st_mode) & ~0o022)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--prefix", type=Path, default=Path("/opt/hermes-publisher"))
    parser.add_argument("--python", default="/usr/bin/python3")
    parser.add_argument("--find-links", type=Path, help="offline wheel directory")
    args = parser.parse_args(argv)
    if os.geteuid() != 0 or not sys.flags.isolated:
        _fail("run as root with python3 -I")
    os.umask(0o022)
    commit, files = _members(args.archive)
    releases = args.prefix / "releases"
    final, staging = releases / commit, releases / f".{commit}.partial"
    if final.exists():
        _fail("release already installed; releases are immutable")
    releases.mkdir(parents=True, exist_ok=True)
    for path in (args.prefix, releases):
        _seal(path)
    shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir()
    lock = staging / "requirements.lock"
    lock.write_bytes(files.pop("requirements.lock"))
    venv = staging / "venv"
    _run(args.python, "-I", "-m", "venv", str(venv))
    python = str(venv / "bin" / "python")
    pip = [python, "-I", "-m", "pip", "--disable-pip-version-check"]
    offline = []
    if args.find_links:
        offline = ["--no-index", "--find-links", str(args.find_links)]
    _run(
        *pip, "install", "--no-cache-dir", "--require-hashes", "--no-deps",
        "--only-binary", ":all:", *offline, "-r", str(lock),
    )  # fmt: skip
    _run(*pip, "uninstall", "--yes", "pip")
    purelib = subprocess.run(
        [python, "-I", "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"],
        check=True,
        capture_output=True,
        text=True,
        env={},
    ).stdout.strip()
    package = Path(purelib) / "publisher"
    package.mkdir()
    manifest = []
    for name, data in sorted(files.items()):
        (package.parent / name).write_bytes(data)
        manifest.append(f"{hashlib.sha256(data).hexdigest()}  {name}\n")
    _run(python, "-I", "-m", "compileall", "-q", str(package))
    (staging / "MANIFEST.sha256").write_text("".join(manifest))
    for path in [staging, *staging.rglob("*")]:
        _seal(path)
    staging.rename(final)
    print(final)


if __name__ == "__main__":
    main()
