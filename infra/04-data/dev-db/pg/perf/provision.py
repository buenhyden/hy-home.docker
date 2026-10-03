#!/usr/bin/env python3
"""Apply the fixed perf_db bootstrap while holding a cluster advisory lock."""

from __future__ import annotations

import os
import re
import stat
import subprocess
import sys
from pathlib import Path

ADMIN_SECRET = Path("/run/secrets/dev_pg_admin_password")
BOOTSTRAP = Path("/work/perf/bootstrap.sql")
ADMIN_USER = re.compile(r"[a-z_][a-z0-9_]{0,62}\Z")
PSQL = ("psql", "-X", "-q", "-h", "dev-pg", "-p", "5432")
LOCK_SQL = (
    "SELECT CASE WHEN pg_try_advisory_lock("
    "hashtextextended('dev-pg:perf_db:bootstrap', 0)) "
    "THEN 'locked' ELSE 'busy' END;\n"
)


def fail(message, code=64):
    print(f"perf_db provision: {message}", file=sys.stderr)
    return code


def read_secret(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError("secret is not a regular file")
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("secret is not a regular file")
    value = path.read_bytes()
    if value.endswith(b"\n"):
        value = value[:-1]
    if (
        not value
        or len(value) > 512
        or any(c in value for c in (b"\x00", b"\r", b"\n"))
    ):
        raise ValueError("secret format is invalid")
    return value.decode("utf-8")


def close_guard(guard):
    try:
        if guard.stdin:
            guard.stdin.write("\\q\n")
            guard.stdin.flush()
        guard.communicate(timeout=5)
    except (BrokenPipeError, OSError):
        guard.wait(timeout=5)
    except subprocess.TimeoutExpired:
        guard.terminate()
        guard.wait(timeout=5)


def main():
    user = os.environ.get("DEV_PG_ADMIN_USER", "postgres")
    if not ADMIN_USER.fullmatch(user):
        return fail("invalid DEV_PG_ADMIN_USER")
    if BOOTSTRAP.is_symlink() or not BOOTSTRAP.is_file():
        return fail("bootstrap SQL is unavailable")
    try:
        password = read_secret(ADMIN_SECRET)
    except (OSError, UnicodeError, ValueError):
        return fail("admin secret is unavailable or invalid")

    env = os.environ.copy()
    env["PGPASSWORD"] = password
    env["PGCONNECT_TIMEOUT"] = "10"
    command = [*PSQL, "-U", user, "-d", "postgres", "-A", "-t"]
    guard = None
    try:
        guard = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        guard.stdin.write(LOCK_SQL)
        guard.stdin.flush()
        lock_state = guard.stdout.readline().strip()
        if lock_state != "locked":
            return fail(
                "another perf_db provision is active"
                if lock_state == "busy"
                else "could not acquire provision lock",
                75 if lock_state == "busy" else 69,
            )
        result = subprocess.run(
            [
                *PSQL,
                "-U",
                user,
                "-d",
                "postgres",
                "-v",
                "ON_ERROR_STOP=1",
                "-f",
                str(BOOTSTRAP),
            ],
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=180,
        )
        if result.returncode:
            return fail(
                "bootstrap SQL failed; inspect approved isolated logs",
                result.returncode,
            )
        return 0
    except (OSError, BrokenPipeError):
        return fail("psql process failed", 69)
    except subprocess.TimeoutExpired:
        return fail("bootstrap SQL timed out", 70)
    finally:
        if guard is not None and guard.poll() is None:
            close_guard(guard)


if __name__ == "__main__":
    sys.exit(main())
