#!/usr/bin/env python3
"""Check pre-commit-hooks EOF/trailing rules without rewriting or printing content."""

from __future__ import annotations

import argparse
import io
import os
import stat
import sys


def invalid_eof(data: bytes) -> bool:
    ending = data[len(data.rstrip(b"\r\n")) :]
    return bool(data) and (
        len(ending) == len(data) or ending not in {b"\n", b"\r\n", b"\r"}
    )


def trailing_whitespace(data: bytes) -> bool:
    for line in io.BytesIO(data):
        if line.endswith(b"\r\n"):
            line = line[:-2]
        elif line.endswith(b"\n"):
            line = line[:-1]
        if line != line.rstrip():
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", choices=("eof", "trailing"), required=True)
    parser.add_argument("filenames", nargs="+")
    arguments = parser.parse_args()
    check = invalid_eof if arguments.check == "eof" else trailing_whitespace
    status = 0
    for filename in arguments.filenames:
        try:
            descriptor = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(descriptor, "rb") as source:
                if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                    raise ValueError("a regular file is required")
                invalid = check(source.read())
        except (OSError, ValueError) as error:
            print(f"{filename}: text style input error: {error}", file=sys.stderr)
            status = 2
            continue
        if invalid:
            print(
                f"{filename}: {arguments.check} style failed; run the registered formatter explicitly"
            )
            status = max(status, 1)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
