#!/usr/bin/env python3
"""Compare single-file config bind mounts on the host with the running container copy.

Read-only: lists running containers of the Compose project, and for every bind
mount whose source is a regular file inside the repository checkout, compares
the SHA-256 of the host file with the file the container actually sees.

The container copy is read with ``docker exec <container> cat <dest>``.
``docker cp`` is deliberately not used: the daemon resolves bind mounts to the
host Source, so it cannot see the stale inode a container keeps after an editor
replaces the host file. Images without ``cat`` report UNREADABLE unless
``--helper-image`` names a local image with ``cat``; the check then starts a
transient ``--rm`` helper with no network in the target's PID namespace and
reads ``/proc/1/root<dest>``. Paths under ``secrets/`` are skipped before any
read. File contents are never printed. Exit 1 when any mount differs, 2 when
Docker cannot be queried.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

PROJECT = "hy-home-infra"
DEFAULT_ROOT = pathlib.Path(__file__).resolve().parents[2]


def _docker(run, *args: str) -> subprocess.CompletedProcess:
    return run(["docker", *args], capture_output=True, check=False)


def _container_digest(run, container: str, dest: str, helper: str | None) -> str | None:
    result = _docker(run, "exec", container, "cat", dest)
    if result.returncode != 0 and helper:
        result = _docker(
            run,
            "run",
            "--rm",
            "--network",
            "none",
            "--pid",
            f"container:{container}",
            "--cap-add",
            "SYS_PTRACE",
            helper,
            "cat",
            f"/proc/1/root{dest}",
        )
    if result.returncode != 0:
        return None
    return hashlib.sha256(result.stdout).hexdigest()


def _host_digest(path: pathlib.Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _mounts(run, root: pathlib.Path):
    listed = _docker(
        run,
        "ps",
        "--filter",
        f"label=com.docker.compose.project={PROJECT}",
        "--format",
        "{{.Names}}",
    )
    if listed.returncode != 0:
        raise RuntimeError("docker ps failed")
    names = sorted(listed.stdout.decode().split())
    if not names:
        return
    inspected = _docker(run, "inspect", *names)
    if inspected.returncode != 0:
        raise RuntimeError("docker inspect failed")
    for container in json.loads(inspected.stdout):
        name = container["Name"].lstrip("/")
        for mount in container.get("Mounts") or []:
            if mount.get("Type") != "bind":
                continue
            source = pathlib.Path(mount["Source"])
            try:
                relative = source.relative_to(root)
            except ValueError:
                continue
            if relative.parts[:1] == ("secrets",) or not source.is_file():
                continue
            yield name, mount["Destination"], source, relative


def main(argv: list[str] | None = None, run=subprocess.run) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=DEFAULT_ROOT,
        help="repository checkout the running containers were started from",
    )
    parser.add_argument(
        "--helper-image",
        help="local image with cat used to read containers that lack it",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    counts = {"MATCH": 0, "DIFF": 0, "UNREADABLE": 0}
    try:
        rows = sorted(_mounts(run, root))
    except (RuntimeError, OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    for name, dest, source, relative in rows:
        host = _host_digest(source)
        inside = _container_digest(run, name, dest, args.helper_image)
        if host is None or inside is None:
            status = "UNREADABLE"
        else:
            status = "MATCH" if host == inside else "DIFF"
        counts[status] += 1
        print(f"{status:<10}  {name}  {dest}  {relative}")
    print(" ".join(f"{key.lower()}={value}" for key, value in counts.items()))
    return 1 if counts["DIFF"] else 0


if __name__ == "__main__":
    sys.exit(main())
