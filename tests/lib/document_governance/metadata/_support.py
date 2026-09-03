"""Shared fixtures for metadata responsibility tests."""

from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys

import yaml

from tests.lib.gate.subprocess_support import gate_root_pass_fds


ROOT = pathlib.Path(__file__).resolve().parents[4]
CHECKER = ROOT / "scripts" / "validation" / "check-document-metadata.py"
REGISTRY = ROOT / "docs/99.templates/registry.json"

spec = importlib.util.spec_from_file_location("check_document_metadata", CHECKER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load checker module: {CHECKER}")
metadata = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = metadata
spec.loader.exec_module(metadata)


def current_profiles() -> dict[str, object]:
    """Project the current Registry into the metadata validator envelope."""

    return metadata.build_registry_profiles(metadata.load_registry(REGISTRY))


def write_doc(path: pathlib.Path, frontmatter: dict[str, object] | None, body: str = "# Fixture\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if frontmatter is None:
        path.write_text(body, encoding="utf-8")
        return
    if isinstance(frontmatter.get("artifact_type"), str):
        canonical: dict[str, object] = {}
        for key, value in frontmatter.items():
            canonical[key] = value
            if key == "parent_ids":
                canonical["created"] = frontmatter.get("created", "2026-08-07")
                canonical["updated"] = frontmatter.get("updated", "2026-08-07")
        frontmatter = canonical
    rendered = yaml.safe_dump(frontmatter, sort_keys=False).rstrip()
    path.write_text(f"---\n{rendered}\n---\n\n{body}", encoding="utf-8")


def git(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def init_git(root: pathlib.Path) -> None:
    initialized = git(root, "init", "-q")
    if initialized.returncode != 0:
        raise RuntimeError(initialized.stderr)
    git(root, "config", "core.hooksPath", "")
    git(root, "config", "user.name", "Metadata Fixture")
    git(root, "config", "user.email", "metadata@example.invalid")
    if git(root, "rev-parse", "--verify", "-q", "HEAD").returncode == 0:
        named = git(root, "branch", "-M", "main")
    else:
        named = git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    if named.returncode != 0:
        raise RuntimeError(named.stderr)
    registry = root / "docs/99.templates/registry.json"
    registry.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REGISTRY, registry)

def copy_registry_contract_fixture(root: pathlib.Path) -> pathlib.Path:
    """Copy the current Registry, schemas, and registered template sources."""

    values = json.loads(REGISTRY.read_text(encoding="utf-8"))
    relative_paths = {
        pathlib.Path("README.md"),
        pathlib.Path("docs/05.operations/incidents/README.md"),
        pathlib.Path("docs/99.templates/registry.json"),
        pathlib.Path("docs/99.templates/contracts/document-profile.schema.json"),
        pathlib.Path("docs/99.templates/contracts/frontmatter.schema.json"),
        # The catalog is a registered contract surface, so a fixture that holds
        # template sources without it is not a valid Stage 99 tree.
        pathlib.Path(values["template_catalog"]),
        *(
            pathlib.Path(role["source"])
            for role in values["template_roles"].values()
        ),
    }
    for relative_path in sorted(relative_paths):
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative_path, target)
    init_git(root)
    staged = git(root, "add", ".")
    if staged.returncode != 0:
        raise RuntimeError(staged.stderr)
    if git(root, "diff", "--cached", "--quiet").returncode != 0:
        committed = git(root, "commit", "-qm", "registry contract fixture")
        if committed.returncode != 0:
            raise RuntimeError(committed.stderr or committed.stdout)
    return root / "docs/99.templates/registry.json"


def body_with_headings(*headings: str) -> str:
    """Build a concrete target body for tests whose subject is not body validation."""

    sections = "\n\n".join(f"{heading}\n\nFixture content." for heading in headings)
    return f"# Fixture\n\n{sections}\n"

REQUIREMENT_TARGET_BODY = body_with_headings(
    "## Problem and Goals",
    "## Stakeholders and User Needs",
    "## Functional Requirements",
    "## Non-functional Requirements",
    "## Constraints",
    "## Acceptance Criteria",
    "## Traceability",
)

POLICY_TARGET_BODY = body_with_headings(
    "## Purpose",
    "## Scope",
    "## Policy Statements",
    "## Enforcement",
    "## Exceptions",
    "## Verification",
    "## Traceability",
)

def _materialised_profiles() -> pathlib.Path:
    """Return the sole current document-profile authority."""

    return REGISTRY


def run_checker(
    root: pathlib.Path,
    mode: str = "report",
    *extra: str,
    env: dict[str, str] | None = None,
    profiles: pathlib.Path | None = None,
) -> subprocess.CompletedProcess[str]:
    resolved_profiles = _materialised_profiles() if profiles is None else profiles
    return _run_checker_process(
        root,
        mode,
        extra,
        env,
        resolved_profiles,
        gate_root_pass_fds(ROOT),
    )


def _run_checker_process(
    root: pathlib.Path,
    mode: str,
    extra: tuple[str, ...],
    env: dict[str, str] | None,
    resolved_profiles: pathlib.Path,
    descriptors: tuple[int, ...],
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(CHECKER),
            "--root",
            str(root),
            "--profiles",
            str(resolved_profiles),
            "--mode",
            mode,
            *extra,
        ],
        cwd=ROOT,
        env={**os.environ, **(env or {})},
        pass_fds=descriptors,
        capture_output=True,
        text=True,
        check=False,
    )
