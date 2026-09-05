from __future__ import annotations

import ast
from collections import defaultdict
from copy import deepcopy
import json
import os
import posixpath
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[2]
BASELINE = "232effd9a5e00907bdbe30efc6665023fb2d07f4"
LEDGER = ROOT / "docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md"
OPERATIONS_MANIFEST_PATHS = (
    "scripts/lib/document_governance/operations_catalog.py",
    "scripts/validation/check-operations-catalog.py",
)
MIGRATION_ROOTS = (
    "docs/01.requirements",
    "docs/02.architecture",
    "docs/03.specs",
    "docs/04.execution",
    "docs/05.operations",
    "docs/90.references",
    "docs/98.archive",
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
    "docs/90.references/data/0082-llm-wiki-index/",
)
MUTATION_OVERRIDES = {
    "scripts/hooks/post-tool-validate.sh": "check-write",
    "scripts/knowledge/generate-llm-wiki.py": "check-write",
    "scripts/operations/gen-secrets.sh": "runtime",
    "scripts/operations/generate-compose-profile-service-coverage.sh": "check-write",
    "scripts/operations/generate-tech-stack-version-provenance.sh": "check-write",
    "scripts/operations/provider_surface_renderer.py": "check-write",
    "scripts/operations/rehearse-sample-service-delivery.sh": "runtime",
    "scripts/operations/sync-provider-surfaces.sh": "check-write",
    "scripts/lib/document_governance/metadata_validator.py": "check-write",
    "scripts/operations/sync-tech-stack-versions.sh": "check-write",
    "scripts/security/generate-supply-chain-sample-service-summary.sh": "check-write",
    "scripts/security/seed-grype-db-cache.sh": "runtime",
    "scripts/security/verify-sample-service-supply-chain.sh": "runtime",
    "scripts/validation/check-document-corpus-lifecycle.py": "check-write",
    "scripts/validation/check-document-metadata.py": "check-write",
    "scripts/validation/generate-audit-implementation-matrix.sh": "check-write",
    "scripts/validation/generate-security-automation-readiness.sh": "check-write",
    "scripts/validation/report-provider-hook-parity.sh": "check-write",
    "scripts/operations/rehearse-postgres-logical-upgrade.sh": "runtime",
    "scripts/validation/run-agent-precommit-all-files.sh": "check-write",
    "scripts/operations/check-compose-core-readiness.sh": "runtime",
    "scripts/validation/validate-docker-compose.sh": "runtime",
}
MANDATORY_DISPOSITIONS = {
    "scripts/hooks/post-tool-validate.sh": "retain",
    "scripts/knowledge/generate-llm-wiki.py": "retain",
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
KNOWN_TOMBSTONE_REPLACEMENTS = {
    "docs/98.archive/05.operations/guides/03-security/01.setup.md": (
        "docs/05.operations/03-security/ops-0016-vault/guide.md",
    ),
    "docs/98.archive/05.operations/guides/05-messaging/ksql-streaming.md": (
        "docs/05.operations/04-data/ops-0018-analytics-ksqldb/guide.md",
    ),
    "docs/98.archive/05.operations/guides/07-workflow/01.airflow-dag-dev.md": (
        "docs/05.operations/07-workflow/ops-0051-airflow-dag-basics/guide.md",
    ),
    "docs/98.archive/05.operations/guides/07-workflow/airbyte.md": (
        "docs/03.specs/0008-workflow/spec.md",
    ),
    "docs/98.archive/05.operations/guides/08-ai/01.llm-inference.md": (
        "docs/05.operations/08-ai/ops-0056-ollama/guide.md",
    ),
    "docs/98.archive/05.operations/guides/08-ai/local-llm-setup.md": (
        "docs/05.operations/08-ai/ops-0056-ollama/guide.md",
    ),
    "docs/98.archive/05.operations/guides/09-tooling/01.iac-automation.md": (
        "docs/05.operations/09-tooling/ops-0069-terrakube/guide.md",
        "docs/05.operations/09-tooling/ops-0068-terraform/guide.md",
    ),
    "docs/98.archive/05.operations/policies/07-workflow/airbyte.md": (
        "docs/03.specs/0008-workflow/spec.md",
    ),
    "docs/98.archive/05.operations/runbooks/07-workflow/airbyte.md": (
        "docs/03.specs/0008-workflow/spec.md",
    ),
}
LINK_FORM_BASELINE_DECLARATIONS = {
    "docs/98.archive/05.operations/guides/07-workflow/01.airflow-dag-dev.md": (
        "docs/05.operations/guides/07-workflow/airflow-dag-basics.md",
    ),
    "docs/98.archive/05.operations/guides/07-workflow/airbyte.md": (
        "docs/03.specs/008-workflow/spec.md",
    ),
    "docs/98.archive/05.operations/policies/07-workflow/airbyte.md": (
        "docs/03.specs/008-workflow/spec.md",
    ),
    "docs/98.archive/05.operations/runbooks/07-workflow/airbyte.md": (
        "docs/03.specs/008-workflow/spec.md",
    ),
}


def tracked_paths(*pathspecs: str) -> set[str]:
    paths = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", *pathspecs],
        cwd=ROOT,
        text=True,
        check=True,
        capture_output=True,
    ).stdout.splitlines()
    return {path for path in paths if (ROOT / path).is_file()}


def local_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git_text(path: str) -> str:
    return subprocess.run(
        ["git", "show", f"{BASELINE}:{path}"],
        cwd=ROOT,
        text=True,
        check=True,
        capture_output=True,
    ).stdout


def frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        return {}
    value = yaml.safe_load(text.split("---\n", 2)[1]) or {}
    return value if isinstance(value, dict) else {}


def markdown_code_paths(text: str) -> list[str]:
    return re.findall(r"`(docs/[^`]+)`", text)


def repository_docs_targets(text: str, source_path: str) -> list[str]:
    targets: list[str] = []
    declaration_pattern = re.compile(
        r"`(?P<code>docs/[^`]+)`|"
        r"\[[^]]*\]\((?P<link>[^)\s]+)(?:\s+[^)]*)?\)"
    )
    for match in declaration_pattern.finditer(text):
        raw_target = match.group("code") or match.group("link")
        candidate = raw_target.strip("<>").split("#", 1)[0]
        if not candidate or "://" in candidate:
            continue
        if candidate.startswith("/docs/"):
            candidate = candidate.lstrip("/")
        if not candidate.startswith("docs/"):
            candidate = posixpath.join(posixpath.dirname(source_path), candidate)
        candidate = posixpath.normpath(candidate).lstrip("/")
        if candidate.startswith("docs/") and candidate not in targets:
            targets.append(candidate)
    return targets


def declared_tombstone_replacements(text: str, tombstone_path: str) -> list[str]:
    for line in text.splitlines():
        if re.match(r"\|\s*Current replacement\s*\|", line, re.IGNORECASE):
            cells = line.strip().strip("|").split("|", 1)
            return repository_docs_targets(cells[1], tombstone_path)
    return []


def canonical_current_path(path: str) -> str:
    """Resolve the Migration 0003 predecessor spelling to its live Stage03 path."""

    return path.replace(
        "docs/03.specs/spec-0008-workflow/", "docs/03.specs/0008-workflow/"
    )


def replacement_preservation_errors(
    row: dict[str, object], translated: list[str]
) -> list[str]:
    if not translated:
        return ["declared-replacement-empty"]
    errors: list[str] = []
    if row["replacement"] is None:
        errors.append("replacement-null")
    elif canonical_current_path(str(row["replacement"])) != translated[0]:
        errors.append("primary-replacement-mismatch")
    evidence = canonical_current_path(f"{row['replacement']} {row['reason']}")
    if any(target not in evidence for target in translated):
        errors.append("translated-replacement-evidence-missing")
    return errors


def _python_imports_target(reference: str, target: str) -> bool:
    if not reference.endswith(".py") or not target.endswith(".py"):
        return False
    module = target.removesuffix(".py").replace("/", ".")
    sibling_module = PurePosixPath(target).stem
    same_directory = PurePosixPath(reference).parent == PurePosixPath(target).parent
    try:
        tree = ast.parse((ROOT / reference).read_text(encoding="utf-8"))
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == module for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if node.module == module or (
                same_directory and node.module == sibling_module
            ):
                return True
            package, _, member = module.rpartition(".")
            if node.module == package and any(
                alias.name == member for alias in node.names
            ):
                return True
    return False


MACHINE_REFERENCE_KEYS = frozenset(
    {
        "argv",
        "command",
        "commands",
        "entry",
        "entrypoint",
        "implementation",
        "path",
        "required_evidence_paths",
        "run",
        "script",
    }
)


def machine_config_proves_use(document: object, target: str, parent: str = "") -> bool:
    if isinstance(document, dict):
        return any(
            machine_config_proves_use(value, target, str(key))
            for key, value in document.items()
        )
    if isinstance(document, list):
        return any(
            machine_config_proves_use(value, target, parent) for value in document
        )
    if parent not in MACHINE_REFERENCE_KEYS or not isinstance(document, str):
        return False
    return bool(
        re.search(
            rf"(?<![A-Za-z0-9_./-]){re.escape(target)}(?![A-Za-z0-9_./-])",
            document,
        )
    )


def reference_proves_use(reference: str, target: str) -> bool:
    """Prove invocation/import evidence, not path inventory membership.

    Markdown evidence must put the path/basename in a command/code span. Source
    evidence must either import the Python module or name the path/basename in
    executable/fixture content. Inventory-only surfaces are rejected up front.
    """

    if reference == "scripts/manifest.yaml" or reference == ".github/CODEOWNERS":
        return False
    if reference.startswith(FORBIDDEN_EVIDENCE_PREFIXES):
        return False
    if _python_imports_target(reference, target):
        return True
    text = (ROOT / reference).read_text(encoding="utf-8")
    basename = PurePosixPath(target).name
    module_symbol = PurePosixPath(target).stem.replace("-", "_")
    token_present = target in text or basename in text
    if not token_present and reference.endswith(".py"):
        token_present = bool(re.search(rf"\b{re.escape(module_symbol)}\b", text))
    if not token_present:
        return False
    if reference.endswith(".md"):
        in_fence = False
        for line in text.splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if (target in line or basename in line) and (
                in_fence or "`" in line or re.search(r"\[[^]]*\]\([^)]*\)", line)
            ):
                return True
        return False
    if reference.endswith((".yaml", ".yml")):
        try:
            document = yaml.safe_load(text)
        except yaml.YAMLError:
            return False
        return machine_config_proves_use(document, target)
    if reference.endswith((".sh", ".bash")):
        return any(
            (target in line or basename in line) and not line.lstrip().startswith("#")
            for line in text.splitlines()
        )
    if reference.endswith(".py"):
        return any(
            marker in text
            for marker in (
                "subprocess.run",
                "subprocess.Popen",
                "runpy.run_path",
                "importlib",
            )
        )
    return target in text


def is_runbook_authority(path: str) -> bool:
    return bool(
        re.fullmatch(
            r"docs/05\.operations/catalog/[0-9]{2}-[a-z0-9-]+/"
            r"[0-9]{4}-[a-z0-9-]+/runbook\.md",
            path,
        )
    )


def stable_target_type(path: str) -> str | None:
    patterns = (
        (r"docs/01\.requirements/prd-[0-9]{4}-[^/]+\.md", "prd"),
        (r"docs/02\.architecture/descriptions/ad-[0-9]{4}-[^/]+\.md", "ad"),
        (r"docs/02\.architecture/decisions/adr-[0-9]{4}-[^/]+\.md", "adr"),
        (r"docs/03\.specs/[0-9]{4}-[^/]+/spec\.md", "spec"),
        (r"docs/03\.specs/spec-[0-9]{4}-[^/]+/spec\.md", "spec"),
        (r"docs/03\.specs/spec-[0-9]{4}-[^/]+/plan\.md", "plan"),
        (r"docs/03\.specs/spec-[0-9]{4}-[^/]+/task\.md", "task"),
        (
            r"docs/05\.operations/(?:[0-9]{2}-[^/]+)/(?:ops-[0-9]{4}-[^/]+)/(?:guide|policy|runbook)\.md",
            "ops-role",
        ),
        (
            r"docs/05\.operations/incidents/[0-9]{4}/inc-[0-9]{4}-[^/]+/(?:incident|postmortem)\.md",
            "event",
        ),
        (r"docs/05\.operations/releases/rel-[0-9]{4}-[^/]+/release\.md", "release"),
        (
            r"docs/90\.references/.*/ref-[0-9]{4}-[^/]+(?:\.(?:md|yaml|yml|json)|/README\.md)",
            "reference",
        ),
        (r"docs/98\.archive/changes/chg-[0-9]{4}-[^/]+/(?:plan|task)\.md", "change"),
        (
            r"docs/98\.archive/tombstones/(?:01\.requirements|02\.architecture|03\.specs|05\.operations)/[^/]+\.md",
            "tombstone",
        ),
        (r"docs/98\.archive/migrations/mig-[0-9]{4}-[^/]+\.md", "migration"),
    )
    if path == "docs/05.operations/README.md" or path.endswith("/README.md"):
        return "readme"
    for pattern, target_type in patterns:
        if re.fullmatch(pattern, path):
            return target_type
    return None



__all__ = tuple(name for name in globals() if not name.startswith("__"))
