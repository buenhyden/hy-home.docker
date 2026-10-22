"""SPEC-0246 W7 write-rate snapshots and the SSD endurance comparison.

A snapshot is three files named ``<label>.time``, ``<label>.diskstats`` and
``<label>.cgroup-wbytes.tsv`` (container name, StartedAt, written bytes). The
written bytes are the sum of every ``io.stat`` line, which is how the
2026-10-19 t0 was taken; dm-0 repeats the SSD's line, so a store's delta is an
upper bound on its real writes. Collection reads only Docker metadata,
``/proc/diskstats`` and cgroup files.
"""

from __future__ import annotations

import math
import subprocess
from datetime import datetime
from pathlib import Path

STORES = ("prometheus", "loki", "tempo", "pyroscope", "alloy")
MIN_WINDOW_SECONDS = 24 * 3600
BUDGET_YEARS = 5.0
SECTOR_BYTES = 512
CGROUP_ROOT = Path("/sys/fs/cgroup/system.slice")
SUFFIXES = {"time": ".time", "diskstats": ".diskstats", "wbytes": ".cgroup-wbytes.tsv"}


def _finite(value: int | float) -> bool:
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def _counter(text: str) -> int:
    value = int(text)
    if value < 0 or not _finite(value):
        raise ValueError("counter must be nonnegative and finite")
    return value


def parse_time(text: str) -> datetime:
    value = datetime.fromisoformat(text.strip())
    if value.tzinfo is None:
        raise ValueError("snapshot time needs a UTC offset")
    return value


def parse_wbytes(text: str) -> dict[str, tuple[str, int]]:
    rows: dict[str, tuple[str, int]] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        name, started, written = line.split("\t")
        if name in rows:
            raise ValueError(f"duplicate container row: {name}")
        rows[name] = (started, _counter(written))
    return rows


def parse_diskstats(text: str) -> dict[str, int]:
    """Return bytes written per device (field 10 is sectors written)."""
    return {name: row[2] for name, row in _diskstats_rows(text).items()}


def _diskstats_rows(text: str) -> dict[str, tuple[int, int, int]]:
    rows = {}
    for line in text.splitlines():
        fields = line.split()
        if not fields:
            continue
        if len(fields) < 10 or fields[2] in rows:
            raise ValueError("malformed or duplicate diskstats device")
        rows[fields[2]] = (
            _counter(fields[0]),
            _counter(fields[1]),
            _counter(fields[9]) * SECTOR_BYTES,
        )
    return rows


def iostat_wbytes(text: str) -> int:
    return sum(
        _counter(item.split("=", 1)[1])
        for line in text.splitlines()
        for item in line.split()[1:]
        if item.startswith("wbytes=")
    )


def read_snapshot(directory: Path, label: str) -> dict[str, str]:
    return {
        key: (directory / f"{label}{suffix}").read_text()
        for key, suffix in SUFFIXES.items()
    }


def collect(directory: Path, label: str, devices: tuple[str, ...]) -> None:
    paths = {key: directory / f"{label}{suffix}" for key, suffix in SUFFIXES.items()}
    if any(path.exists() for path in paths.values()):
        raise FileExistsError(f"snapshot {label} already exists in {directory}")
    now = datetime.now().astimezone().replace(microsecond=0)
    disks = [
        line
        for line in Path("/proc/diskstats").read_text().splitlines()
        if len(line.split()) > 2 and line.split()[2] in devices
    ]
    ids = subprocess.run(
        ["docker", "ps", "-q"], check=True, capture_output=True, text=True
    ).stdout.split()
    rows = []
    if ids:
        inspected = subprocess.run(
            [
                "docker",
                "inspect",
                "-f",
                "{{.Name}}\t{{.State.StartedAt}}\t{{.Id}}",
                *ids,
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        for line in inspected.splitlines():
            name, started, container_id = line.split("\t")
            stat = CGROUP_ROOT / f"docker-{container_id}.scope" / "io.stat"
            rows.append(
                f"{name.lstrip('/')}\t{started}\t{iostat_wbytes(stat.read_text())}"
            )
    directory.mkdir(parents=True, exist_ok=True)
    paths["time"].write_text(now.isoformat() + "\n")
    paths["diskstats"].write_text("\n".join(disks) + "\n")
    paths["wbytes"].write_text("\n".join(rows) + "\n")


def _years(used_percent: float, host_bytes: int, bytes_per_day: float) -> float:
    try:
        years = (100.0 - used_percent) / (
            used_percent / host_bytes * bytes_per_day * 365.25
        )
    except (OverflowError, ZeroDivisionError) as error:
        raise ValueError("endurance calculation is outside the finite range") from error
    if not _finite(years):
        raise ValueError("endurance calculation is outside the finite range")
    return years


def _daily_bytes(delta: int, days: float) -> float:
    try:
        rate = delta / days
    except OverflowError as error:
        raise ValueError("write rate is outside the finite range") from error
    if not _finite(rate):
        raise ValueError("write rate is outside the finite range")
    return rate


def compare(
    t0: dict[str, str],
    t1: dict[str, str],
    *,
    ssd_device: str,
    smart_used_percent: float | None = None,
    smart_host_bytes: int | None = None,
) -> dict[str, object]:
    """Compare two snapshots read by ``read_snapshot``."""
    if smart_used_percent is not None and (
        isinstance(smart_used_percent, bool)
        or not isinstance(smart_used_percent, (int, float))
        or not _finite(smart_used_percent)
        or not 0 <= smart_used_percent <= 100
    ):
        raise ValueError("SMART used percentage must be finite and between 0 and 100")
    if smart_host_bytes is not None and (
        type(smart_host_bytes) is not int
        or smart_host_bytes <= 0
        or not _finite(smart_host_bytes)
    ):
        raise ValueError("SMART host bytes must be a positive finite integer")
    start, end = parse_time(t0["time"]), parse_time(t1["time"])
    window = (end - start).total_seconds()
    if window <= 0:
        raise ValueError("t1 is not after t0")
    days = window / 86400
    short = window < MIN_WINDOW_SECONDS
    smart = bool(smart_used_percent and smart_host_bytes)
    disk0, disk1 = _diskstats_rows(t0["diskstats"]), _diskstats_rows(t1["diskstats"])

    disks: dict[str, dict[str, object]] = {}
    for device in sorted(disk0.keys() & disk1.keys()):
        delta = disk1[device][2] - disk0[device][2]
        if disk0[device][:2] != disk1[device][:2]:
            disks[device] = {"status": "invalid", "reason": "device numbers changed"}
        elif delta < 0:
            disks[device] = {
                "status": "invalid",
                "reason": "counter decreased (reboot)",
            }
        else:
            disks[device] = {
                "status": "valid",
                "bytes": delta,
                "bytes_per_day": _daily_bytes(delta, days),
            }
    ssd = disks.get(ssd_device, {"status": "invalid", "reason": "SSD device missing"})
    ssd_rate = ssd["bytes_per_day"] if ssd["status"] == "valid" and not short else None
    baseline = (
        _years(smart_used_percent, smart_host_bytes, ssd_rate)
        if smart and ssd_rate
        else None
    )

    rows0, rows1 = parse_wbytes(t0["wbytes"]), parse_wbytes(t1["wbytes"])
    stores: dict[str, dict[str, object]] = {}
    for store in STORES:
        if short:
            reason = "window shorter than 24 h"
        elif store not in rows0 or store not in rows1:
            reason = "missing from a snapshot"
        elif rows0[store][0] != rows1[store][0]:
            reason = "container restarted (counter reset)"
        elif rows1[store][1] < rows0[store][1]:
            reason = "counter decreased"
        elif not ssd_rate:
            reason = "SSD rate unavailable"
        elif not smart:
            reason = "SMART counters not supplied"
        else:
            reason = None
        if reason:
            stores[store] = {
                "status": "invalid",
                "reason": reason,
                "disposition": "DEFER",
            }
            continue
        delta = rows1[store][1] - rows0[store][1]
        rate = _daily_bytes(delta, days)
        years = _years(smart_used_percent, smart_host_bytes, ssd_rate + rate)
        stores[store] = {
            "status": "valid",
            "bytes": delta,
            "bytes_per_day": rate,
            "ssd_years_with_store": years,
            "disposition": "ELIGIBLE" if years >= BUDGET_YEARS else "KEEP_HDD",
        }
    return {
        "t0": start.isoformat(),
        "t1": end.isoformat(),
        "window_seconds": window,
        "disks": disks,
        "ssd_device": ssd_device,
        "ssd_years_baseline": baseline,
        "budget_years": BUDGET_YEARS,
        "stores": stores,
        "accounting": (
            "cgroup io.stat sum of all device lines; dm-0 repeats the SSD line, "
            "so store bytes are an upper bound"
        ),
    }
