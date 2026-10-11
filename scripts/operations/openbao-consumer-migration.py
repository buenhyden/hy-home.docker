#!/usr/bin/env python3
"""Offline public contract validation; accepts synthetic JSON on stdin only."""

from __future__ import annotations

import os
import select
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.lib.ops.openbao_consumer_migration import (
    MAX_BYTES,
    MigrationError,
    parse_public_json,
    validate_public,
)


def _stdin() -> bytes:
    deadline = time.monotonic() + 5
    payload = b""
    descriptor = sys.stdin.fileno()
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0 or not select.select([descriptor], [], [], remaining)[0]:
            raise MigrationError("public_input_timeout")
        chunk = os.read(descriptor, min(65536, MAX_BYTES + 1 - len(payload)))
        if not chunk:
            return payload
        payload += chunk
        if len(payload) > MAX_BYTES:
            raise MigrationError("public_input_size")


def main(argv=None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if arguments == ["--help"]:
        print("usage: openbao-consumer-migration.py {validate-wave,validate-receipt}")
        print("Reads bounded public synthetic JSON from stdin; validates shape only.")
        return 0
    if len(arguments) != 1 or arguments[0] not in {"validate-wave", "validate-receipt"}:
        print("FAIL: public_command_invalid", file=sys.stderr)
        return 2
    try:
        validate_public(
            arguments[0].removeprefix("validate-"), parse_public_json(_stdin())
        )
    except MigrationError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 2
    except (OSError, ValueError):
        print("FAIL: public_input_unavailable", file=sys.stderr)
        return 2
    print("PASS: public contract shape only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
