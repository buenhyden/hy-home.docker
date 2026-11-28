#!/usr/bin/env python3
"""Restore a Restic state copy of SeaweedFS into one isolated server (RUN-0024).

The input is a restored state tree (``--state-dir``) that holds
``volumes/data/seaweedfs/volume`` and ``exports/seaweedfs-filer.meta``. The
volume files and the metadata export are copied as the invoking user into a new
0700 work directory; the source tree is never written. One container from the
Compose-pinned image runs master, volume, filer and S3 together as the invoking
user, with ``--network none``, no capabilities and an empty master directory and
filer store. The run loads the metadata export, checks with
``volume.fsck -findMissingChunksInFiler`` that the filer entries still have
their chunks, then lists every bucket through S3 and reads every object,
comparing the S3 count and bytes with the filer's ``fs.du``. Buckets whose
volumes the state snapshot excludes (POL-0021) are reported and skipped. The
container is always removed; the work directory is removed unless --keep and
only after the container is gone. Production containers and volumes are never
touched. Exit 0 PASS, 1 FAIL, 2 refused input.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

IMAGE = "chrislusf/seaweedfs:4.54@sha256:4b42c212543a0acd4c0e675215ecdcaf62a186ef98def76c7e12701871222d15"
LABEL = "hy.rehearsal=seaweedfs-restore"
VOLUME_SOURCE = Path("volumes/data/seaweedfs/volume")
META_SOURCE = Path("exports/seaweedfs-filer.meta")
EXCLUDED_BUCKETS = ("loki-bucket", "tempo-bucket")
MASTER = "127.0.0.1:9333"
S3 = "http://127.0.0.1:8333"
S3_NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"
BUCKET_RE = re.compile(r"^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$")
DU_RE = re.compile(r"block:\s*(\d+)\s+(?:byte|logical size):\s*(\d+)")


class RestoreError(Exception):
    """Input refused before anything runs."""


def _run(argv, *, timeout, stdin=None):
    try:
        done = subprocess.run(
            argv, input=stdin, capture_output=True, timeout=timeout, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return 1, b""
    return done.returncode, done.stdout + done.stderr


def _tree_bytes(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def parse_du(text: str) -> tuple[int, int] | None:
    """Return (blocks, bytes) from the last `fs.du` total line."""
    found = DU_RE.findall(text)
    if not found:
        return None
    blocks, size = found[-1]
    return int(blocks), int(size)


def parse_buckets(text: str) -> list[str]:
    """Return bucket names from `fs.ls /buckets` output."""
    names = []
    for line in text.splitlines():
        name = line.strip().rstrip("/").split("/")[-1]
        if BUCKET_RE.match(name):
            names.append(name)
    return sorted(set(names))


FSCK_LINE_RE = re.compile(r"^\d+,[0-9a-f]+\s+(/\S+)\s+\S.*$")
SHELL_NOISE_RE = re.compile(r"^(>|total \d+ directories, \d+ files$)")


def parse_fsck(text: str) -> dict:
    """Count `volume.fsck -findMissingChunksInFiler` findings per bucket.

    SeaweedFS 4.54 prints one ``<fid> <path> <reason>`` line per filer chunk
    whose volume or needle is gone, such as ``volume not found``. Any other
    non-empty line is kept as unparsed so a format change fails the run instead
    of passing it.
    """
    by_bucket: dict[str, int] = {}
    unparsed = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or SHELL_NOISE_RE.match(line):
            continue
        match = FSCK_LINE_RE.match(line)
        if not match:
            unparsed.append(line)
            continue
        bucket = re.match(r"/buckets/([^/]+)", match.group(1))
        key = bucket.group(1) if bucket else "(outside /buckets)"
        by_bucket[key] = by_bucket.get(key, 0) + 1
    return {
        "missing_by_bucket": dict(sorted(by_bucket.items())),
        "missing_buckets": sorted(by_bucket),
        "unparsed": unparsed[:5],
    }


def _shell(run, name: str, commands: list[str], timeout: float = 1800) -> str:
    script = "\n".join(["lock", *commands, "unlock", "exit"]) + "\n"
    _, out = run(
        ["docker", "exec", "-i", name, "weed", "shell", f"-master={MASTER}"],
        timeout=timeout,
        stdin=script.encode(),
    )
    return out.decode(errors="replace")


def _get(run, name: str, url: str, timeout: float = 120) -> bytes | None:
    code, out = run(["docker", "exec", name, "wget", "-qO-", url], timeout=timeout)
    return out if code == 0 else None


def _list_bucket(run, name: str, bucket: str) -> list[tuple[str, int]] | None:
    objects, token = [], None
    while True:
        query = {"list-type": "2", "max-keys": "1000"}
        if token:
            query["continuation-token"] = token
        body = _get(run, name, f"{S3}/{bucket}?{urllib.parse.urlencode(query)}")
        if body is None:
            return None
        root = ET.fromstring(body)
        for item in root.iter(f"{S3_NS}Contents"):
            objects.append(
                (item.findtext(f"{S3_NS}Key"), int(item.findtext(f"{S3_NS}Size")))
            )
        if root.findtext(f"{S3_NS}IsTruncated") != "true":
            return objects
        token = root.findtext(f"{S3_NS}NextContinuationToken")


def _read_all(run, name: str, workdir: Path, bucket: str, keys) -> tuple[int, int]:
    """Read every object once; return (objects read, bytes read)."""
    listing = workdir / "keys.txt"
    listing.write_text(
        "".join(f"{S3}/{bucket}/{urllib.parse.quote(key, safe='/')}\n" for key in keys)
    )
    script = (
        "n=0; b=0; while IFS= read -r u; do "
        'if wget -qO /tmp/o "$u"; then n=$((n+1)); b=$((b+$(wc -c < /tmp/o))); fi; '
        'done < /data/keys.txt; rm -f /tmp/o; echo "$n $b"'
    )
    _, out = run(["docker", "exec", name, "sh", "-c", script], timeout=7200)
    listing.unlink()
    read, size = [*out.decode().split(), "0", "0"][:2]
    return int(read), int(size)


def _wait(run, name: str, volumes: int, sleep, clock, timeout: float) -> bool:
    started = clock()
    while clock() - started < timeout:
        status = _get(run, name, "http://127.0.0.1:8080/status", timeout=20)
        if status is not None:
            try:
                ready = len(json.loads(status).get("Volumes") or []) >= volumes
            except ValueError:
                ready = False
            if ready and _get(run, name, "http://127.0.0.1:8888/", timeout=20):
                if _get(run, name, f"{S3}/", timeout=20) is not None:
                    return True
        sleep(3)
    return False


def restore(
    *,
    state_dir: Path,
    workdir: Path,
    keep: bool,
    run=_run,
    sleep=time.sleep,
    clock=time.monotonic,
    ready_timeout: float = 600,
) -> dict:
    state_dir, workdir = Path(state_dir).resolve(), Path(workdir).absolute()
    volume_src, meta_src = state_dir / VOLUME_SOURCE, state_dir / META_SOURCE
    if not volume_src.is_dir() or not any(volume_src.glob("*.dat")):
        raise RestoreError("volume_source")
    if not meta_src.is_file() or meta_src.stat().st_size == 0:
        raise RestoreError("filer_meta")
    if workdir.exists() or workdir.is_symlink():
        raise RestoreError("workdir_exists")
    if not workdir.parent.is_dir():
        raise RestoreError("workdir_parent")
    if "," in str(workdir) or ":" in str(workdir):
        raise RestoreError("workdir_name")
    need = _tree_bytes(volume_src) + meta_src.stat().st_size
    if shutil.disk_usage(workdir.parent).free < 2 * need:
        raise RestoreError("free_space")
    volumes = len(list(volume_src.glob("*.dat")))
    name = "hyhome-swfs-restore-" + uuid.uuid4().hex[:12]
    receipt = {
        "image": IMAGE,
        "container": name,
        "volumes": volumes,
        "copy_seconds": None,
        "ready_seconds": None,
        "meta_loaded": False,
        "fsck": {},
        "buckets": {},
        "excluded_buckets": [],
        "result": "FAIL",
    }
    workdir.mkdir(mode=0o700)
    try:
        started = clock()
        shutil.copytree(volume_src, workdir / "volume")
        (workdir / "master").mkdir()
        (workdir / "filerldb2").mkdir()
        shutil.copy2(meta_src, workdir / "filer.meta")
        receipt["copy_seconds"] = round(clock() - started, 3)
        started = clock()
        code, _ = run(
            [
                "docker", "run", "-d", f"--name={name}", f"--label={LABEL}",
                "--network=none", "--pull=never", "--cap-drop=ALL",
                "--security-opt=no-new-privileges", "--memory=4g", "--cpus=2",
                "--pids-limit=512", f"--user={os.getuid()}:{os.getgid()}",
                f"--mount=type=bind,src={workdir},dst=/data",
                "--entrypoint=weed", IMAGE, "server",
                "-ip=127.0.0.1", "-ip.bind=127.0.0.1", "-dir=/data/volume",
                "-master.dir=/data/master", "-volume.max=0", "-filer", "-s3",
            ],
            timeout=120,
        )  # fmt: skip
        if code:
            receipt["failure"] = "docker_run"
            return receipt
        if not _wait(run, name, volumes, sleep, clock, ready_timeout):
            receipt["failure"] = "ready_timeout"
            return receipt
        receipt["ready_seconds"] = round(clock() - started, 3)
        load = _shell(run, name, ["fs.meta.load /data/filer.meta"])
        (workdir / "meta-load.log").write_text(load)
        buckets = parse_buckets(_shell(run, name, ["fs.ls /buckets"]))
        receipt["meta_loaded"] = bool(buckets) and "error" not in load.lower()
        if not receipt["meta_loaded"]:
            receipt["failure"] = "meta_load"
            return receipt
        fsck = _shell(run, name, ["volume.fsck -findMissingChunksInFiler"])
        (workdir / "fsck.log").write_text(fsck)
        receipt["fsck"] = parse_fsck(fsck)
        checked_ok = True
        for bucket in buckets:
            if bucket in EXCLUDED_BUCKETS:
                receipt["excluded_buckets"].append(bucket)
                continue
            du = parse_du(_shell(run, name, [f"fs.du /buckets/{bucket}"]))
            listing = _list_bucket(run, name, bucket)
            entry = {"filer_bytes": du[1] if du else None}
            if listing is None:
                entry["s3_list"] = "failed"
                checked_ok = False
            else:
                read, size = _read_all(
                    run, name, workdir, bucket, [k for k, _ in listing]
                )
                entry.update(
                    s3_objects=len(listing),
                    s3_listed_bytes=sum(s for _, s in listing),
                    objects_read=read,
                    bytes_read=size,
                )
                entry["match"] = (
                    read == len(listing)
                    and size == entry["s3_listed_bytes"]
                    and (du is None or du[1] == size)
                )
                checked_ok = checked_ok and entry["match"]
            receipt["buckets"][bucket] = entry
        unexpected = [
            b for b in receipt["fsck"]["missing_buckets"] if b not in EXCLUDED_BUCKETS
        ]
        receipt["fsck"]["unexpected_missing_buckets"] = unexpected
        if checked_ok and not unexpected and not receipt["fsck"]["unparsed"]:
            receipt["result"] = "PASS"
        return receipt
    finally:
        removed, _ = run(["docker", "rm", "-f", name], timeout=60)
        if keep or removed:
            receipt["workdir_kept"] = True
            (workdir / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        else:
            shutil.rmtree(workdir, ignore_errors=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv)
    try:
        receipt = restore(
            state_dir=args.state_dir, workdir=args.workdir, keep=args.keep
        )
    except RestoreError as error:
        print(json.dumps({"result": "REFUSED", "reason": str(error)}))
        return 2
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
