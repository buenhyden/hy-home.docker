#!/usr/bin/env python3
"""P30, P50 and P80 completion-time forecasts recorded before work starts.

A forecast is fixed before the task starts and never edited: a changed
estimate is a new revision, and SQLite triggers refuse any update or delete.
P30, P50 and P80 are the times by which the task completes with probability
0.3, 0.5 and 0.8, not progress shares. Each revision records its assumptions
and reference class, and the number of comparable tasks (same type and time
basis) that had completed in this store before it was made. An outcome is
recorded once, as completed, failed, cancelled or blocked, names the
revision it is scored against and closes the task. `score` groups by task
type and time basis and reports, per quantile, how often the actual time fell
at or under the forecast with its 95% Wilson interval and the mean pinball
loss, with the sample size; failed, cancelled and blocked tasks are censored
and counted apart, and open forecasts are counted. A forecast is a planning
aid, not a deadline, an approval, a gate or a reason to skip a required
check.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.lib.hooks import session_capture as capture  # noqa: E402
from scripts.operations.agent_memory import MemoryStoreError  # noqa: E402

STORE_NAME = "forecast.sqlite3"
UNITS = ("minutes",)
TIME_BASES = ("elapsed", "active")
STATUSES = ("completed", "failed", "cancelled", "blocked")
CENSORED = STATUSES[1:]
QUANTILES = (("p30", 0.3), ("p50", 0.5), ("p80", 0.8))
# ponytail: a flat floor; a per-type calibration rule can replace it with data
MIN_CALIBRATION_SAMPLE = 20
SCHEMA = (
    "CREATE TABLE IF NOT EXISTS forecasts (task_ref TEXT NOT NULL,"
    " revision INTEGER NOT NULL, task_type TEXT NOT NULL, unit TEXT NOT NULL,"
    " time_basis TEXT NOT NULL, p30 REAL NOT NULL, p50 REAL NOT NULL,"
    " p80 REAL NOT NULL, assumptions TEXT, reference_class TEXT,"
    " sample_size INTEGER, forecasted_at TEXT NOT NULL, comparable_prior INTEGER,"
    " PRIMARY KEY (task_ref, revision))",
    "CREATE TABLE IF NOT EXISTS outcomes (task_ref TEXT PRIMARY KEY,"
    " status TEXT NOT NULL, started_at TEXT NOT NULL, finished_at TEXT NOT NULL,"
    " active_minutes REAL, runner_wait_minutes REAL, user_wait_minutes REAL,"
    " observed_at TEXT NOT NULL, forecast_revision INTEGER)",
    "CREATE TRIGGER IF NOT EXISTS forecasts_no_update BEFORE UPDATE ON forecasts"
    " BEGIN SELECT RAISE(ABORT, 'forecasts are append-only'); END",
    "CREATE TRIGGER IF NOT EXISTS forecasts_no_delete BEFORE DELETE ON forecasts"
    " BEGIN SELECT RAISE(ABORT, 'forecasts are append-only'); END",
    # REPLACE deletes without firing DELETE triggers, so refuse the insert itself.
    "CREATE TRIGGER IF NOT EXISTS forecasts_no_replace BEFORE INSERT ON forecasts"
    " WHEN EXISTS (SELECT 1 FROM forecasts WHERE task_ref=NEW.task_ref"
    " AND revision=NEW.revision)"
    " BEGIN SELECT RAISE(ABORT, 'forecasts are append-only'); END",
    "CREATE TRIGGER IF NOT EXISTS outcomes_no_replace BEFORE INSERT ON outcomes"
    " WHEN EXISTS (SELECT 1 FROM outcomes WHERE task_ref=NEW.task_ref)"
    " BEGIN SELECT RAISE(ABORT, 'outcomes are append-only'); END",
    "CREATE TRIGGER IF NOT EXISTS outcomes_no_update BEFORE UPDATE ON outcomes"
    " BEGIN SELECT RAISE(ABORT, 'outcomes are append-only'); END",
    "CREATE TRIGGER IF NOT EXISTS outcomes_no_delete BEFORE DELETE ON outcomes"
    " BEGIN SELECT RAISE(ABORT, 'outcomes are append-only'); END",
)


class ForecastError(ValueError):
    """A forecast or outcome that the contract refuses."""


def now() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds")


def _when(value: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(value)
    except ValueError as error:
        raise ForecastError(f"not an ISO 8601 time: {value}") from error
    if parsed.tzinfo is None:
        raise ForecastError(f"time needs a UTC offset: {value}")
    return parsed


def connect(directory: Path) -> sqlite3.Connection:
    capture.connect(directory).close()  # the same private directory checks
    path = directory / STORE_NAME
    if path.is_symlink():
        raise OSError("forecast store is a symbolic link")
    connection = sqlite3.connect(path, timeout=1.0, isolation_level=None)
    os.chmod(path, 0o600)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 1000")
    for statement in SCHEMA:
        connection.execute(statement)
    for table, column in (
        ("forecasts", "comparable_prior INTEGER"),
        ("outcomes", "forecast_revision INTEGER"),
    ):  # a store written before these columns
        present = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
        if column.split()[0] not in present:
            connection.execute(f"ALTER TABLE {table} ADD COLUMN {column}")
    return connection


def _comparable(connection, task_type: str, time_basis: str, before: str) -> int:
    """Completed tasks of the same type and basis that ended before `before`."""
    count = 0
    for outcome in connection.execute(
        "SELECT * FROM outcomes WHERE status='completed'"
    ).fetchall():
        if _when(outcome["finished_at"]) > _when(before):
            continue
        chosen = _scored(connection, outcome)
        if chosen and (chosen["task_type"], chosen["time_basis"]) == (
            task_type,
            time_basis,
        ):
            count += 1
    return count


def _scored(connection, outcome):
    """The revision an outcome is scored against: the stored link, else the
    last revision fixed before its start (an outcome before the link)."""
    if outcome["forecast_revision"] is not None:
        return connection.execute(
            "SELECT * FROM forecasts WHERE task_ref=? AND revision=?",
            (outcome["task_ref"], outcome["forecast_revision"]),
        ).fetchone()
    return _pre_start(connection, outcome["task_ref"], _when(outcome["started_at"]))[1]


def forecast(
    directory: Path,
    task_ref: str,
    task_type: str,
    p30: float,
    p50: float,
    p80: float,
    *,
    unit: str = "minutes",
    time_basis: str = "elapsed",
    assumptions: str = "",
    reference_class: str = "",
    sample_size: int = 0,
    forecasted_at: str | None = None,
) -> int:
    """Append a revision; refuse inversion, bad units and a closed task."""
    if not task_ref or not task_type:
        raise ForecastError("task_ref and task_type are required")
    if not assumptions.strip() or not reference_class.strip():
        raise ForecastError("assumptions and reference_class are required")
    if type(sample_size) is not int or sample_size < 0:
        raise ForecastError("sample_size must be a whole number, 0 or more")
    if unit not in UNITS:
        raise ForecastError(f"unit must be one of {UNITS}")
    if time_basis not in TIME_BASES:
        raise ForecastError(f"time_basis must be one of {TIME_BASES}")
    if not all(math.isfinite(value) for value in (p30, p50, p80)):
        raise ForecastError("quantiles must be finite numbers")
    if not 0 <= p30 <= p50 <= p80:
        raise ForecastError("quantiles must satisfy 0 <= p30 <= p50 <= p80")
    at = forecasted_at or now()
    _when(at)
    connection = connect(directory)
    try:
        connection.execute("BEGIN IMMEDIATE")
        if connection.execute(
            "SELECT 1 FROM outcomes WHERE task_ref=?", (task_ref,)
        ).fetchone():
            connection.execute("ROLLBACK")
            raise ForecastError(f"{task_ref} already has an outcome")
        revision = (
            connection.execute(
                "SELECT COALESCE(MAX(revision), 0) FROM forecasts WHERE task_ref=?",
                (task_ref,),
            ).fetchone()[0]
            + 1
        )
        connection.execute(
            "INSERT INTO forecasts (task_ref, revision, task_type, unit,"
            " time_basis, p30, p50, p80, assumptions, reference_class,"
            " sample_size, forecasted_at, comparable_prior)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                task_ref,
                revision,
                task_type,
                unit,
                time_basis,
                p30,
                p50,
                p80,
                assumptions,
                reference_class,
                sample_size,
                at,
                _comparable(connection, task_type, time_basis, at),
            ),
        )
        connection.execute("COMMIT")
        return revision
    finally:
        connection.close()


def _pre_start(connection, task_ref: str, started: dt.datetime):
    """The last revision fixed at or before the start, which is what is scored."""
    rows = connection.execute(
        "SELECT * FROM forecasts WHERE task_ref=? ORDER BY revision", (task_ref,)
    ).fetchall()
    eligible = [row for row in rows if _when(row["forecasted_at"]) <= started]
    return rows, (eligible[-1] if eligible else None)


def observe(
    directory: Path,
    task_ref: str,
    status: str,
    started_at: str,
    finished_at: str,
    *,
    active_minutes: float | None = None,
    runner_wait_minutes: float | None = None,
    user_wait_minutes: float | None = None,
) -> dict:
    """Record the one outcome of a task that had a forecast before it started."""
    if status not in STATUSES:
        raise ForecastError(f"status must be one of {STATUSES}")
    started, finished = _when(started_at), _when(finished_at)
    if finished < started:
        raise ForecastError("finished_at precedes started_at")
    if finished > dt.datetime.now(dt.UTC):
        raise ForecastError("finished_at is in the future")
    elapsed = (finished - started).total_seconds() / 60
    for value in (active_minutes, runner_wait_minutes, user_wait_minutes):
        if value is not None and not (math.isfinite(value) and value >= 0):
            raise ForecastError("minutes must be finite and not negative")
    if active_minutes is not None and active_minutes > elapsed:
        raise ForecastError("active_minutes exceeds the elapsed time")
    connection = connect(directory)
    try:
        connection.execute("BEGIN IMMEDIATE")
        rows, chosen = _pre_start(connection, task_ref, started)
        problem = (
            f"{task_ref} has no forecast"
            if not rows
            else f"{task_ref} has no forecast fixed before it started"
            if chosen is None
            else f"{task_ref} already has an outcome"
            if connection.execute(
                "SELECT 1 FROM outcomes WHERE task_ref=?", (task_ref,)
            ).fetchone()
            else "an active-time forecast needs active_minutes"
            if chosen["time_basis"] == "active"
            and active_minutes is None
            and status == "completed"
            else None
        )
        if problem:
            connection.execute("ROLLBACK")
            raise ForecastError(problem)
        connection.execute(
            "INSERT INTO outcomes (task_ref, status, started_at, finished_at,"
            " active_minutes, runner_wait_minutes, user_wait_minutes, observed_at,"
            " forecast_revision) VALUES (?,?,?,?,?,?,?,?,?)",
            (
                task_ref,
                status,
                started_at,
                finished_at,
                active_minutes,
                runner_wait_minutes,
                user_wait_minutes,
                now(),
                chosen["revision"],
            ),
        )
        connection.execute("COMMIT")
    finally:
        connection.close()
    actual = active_minutes if chosen["time_basis"] == "active" else elapsed
    return {
        "task_ref": task_ref,
        "status": status,
        "revision": chosen["revision"],
        "time_basis": chosen["time_basis"],
        "actual_minutes": actual,
    }


def _wilson(hits: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    """95% Wilson score interval for a coverage share; None without a sample."""
    if not n:
        return None
    share, spread = hits / n, z * z / n
    centre = (share + spread / 2) / (1 + spread)
    margin = z * math.sqrt(share * (1 - share) / n + spread / (4 * n)) / (1 + spread)
    return (round(centre - margin, 4), round(centre + margin, 4))


def score(
    directory: Path, task_type: str | None = None, time_basis: str | None = None
) -> dict:
    """Coverage and pinball per quantile over completed tasks; censored apart.

    Only one task type on one time basis is a comparable group; a wider
    selection is reported with its groups and never labelled empirical.
    """
    connection = connect(directory)
    try:
        outcomes = connection.execute(
            "SELECT * FROM outcomes ORDER BY task_ref"
        ).fetchall()
        closed = {outcome["task_ref"] for outcome in outcomes}
        latest = connection.execute(
            "SELECT f.* FROM forecasts f WHERE revision=(SELECT max(revision)"
            " FROM forecasts g WHERE g.task_ref=f.task_ref)"
        ).fetchall()
        completed, censored = [], dict.fromkeys(CENSORED, 0)
        groups: dict[tuple[str, str], dict] = {}

        def selected(row) -> bool:
            return (task_type is None or row["task_type"] == task_type) and (
                time_basis is None or row["time_basis"] == time_basis
            )

        def group(row) -> dict:
            key = (row["task_type"], row["time_basis"])
            return groups.setdefault(
                key,
                {"task_type": key[0], "time_basis": key[1], "completed": 0,
                 "censored": 0, "open": 0},
            )  # fmt: skip

        for outcome in outcomes:
            chosen = _scored(connection, outcome)
            if chosen is None or not selected(chosen):
                continue
            if outcome["status"] in censored:
                censored[outcome["status"]] += 1
                group(chosen)["censored"] += 1
                continue
            elapsed = (
                _when(outcome["finished_at"]) - _when(outcome["started_at"])
            ).total_seconds() / 60
            actual = (
                outcome["active_minutes"]
                if chosen["time_basis"] == "active"
                else elapsed
            )
            completed.append((chosen, actual))
            group(chosen)["completed"] += 1
        opened = 0
        for row in latest:
            if row["task_ref"] not in closed and selected(row):
                opened += 1
                group(row)["open"] += 1
    finally:
        connection.close()
    quantiles = {}
    for name, p in QUANTILES:
        pairs = [(row[name], actual) for row, actual in completed]
        n = len(pairs)
        hits = sum(actual <= q for q, actual in pairs)
        quantiles[name] = {
            "n": n,
            "coverage": hits / n if n else None,
            "coverage_95": _wilson(hits, n),
            # pinball L_p(y, q) = (p - 1[y < q]) * (y - q), not doubled
            "pinball": (
                sum((p - (actual < q)) * (actual - q) for q, actual in pairs) / n
                if n
                else None
            ),
        }
    bases = {basis for _, basis in groups}
    types = {kind for kind, _ in groups}
    calibration = (
        "mixed time bases; score one basis"
        if len(bases) > 1
        else "insufficient sample"
        if len(completed) < MIN_CALIBRATION_SAMPLE
        else "pooled across types; score one type"
        if task_type is None or len(types) > 1
        else "empirical"
    )
    return {
        "task_type": task_type,
        "time_basis": time_basis,
        "completed": len(completed),
        **censored,
        "open": opened,
        "calibration": calibration,
        "groups": [groups[key] for key in sorted(groups)],
        "note": "completed tasks only; failed, cancelled and blocked tasks are"
        " censored, open forecasts are not scored",
        "quantiles": quantiles,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    predict = commands.add_parser("forecast")
    predict.add_argument("task_ref")
    predict.add_argument("--type", required=True, dest="task_type")
    for name in ("p30", "p50", "p80"):
        predict.add_argument(f"--{name}", type=float, required=True)
    predict.add_argument("--time-basis", default="elapsed", choices=TIME_BASES)
    predict.add_argument("--assumptions", default="")
    predict.add_argument("--reference-class", default="")
    predict.add_argument("--sample-size", type=int, default=0)
    seen = commands.add_parser("observe")
    seen.add_argument("task_ref")
    seen.add_argument("--status", required=True, choices=STATUSES)
    seen.add_argument("--started-at", required=True)
    seen.add_argument("--finished-at", required=True)
    for name in ("active", "runner-wait", "user-wait"):
        seen.add_argument(f"--{name}-minutes", type=float)
    scoring = commands.add_parser("score")
    scoring.add_argument("--type", dest="task_type")
    scoring.add_argument("--time-basis", choices=TIME_BASES)
    args = parser.parse_args(argv)
    try:
        directory = capture.capture_dir()
        if args.command == "forecast":
            result = {
                "task_ref": args.task_ref,
                "revision": forecast(
                    directory,
                    args.task_ref,
                    args.task_type,
                    args.p30,
                    args.p50,
                    args.p80,
                    time_basis=args.time_basis,
                    assumptions=args.assumptions,
                    reference_class=args.reference_class,
                    sample_size=args.sample_size,
                ),
            }
            connection = connect(directory)
            try:
                prior = connection.execute(
                    "SELECT comparable_prior FROM forecasts WHERE task_ref=?"
                    " AND revision=?",
                    (args.task_ref, result["revision"]),
                ).fetchone()[0]
            finally:
                connection.close()
            result.update(
                comparable_prior=prior,
                calibration="uncalibrated prior"
                if prior < MIN_CALIBRATION_SAMPLE
                else "comparable sample",
                meaning="P30/P50/P80: completion within that time with"
                " probability 0.3/0.5/0.8, not progress",
            )
        elif args.command == "observe":
            result = observe(
                directory,
                args.task_ref,
                args.status,
                args.started_at,
                args.finished_at,
                active_minutes=args.active_minutes,
                runner_wait_minutes=args.runner_wait_minutes,
                user_wait_minutes=args.user_wait_minutes,
            )
        else:
            result = score(directory, args.task_type, args.time_basis)
    except (ForecastError, MemoryStoreError, OSError, sqlite3.Error) as error:
        print(f"FORECAST_REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
