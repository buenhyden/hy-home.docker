"""Shared fixtures for lifecycle responsibility tests."""

from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys

from tests.lib.gate.subprocess_support import gate_root_pass_fds


ROOT = pathlib.Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts/validation/check-document-corpus-lifecycle.py"
REGISTRY = ROOT / "docs/99.templates/registry.json"


spec = importlib.util.spec_from_file_location("document_corpus_lifecycle", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load {SCRIPT}")
lifecycle = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lifecycle
spec.loader.exec_module(lifecycle)


def run(*args: str, cwd: pathlib.Path) -> subprocess.CompletedProcess[str]:
    """Run a child while forwarding only a valid held repository descriptor."""

    pass_fds: tuple[int, ...] = ()
    if (
        len(args) > 1
        and pathlib.Path(args[1]).resolve() == SCRIPT
    ):
        pass_fds = gate_root_pass_fds(ROOT)
    return subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        pass_fds=pass_fds,
    )


def git(root: pathlib.Path, *args: str) -> str:
    result = run("git", *args, cwd=root)
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def init_repo(root: pathlib.Path) -> None:
    git(root, "init", "-q")
    git(root, "config", "core.hooksPath", "")
    git(root, "config", "user.email", "lifecycle@example.invalid")
    git(root, "config", "user.name", "Lifecycle Fixture")
    git(root, "symbolic-ref", "HEAD", "refs/heads/main")


def commit_all(root: pathlib.Path, message: str = "fixture") -> str:
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD")
