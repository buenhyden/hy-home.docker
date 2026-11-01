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
# Publisher modules only: producer-side code (signing, fetching) never ships here.
MODULES = (
    "__init__", "candidates", "cli", "delivery", "evidence", "files",
    "gateway_adapter", "gateway_transport", "http_transport", "outbox",
    "policy", "trust",
)  # fmt: skip
# The attester runs as its own account from its own prefix; only its release
# carries the signing and source-fetching modules.
ATTESTER_MODULES = ("attestation", "attester", "source_check", "source_fetch")
PREFIX = {
    "publisher": Path("/opt/hermes-publisher"),
    "attester": Path("/opt/hermes-attester"),
}


def role_files(role):
    modules = MODULES + (ATTESTER_MODULES if role == "attester" else ())
    return {
        *(f"publisher/{name}.py" for name in modules),
        "publisher/producer-keys.json",
        "requirements.lock",
    }


COMMIT = re.compile(r"[0-9a-f]{40}\Z")


def _fail(message):
    print(f"install: {message}", file=sys.stderr)
    raise SystemExit(1)


def _root_only(path, info):
    if (
        stat.S_ISLNK(info.st_mode)
        or info.st_uid != 0
        or stat.S_IMODE(info.st_mode) & 0o022
    ):
        _fail(f"{path} must be root-owned, not a link, without group/other write")


def _directory(path):
    """Create or accept path only if it and every ancestor are root-only."""
    for item in [*reversed(path.parents), path]:
        if not os.path.lexists(item):
            os.mkdir(item, 0o755)
        info = os.lstat(item)
        _root_only(item, info)
        if not stat.S_ISDIR(info.st_mode):
            _fail(f"{item} is not a directory")


def _members(archive, wanted):
    """Read the allowlisted files of a root-only `git archive` tar."""
    for item in archive.parents:
        _root_only(item, os.lstat(item))
    descriptor = os.open(archive, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "rb") as handle:
        info = os.fstat(handle.fileno())
        _root_only(archive, info)
        if not stat.S_ISREG(info.st_mode):
            _fail("archive is not a regular file")
        with tarfile.open(fileobj=handle, mode="r:") as tar:
            commit = tar.pax_headers.get("comment", "")
            if not COMMIT.fullmatch(commit):
                _fail("archive has no commit id; use git archive <commit>")
            files = {}
            for member in tar.getmembers():
                name = member.name.removeprefix(WORKLOAD)
                if member.name.startswith(WORKLOAD) and name in wanted:
                    if name in files or not member.isfile():
                        _fail(f"ambiguous archive member {name}")
                    files[name] = tar.extractfile(member).read()
    if set(files) != wanted:
        _fail("archive lacks release files")
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
    parser.add_argument("--role", choices=sorted(PREFIX), default="publisher")
    parser.add_argument("--prefix", type=Path, help="default: /opt/hermes-<role>")
    parser.add_argument("--python", default="/usr/bin/python3")
    parser.add_argument("--find-links", type=Path, help="offline wheel directory")
    args = parser.parse_args(argv)
    if os.geteuid() != 0 or not sys.flags.isolated:
        _fail("run as root with python3 -I")
    os.umask(0o022)
    commit, files = _members(args.archive.absolute(), role_files(args.role))
    releases = (args.prefix or PREFIX[args.role]) / "releases"
    final, staging = releases / commit, releases / f".{commit}.partial"
    if final.exists():
        _fail("release already installed; releases are immutable")
    _directory(releases.absolute())
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
