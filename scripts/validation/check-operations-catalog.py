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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("manifest", "structure", "executed", "complete", "consumers"),
        required=True,
    )
    parser.add_argument("--domains", help="retained for bounded CLI compatibility")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.domains and args.mode != "executed":
        parser.error("--domains is accepted only by --mode executed")
    try:
        findings = validate_current_operations(ROOT)
        if args.mode in {"complete", "consumers"}:
            findings = (*findings, *validate_active_operations_references(ROOT))
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
