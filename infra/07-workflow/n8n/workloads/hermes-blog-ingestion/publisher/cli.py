"""Offline staging/status CLI. No send command or credential inputs."""

import argparse
import json
import os
import sqlite3
from pathlib import Path

from .candidates import EXPORT_NAME, JOBS, load_candidate, load_validator
from .files import InputError, open_directory
from .outbox import Outbox, OutboxError


def _scan(args, box):
    validator = load_validator(args.validator, args.validator_sha256)
    counts = dict(staged=0, duplicate=0, conflict=0, rejected=0)
    with open_directory(args.exports):
        pass
    for job in JOBS:
        try:
            with open_directory(args.exports / job) as descriptor:
                names = []
                with os.scandir(descriptor) as entries:
                    for entry in entries:
                        if EXPORT_NAME.fullmatch(entry.name):
                            names.append(entry.name)
                            if len(names) > 1000:
                                raise InputError("scan_limit")
        except InputError as error:
            if str(error) == "directory_missing":
                continue
            raise
        for name in sorted(names):
            try:
                snapshot = load_candidate(
                    args.exports, job, name, args.source_root, args.item_root, validator
                )
                outcome = box.stage(snapshot)
                counts[outcome] += 1
            except (InputError, OutboxError):
                counts["rejected"] += 1
    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    stage = sub.add_parser("stage")
    for name in ("exports", "source-root", "item-root", "validator"):
        stage.add_argument("--" + name, type=Path, required=True)
    stage.add_argument("--validator-sha256", required=True)
    stage.add_argument("--outbox", type=Path, required=True)
    status = sub.add_parser("status")
    status.add_argument("--outbox", type=Path, required=True)
    args = parser.parse_args(argv)
    box = None
    try:
        box = Outbox(args.outbox)
        result = _scan(args, box) if args.command == "stage" else box.counts()
        print(json.dumps(result, sort_keys=True))
        return 1 if result.get("rejected", 0) or result.get("conflict", 0) else 0
    except (InputError, OutboxError, OSError, sqlite3.Error):
        print('{"error":"operation_rejected"}')
        return 1
    finally:
        if box is not None:
            box.close()


if __name__ == "__main__":
    raise SystemExit(main())
