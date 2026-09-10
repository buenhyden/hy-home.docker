from __future__ import annotations

import ast
import importlib.util
import sys
from copy import deepcopy
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[2]
OPERATIONS_MANIFEST_PATHS = (
    "scripts/lib/document_governance/operations_catalog.py",
    "scripts/validation/check-operations-catalog.py",
)
REQUIRED_FIELDS = frozenset(
    {
        "path",
        "kind",
        "authority",
        "lifecycle",
        "mutation",
        "consumers",
        "disposition",
        "successor",
        "tests",
    }
)
KINDS = frozenset(
    {
        "contract",
        "dependency-manifest",
        "generator",
        "hook",
        "library",
        "operations",
        "runner",
        "validator",
    }
)
LIFECYCLES = frozenset({"active", "transition"})
MUTATIONS = frozenset({"none", "check-write", "runtime"})
DISPOSITIONS = frozenset({"retain", "merge", "delete", "rewrite"})
FORBIDDEN_EVIDENCE_PREFIXES = (
    "graphify-out/",
    "docs/98.archive/",
    "docs/04.execution/",
)
MUTATION_OVERRIDES = {
    "scripts/hooks/post-tool-validate.sh": "check-write",
    "scripts/operations/gen-secrets.sh": "runtime",
    "scripts/operations/provider_surface_renderer.py": "check-write",
    "scripts/operations/rehearse-sample-service-delivery.sh": "runtime",
    "scripts/lib/document_governance/metadata_validator.py": "check-write",
    "scripts/operations/sync-tech-stack-versions.sh": "check-write",
    "scripts/security/seed-grype-db-cache.sh": "runtime",
    "scripts/security/verify-sample-service-supply-chain.sh": "runtime",
    "scripts/validation/check-document-corpus-lifecycle.py": "check-write",
    "scripts/validation/check-document-metadata.py": "check-write",
    "scripts/operations/rehearse-postgres-logical-upgrade.sh": "runtime",
    "scripts/validation/run-agent-precommit-all-files.sh": "check-write",
    "scripts/operations/check-compose-core-readiness.sh": "runtime",
    "scripts/validation/validate-docker-compose.sh": "runtime",
}
MANDATORY_DISPOSITIONS = {
    "scripts/hooks/post-tool-validate.sh": "retain",
}
TASK12_RETIRED_SCRIPTS = frozenset(
    {
        "scripts/hooks/patch-graphify-post-commit.sh",
        "scripts/knowledge/generate-llm-wiki-coverage.sh",
        "scripts/knowledge/generate-llm-wiki-index.sh",
        "scripts/validation/check-repo-contracts.sh",
        "scripts/validation/recommend-gap-routing.sh",
        "scripts/validation/recommend-qa-gates.sh",
    }
)


def tracked_paths(*pathspecs: str) -> set[str]:
    paths = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", *pathspecs],
        cwd=ROOT,
        text=True,
        check=True,
        capture_output=True,
    ).stdout.splitlines()
    return {path for path in paths if (ROOT / path).is_file()}


MANIFEST_CHECKER = ROOT / "scripts/validation/check-script-manifest.py"
_CHECKER = None


def load_manifest_checker():
    """Load the gate checker once; it owns manifest evidence semantics."""

    global _CHECKER
    if _CHECKER is None:
        spec = importlib.util.spec_from_file_location(
            "check_script_manifest", MANIFEST_CHECKER
        )
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {MANIFEST_CHECKER}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        _CHECKER = module
    return _CHECKER


def reference_proves_use(reference: str, target: str, *, is_test: bool = False) -> bool:
    """Answer the gate's own evidence question about a declared reference.

    The grammar has a single owner. Only the inventory surfaces these manifest
    tests own are rejected here: they list every tracked path by construction,
    so naming one there is membership rather than use.
    """

    if reference in {"scripts/manifest.yaml", ".github/CODEOWNERS"}:
        return False
    if reference.startswith(FORBIDDEN_EVIDENCE_PREFIXES):
        return False
    text = (ROOT / reference).read_text(encoding="utf-8")
    return load_manifest_checker()._reference_proves_use(
        reference, text, target, is_test=is_test
    )


def is_runbook_authority(path: str) -> bool:
    return bool(
        re.fullmatch(
            r"docs/05\.operations/catalog/[0-9]{2}-[a-z0-9-]+/"
            r"[0-9]{4}-[a-z0-9-]+/runbook\.md",
            path,
        )
    )


__all__ = tuple(name for name in globals() if not name.startswith("__"))
