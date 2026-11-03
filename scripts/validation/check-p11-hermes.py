#!/usr/bin/env python3
"""Run the complete, offline P11 Hermes regression suite."""

from __future__ import annotations

import importlib.metadata
import os
import pathlib
import re
import site
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Sequence
from types import MappingProxyType
from typing import TextIO

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERMES_TESTS = ROOT / "infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests"
HERMES_E2E_CONTRACT = HERMES_TESTS / "e2e-cache-contract.sh"
HERMES_LOCK = HERMES_TESTS.parent / "requirements.lock"
PATTERN = "test_*.py"
E2E_TIMEOUT_SECONDS = 60
INSTALL_TIMEOUT_SECONDS = 300
# Set only on the child this gate starts inside its workload environment.
CHILD_MARKER = "HYHOME_P11_HERMES_WORKLOAD_ENV"
_ROOT_KEY = "HYHOME_CI_GATE_ROOT"
_PIN = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([^\s\\;]+)")
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


def locked_requirements(root: pathlib.Path = ROOT) -> dict[str, str]:
    """Return the exact name==version pins of the workload's hashed lock."""
    candidate = root.absolute() / HERMES_LOCK.relative_to(ROOT)
    try:
        resolved = candidate.resolve(strict=True)
        text = resolved.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise HermesGateError("workload requirements lock is unavailable") from exc
    if resolved != candidate or not resolved.is_file():
        raise HermesGateError("workload requirements lock is not canonical")
    pins = {
        match.group(1).lower().replace("_", "-"): match.group(2)
        for match in map(_PIN.match, text.splitlines())
        if match
    }
    if not pins:
        raise HermesGateError("workload requirements lock pins nothing")
    return pins


def locked_requirements_present(pins: dict[str, str], *, version=None) -> bool:
    """True when this interpreter already has every locked version."""
    lookup = version or importlib.metadata.version
    for name, expected in pins.items():
        try:
            if lookup(name) != expected:
                return False
        except importlib.metadata.PackageNotFoundError:
            return False
    return True


def inherited_root_descriptors() -> tuple[int, ...]:
    """Keep the CI runner's descriptor-rooted checkout valid in the child.

    The runner exposes the checkout as HYHOME_CI_GATE_ROOT=/proc/self/fd/N and
    its sitecustomize puts that path on sys.path. subprocess closes N by
    default, so the rerun would otherwise resolve it to an unrelated file.
    """
    match = re.fullmatch(r"/proc/self/fd/(\d+)", os.environ.get(_ROOT_KEY, ""))
    if match is None:
        return ()
    descriptor = int(match.group(1))
    try:
        os.fstat(descriptor)
    except OSError:
        return ()
    return (descriptor,)


def controller_site_paths() -> list[str]:
    """Third-party package directories this interpreter imports from."""
    candidates = [*site.getsitepackages(), *sys.path]
    seen: list[str] = []
    for path in candidates:
        name = pathlib.PurePath(path).name
        if name in {"site-packages", "dist-packages"} and path not in seen:
            seen.append(path)
    return seen


def run_in_workload_environment(
    *,
    runner=subprocess.run,
    stream: TextIO | None = None,
    root: pathlib.Path = ROOT,
) -> int:
    """Install the hashed workload lock into a throwaway venv and rerun there.

    The trusted controller interpreter does not carry the workload's
    dependencies, so the regression suite runs in its own environment instead
    of widening the controller lock.
    """
    output = stream or sys.stderr
    lock = root.absolute() / HERMES_LOCK.relative_to(ROOT)
    with tempfile.TemporaryDirectory(prefix="p11-hermes-") as directory:
        venv = pathlib.Path(directory) / "venv"
        python = venv / "bin/python"
        steps = (
            ("create", [sys.executable, "-m", "venv", str(venv)]),
            (
                "install",
                [
                    str(python), "-m", "pip", "install",
                    "--disable-pip-version-check", "--no-input",
                    "--require-hashes", "--no-deps", "--only-binary=:all:",
                    "-r", str(lock),
                ],
            ),
        )  # fmt: skip
        for label, argv in steps:
            try:
                result = runner(
                    argv,
                    cwd=root,
                    stdin=subprocess.DEVNULL,
                    capture_output=True,
                    text=True,
                    timeout=INSTALL_TIMEOUT_SECONDS,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired):
                result = None
            if result is None or result.returncode != 0:
                output.write(f"P11 Hermes gate: workload environment {label} failed\n")
                return 1
        # The suite also needs the controller's own packages (PyYAML,
        # jsonschema). A .pth file appends this interpreter's site-packages
        # after the venv's, so locked versions win and `python -I` subprocesses
        # in the suite still see both.
        version = f"python{sys.version_info.major}.{sys.version_info.minor}"
        site_dir = venv / "lib" / version / "site-packages"
        site_dir.mkdir(parents=True, exist_ok=True)
        (site_dir / "zz-controller-site.pth").write_text(
            "".join(f"{path}\n" for path in controller_site_paths()),
            encoding="utf-8",
        )
        try:
            child = runner(
                [str(python), str(pathlib.Path(__file__).resolve())],
                cwd=root,
                stdin=subprocess.DEVNULL,
                env={**os.environ, CHILD_MARKER: "1"},
                pass_fds=inherited_root_descriptors(),
                check=False,
            )
        except OSError:
            output.write("P11 Hermes gate: workload environment could not run\n")
            return 1
    return 0 if child.returncode == 0 else 1


def main(argv: Sequence[str] | None = None) -> int:
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    if arguments:
        sys.stderr.write("usage: check-p11-hermes.py\n")
        return 2
    try:
        present = locked_requirements_present(locked_requirements())
    except HermesGateError as exc:
        sys.stderr.write(f"P11 Hermes gate: {exc}\n")
        return 1
    if present:
        return run()
    if os.environ.get(CHILD_MARKER) == "1":
        sys.stderr.write("P11 Hermes gate: workload environment lacks the lock\n")
        return 1
    return run_in_workload_environment()


if __name__ == "__main__":
    raise SystemExit(main())
