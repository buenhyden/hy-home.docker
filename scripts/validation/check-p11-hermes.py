#!/usr/bin/env python3
"""Run the complete, offline P11 Hermes regression suite."""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import unittest
from collections.abc import Sequence
from types import MappingProxyType
from typing import TextIO

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERMES_TESTS = ROOT / "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests"
HERMES_E2E_CONTRACT = HERMES_TESTS / "e2e-cache-contract.sh"
PATTERN = "test_*.py"
E2E_TIMEOUT_SECONDS = 60
E2E_SUCCESS = (
    "PASS: cached image is pinned; missing, malformed and invalid references are "
    "rejected"
)
E2E_ENVIRONMENT = MappingProxyType(
    {
        "GIT_CONFIG_NOSYSTEM": "1",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": os.defpath,
    }
)


class HermesGateError(RuntimeError):
    """The complete regression boundary is unavailable or unsafe."""


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
    """Discover every reviewed Python regression in the Hermes test directory."""
    test_directory = _canonical_test_directory(root)
    active_loader = loader or unittest.TestLoader()
    return active_loader.discover(
        start_dir=str(test_directory),
        pattern=PATTERN,
        top_level_dir=str(test_directory),
    )


def _canonical_contract_script(root: pathlib.Path) -> pathlib.Path:
    candidate = (
        root.absolute()
        / "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests"
        / "e2e-cache-contract.sh"
    )
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise HermesGateError("cache-only E2E contract is unavailable") from exc
    if resolved != candidate or not resolved.is_file():
        raise HermesGateError("cache-only E2E contract is not canonical")
    return resolved


def run_e2e_contract(
    *,
    runner=subprocess.run,
    stream: TextIO | None = None,
    root: pathlib.Path = ROOT,
) -> int:
    """Run the cache-only contract with a bounded, value-free environment."""
    output = stream or sys.stderr
    try:
        script = _canonical_contract_script(root)
        result = runner(
            ["/bin/bash", str(script)],
            cwd=root,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=E2E_TIMEOUT_SECONDS,
            env=E2E_ENVIRONMENT,
            check=False,
        )
    except HermesGateError as exc:
        output.write(f"P11 Hermes gate: {exc}\n")
        return 1
    except subprocess.TimeoutExpired:
        output.write("P11 Hermes gate: cache-only E2E contract timed out\n")
        return 1
    except OSError:
        output.write("P11 Hermes gate: cache-only E2E contract could not run\n")
        return 1
    if result.returncode != 0:
        output.write("P11 Hermes gate: cache-only E2E contract failed\n")
        return 1
    observed = tuple(line for line in result.stdout.splitlines() if line)
    if observed != (E2E_SUCCESS,):
        output.write("P11 Hermes gate: cache-only E2E contract reported no result\n")
        return 1
    output.write("P11 Hermes gate: cache-only E2E contract passed (1/1)\n")
    return 0


def run(
    *,
    loader: unittest.TestLoader | None = None,
    stream: TextIO | None = None,
    contract_runner=subprocess.run,
) -> int:
    """Execute the gate and reject empty, skip-only, or failed results."""
    output = stream or sys.stderr
    try:
        suite = load_suite(loader=loader)
    except HermesGateError as exc:
        output.write(f"P11 Hermes gate: {exc}\n")
        return 1
    if suite.countTestCases() == 0:
        output.write("P11 Hermes gate: no tests discovered\n")
        return 1
    result = unittest.TextTestRunner(
        stream=output,
        verbosity=2,
        buffer=True,
    ).run(suite)
    if result.testsRun == len(result.skipped):
        output.write("P11 Hermes gate: all discovered tests skipped\n")
        return 1
    if not result.wasSuccessful():
        return 1
    return run_e2e_contract(runner=contract_runner, stream=output)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        sys.stderr.write("usage: check-p11-hermes.py\n")
        return 2
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
