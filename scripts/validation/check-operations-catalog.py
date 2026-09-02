#!/usr/bin/env python3
"""Validate the bounded current Stage 05 Operations tree."""

from __future__ import annotations

import argparse
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.document_governance.operations_catalog import (  # noqa: E402
    OperationsAuthorityError,
    validate_active_operations_references,
    validate_current_operations,
)


def _parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description=__doc__)


def main(argv: list[str] | None = None) -> int:
    """Validate the complete current Stage 05 tree in one route.

    The five retired modes selected between two validations, not five.
    `manifest`, `structure`, and `executed` ran the current-operations check
    alone; `complete` and `consumers` added the active-reference check. This
    route always runs both, so it is what `complete` did and nothing is lost.
    `--domains` was accepted and never read.
    """

    _parser().parse_args(argv)
    try:
        findings = (
            *validate_current_operations(ROOT),
            *validate_active_operations_references(ROOT),
        )
    except OperationsAuthorityError as error:
        print(f"FAIL {error.code}: {error}")
        return 1
    for finding in findings:
        print(f"FAIL {finding.code}: {finding.path}: {finding.message}")
    if findings:
        print(f"operations-catalog: FAIL findings={len(findings)}")
        return 1
    print("operations-catalog: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
