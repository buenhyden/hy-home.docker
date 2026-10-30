#!/usr/bin/env python3
"""Restore a stopped-volume Prometheus tar into an isolated container (SPEC-0245 W2).

The archive is checked against its SHA-256, extracted as the invoking user into a
new 0700 directory, and served by the Compose-pinned image with no network, no
capabilities and no scrape targets. The check records the extraction time, the
time to `/-/ready`, the head's newest sample and WAL corruption counter, and
`count(up)` at the head's end, one hour before the newest block and seven days
before that. A container that exits early stops the wait; its OOM flag and log
tail go into the receipt. The container is always removed; the scratch
directory is removed unless --keep and only after the container is gone.
Production containers and volumes are never touched.
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

IMAGE = "prom/prometheus:v3.15.1@sha256:fa3302279710be2f21a8301ec17a8b4f2301fd829bd113839b3b6b02b6f191a2"
LABEL = "hy.rehearsal=prometheus-restore"
API = "http://127.0.0.1:9090"
CONFIG = "global:\n  scrape_interval: 1h\n"
HEAD_METRICS = (
    "prometheus_tsdb_head_max_time",
    "prometheus_tsdb_wal_corruptions_total",
)


class RestoreError(Exception):
    """Input refused before anything runs."""


def _run(argv, *, timeout):
    try:
        done = subprocess.run(argv, capture_output=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return 1, b""
    return done.returncode, done.stdout + done.stderr


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


def _get(run, name: str, path: str) -> bytes | None:
    code, body = run(["docker", "exec", name, "wget", "-qO-", API + path], timeout=60)
    return None if code else body


def _query_count(run, name: str, at: int) -> int | None:
    query = urllib.parse.urlencode({"query": "count(up)", "time": at})
    body = _get(run, name, f"/api/v1/query?{query}")
    try:
        result = json.loads(body)["data"]["result"]
        return int(float(result[0]["value"][1])) if result else 0
    except (ValueError, KeyError, IndexError, TypeError):
        return None


def _head_metrics(run, name: str) -> dict:
    body = _get(run, name, "/metrics") or b""
    found = {}
    for line in body.decode(errors="replace").splitlines():
        key, _, value = line.partition(" ")
        if key in HEAD_METRICS:
            try:
                found[key] = float(value)
            except ValueError:
                pass
    return found


def _running(run, name: str) -> bool:
    code, out = run(
        ["docker", "inspect", "--format", "{{.State.Running}}", name], timeout=30
    )
    return code == 0 and out.strip() == b"true"


def _exit_evidence(run, name: str) -> dict:
    _, state = run(
        [
            "docker",
            "inspect",
            "--format",
            "{{.State.OOMKilled}} {{.State.ExitCode}}",
            name,
        ],
        timeout=30,
    )
    _, logs = run(["docker", "logs", "--tail", "20", name], timeout=30)
    return {
        "state": state.decode(errors="replace").strip(),
        "log_tail": logs.decode(errors="replace")[-4000:],
    }


def restore(
    *,
    archive: Path,
    sha256: str,
    workdir: Path,
    keep: bool,
    run=_run,
    sleep=time.sleep,
    clock=time.monotonic,
    ready_timeout: float = 900,
) -> dict:
    archive, workdir = Path(archive).resolve(), Path(workdir).absolute()
    if "," in str(workdir):
        raise RestoreError("workdir_comma")
    if not archive.is_file() or _sha256(archive) != sha256.lower():
        raise RestoreError("archive_sha256")
    if workdir.exists() or workdir.is_symlink():
        raise RestoreError("workdir_exists")
    if not workdir.parent.is_dir():
        raise RestoreError("workdir_parent")
    if shutil.disk_usage(workdir.parent).free < 2 * archive.stat().st_size:
        raise RestoreError("free_space")
    workdir.mkdir(mode=0o700)
    data, config = workdir / "data", workdir / "prometheus.yml"
    data.mkdir(mode=0o700)
    config.write_text(CONFIG)
    config.chmod(0o644)
    name = "hyhome-prom-restore-" + uuid.uuid4().hex[:12]
    receipt = {
        "archive_sha256": sha256.lower(),
        "image": IMAGE,
        "container": name,
        "extract_seconds": None,
        "ready_seconds": None,
        "head": {},
        "queries": [],
        "result": "FAIL",
    }
    try:
        started = clock()
        with tarfile.open(archive) as tar:
            tar.extractall(data, filter="data")
        receipt["blocks"], newest = _newest_block_seconds(data)
        receipt["extract_seconds"] = round(clock() - started, 3)
        started = clock()
        code, _ = run(
            [
                "docker", "run", "-d", f"--name={name}", f"--label={LABEL}",
                "--network=none", "--pull=never", "--cap-drop=ALL",
                "--security-opt=no-new-privileges", "--memory=2g", "--cpus=1",
                "--pids-limit=256", f"--user={os.getuid()}:{os.getgid()}",
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
            receipt["failure"] = "docker_run"
            return receipt
        while clock() - started < ready_timeout:
            if _get(run, name, "/-/ready") is not None:
                receipt["ready_seconds"] = round(clock() - started, 3)
                break
            if not _running(run, name):
                receipt["failure"] = "exited"
                receipt["exit"] = _exit_evidence(run, name)
                return receipt
            sleep(5)
        else:
            receipt["failure"] = "ready_timeout"
            receipt["exit"] = _exit_evidence(run, name)
            return receipt
        receipt["head"] = _head_metrics(run, name)
        times = [newest - 3600, newest - 3600 - 7 * 86400]
        head_ms = receipt["head"].get("prometheus_tsdb_head_max_time")
        if head_ms and head_ms > 0:
            times.insert(0, int(head_ms // 1000) - 300)
        for at in times:
            receipt["queries"].append(
                {"time": at, "count_up": _query_count(run, name, at)}
            )
        wal_ok = receipt["head"].get("prometheus_tsdb_wal_corruptions_total") == 0
        counts_ok = all((q["count_up"] or 0) > 0 for q in receipt["queries"])
        if wal_ok and counts_ok:
            receipt["result"] = "PASS"
        return receipt
    finally:
        removed, _ = run(["docker", "rm", "-f", name], timeout=60)
        if keep or removed:
            receipt["scratch_kept"] = True
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
