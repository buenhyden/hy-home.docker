#!/usr/bin/env python3
"""Restore a stopped-volume Prometheus tar into an isolated container (SPEC-0245 W2).

The archive is checked against its SHA-256, extracted as the invoking user into a
new 0700 directory, and served by the Compose-pinned image with no network, no
capabilities and no scrape targets. The check waits for `/-/ready` (the time is
the measured recovery seconds) and runs `count(up)` one hour and seven days
before the newest block. The container is always removed; the scratch directory
is removed unless --keep. Production containers and volumes are never touched.
Exit 0 PASS, 1 FAIL, 2 refused input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.parse
import uuid
from pathlib import Path

IMAGE = "prom/prometheus:v3.15.0@sha256:efd719c99d83b060d9daefdcf00360461adf279f45ef5391f8d111892118753e"
LABEL = "hy.rehearsal=prometheus-restore"
API = "http://127.0.0.1:9090"
CONFIG = "global:\n  scrape_interval: 1h\n"


class RestoreError(Exception):
    """Input refused before anything runs."""


def _run(argv, *, timeout):
    try:
        done = subprocess.run(argv, capture_output=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return 1, b""
    return done.returncode, done.stdout


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _newest_block_seconds(data: Path) -> tuple[int, int]:
    times = [
        int(json.loads(meta.read_text())["maxTime"]) // 1000
        for meta in data.glob("*/meta.json")
    ]
    if not times:
        raise RestoreError("no_blocks")
    return len(times), max(times)


def _query_count(run, name: str, at: int) -> int | None:
    query = urllib.parse.urlencode({"query": "count(up)", "time": at})
    code, body = run(
        ["docker", "exec", name, "wget", "-qO-", f"{API}/api/v1/query?{query}"],
        timeout=60,
    )
    if code:
        return None
    try:
        result = json.loads(body)["data"]["result"]
        return int(float(result[0]["value"][1])) if result else 0
    except (ValueError, KeyError, IndexError, TypeError):
        return None


def restore(
    *,
    archive: Path,
    sha256: str,
    workdir: Path,
    keep: bool,
    run=_run,
    sleep=time.sleep,
    ready_timeout: float = 900,
) -> dict:
    archive, workdir = Path(archive), Path(workdir)
    if not archive.is_file() or _sha256(archive) != sha256:
        raise RestoreError("archive_sha256")
    if workdir.exists() or workdir.is_symlink():
        raise RestoreError("workdir_exists")
    if not workdir.parent.is_dir():
        raise RestoreError("workdir_parent")
    workdir.mkdir(mode=0o700)
    data, config = workdir / "data", workdir / "prometheus.yml"
    data.mkdir(mode=0o700)
    config.write_text(CONFIG)
    config.chmod(0o644)
    name = "hyhome-prom-restore-" + uuid.uuid4().hex[:12]
    receipt = {
        "archive_sha256": sha256,
        "image": IMAGE,
        "container": name,
        "ready_seconds": None,
        "queries": [],
        "result": "FAIL",
    }
    try:
        with tarfile.open(archive) as tar:
            tar.extractall(data, filter="data")
        receipt["blocks"], newest = _newest_block_seconds(data)
        started = time.monotonic()
        code, _ = run(
            [
                "docker", "run", "-d", f"--name={name}", f"--label={LABEL}",
                "--network=none", "--pull=never", "--cap-drop=ALL",
                "--security-opt=no-new-privileges", "--memory=2g", "--cpus=1",
                f"--user={os.getuid()}:{os.getgid()}",
                f"--mount=type=bind,src={data},dst=/prometheus",
                f"--mount=type=bind,src={config},dst=/etc/prometheus/prometheus.yml,readonly",
                IMAGE,
                "--config.file=/etc/prometheus/prometheus.yml",
                "--storage.tsdb.path=/prometheus",
                "--storage.tsdb.retention.time=36500d",
                "--web.listen-address=127.0.0.1:9090",
            ],
            timeout=120,
        )  # fmt: skip
        if code:
            return receipt
        while time.monotonic() - started < ready_timeout:
            code, _ = run(
                ["docker", "exec", name, "wget", "-qO-", f"{API}/-/ready"], timeout=30
            )
            if code == 0:
                receipt["ready_seconds"] = round(time.monotonic() - started, 3)
                break
            sleep(5)
        else:
            return receipt
        latest = newest - 3600
        for at in (latest, latest - 7 * 86400):
            receipt["queries"].append(
                {"time": at, "count_up": _query_count(run, name, at)}
            )
        if all((q["count_up"] or 0) > 0 for q in receipt["queries"]):
            receipt["result"] = "PASS"
        return receipt
    finally:
        run(["docker", "rm", "-f", name], timeout=60)
        if keep:
            (workdir / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        else:
            shutil.rmtree(workdir, ignore_errors=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv)
    try:
        receipt = restore(
            archive=args.archive,
            sha256=args.sha256,
            workdir=args.workdir,
            keep=args.keep,
        )
    except RestoreError as error:
        print(json.dumps({"result": "REFUSED", "reason": str(error)}))
        return 2
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
