#!/usr/bin/env python3
"""Run the fixed, offline P03 Hermes regression set."""

from __future__ import annotations

import pathlib
import sys
import unittest
from collections.abc import Sequence
from typing import TextIO

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERMES_TESTS = ROOT / "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests"
PATTERNS = (
    "test_research_report_plugin.py",
    "test_webhook_transport.py",
)


class HermesGateError(RuntimeError):
    """The fixed regression boundary is unavailable or unsafe."""


def _canonical_test_directory(root: pathlib.Path) -> pathlib.Path:
    candidate = (
        root.absolute() / "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests"
    )
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise HermesGateError("Hermes test directory is unavailable") from exc
    if resolved != candidate or not resolved.is_dir():
        raise HermesGateError("Hermes test directory is not canonical")
    return resolved


def load_suite(
    *,
    loader: unittest.TestLoader | None = None,
    root: pathlib.Path = ROOT,
) -> unittest.TestSuite:
    """Load only the two reviewed Hermes test files from the repository root."""
    test_directory = _canonical_test_directory(root)
    active_loader = loader or unittest.TestLoader()
    suites = tuple(
        active_loader.discover(
            start_dir=str(test_directory),
            pattern=pattern,
            top_level_dir=str(test_directory),
        )
        for pattern in PATTERNS
    )
    return unittest.TestSuite(suites)


def run(
    *,
    loader: unittest.TestLoader | None = None,
    stream: TextIO | None = None,
) -> int:
    """Execute the gate and reject empty, skip-only, or failed results."""
    output = stream or sys.stderr
    try:
        suite = load_suite(loader=loader)
    except HermesGateError as exc:
        output.write(f"P03 Hermes gate: {exc}\n")
        return 1
    if suite.countTestCases() == 0:
        output.write("P03 Hermes gate: no tests discovered\n")
        return 1
    result = unittest.TextTestRunner(
        stream=output,
        verbosity=2,
        buffer=True,
    ).run(suite)
    if result.testsRun == len(result.skipped):
        output.write("P03 Hermes gate: all discovered tests skipped\n")
        return 1
    return 0 if result.wasSuccessful() else 1


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        sys.stderr.write("usage: check-p03-hermes.py\n")
        return 2
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
