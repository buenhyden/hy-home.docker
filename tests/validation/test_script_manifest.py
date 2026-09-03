from __future__ import annotations

import ast
from collections import defaultdict
from copy import deepcopy
import importlib.util
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath

import yaml


ROOT = Path(__file__).resolve().parents[2]
BASELINE = "232effd9a5e00907bdbe30efc6665023fb2d07f4"
MANIFEST = ROOT / "scripts/manifest.yaml"
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
PUBLIC_SUITE_NAMES = frozenset(
    {
        "agent-governance",
        "document-contract",
        "document-graph",
        "document-lifecycle",
        "operations",
        "repository-integrity",
    }
)
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
    "scripts/lib/ops/rehearse-postgres-logical-upgrade.sh": "runtime",
    "scripts/validation/run-agent-precommit-all-files.sh": "check-write",
    "scripts/validation/run-compose-core-readiness.sh": "runtime",
    "scripts/validation/compose-core-readiness.lib.sh": "runtime",
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


def load_manifest_checker():
    path = ROOT / "scripts/validation/check-script-manifest.py"
    spec = importlib.util.spec_from_file_location("check_script_manifest", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def tracked_paths(pathspec: str) -> set[str]:
    paths = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", pathspec],
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


class ScriptManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tracked = tracked_paths("scripts")
        cls.repository_paths = tracked_paths(":(top)")
        cls.manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        cls.rows = cls.manifest["files"]
        cls.rows_by_path = {row["path"]: row for row in cls.rows}
        ledger_text = (
            LEDGER.read_text(encoding="utf-8")
            .split("```yaml\n", 1)[1]
            .split("```", 1)[0]
        )
        cls.ledger_rows = yaml.safe_load(ledger_text)["records"]
        cls.ledger_by_path = {row["legacy_path"]: row for row in cls.ledger_rows}

    def test_every_tracked_script_has_one_manifest_record(self) -> None:
        declared = [row["path"] for row in self.rows]
        self.assertEqual(len(declared), len(set(declared)))
        self.assertEqual(self.tracked, set(declared))

    def test_stage90_generators_declare_exact_destinations_and_explicit_write_mode(
        self,
    ) -> None:
        for script, output in (
            (
                "scripts/operations/generate-compose-profile-service-coverage.sh",
                "docs/90.references/data/0059-compose-profile-service-coverage/README.md",
            ),
            (
                "scripts/operations/generate-tech-stack-version-provenance.sh",
                "docs/90.references/data/0061-tech-stack-version-provenance/README.md",
            ),
            (
                "scripts/validation/generate-audit-implementation-matrix.sh",
                "docs/90.references/data/0065-audit-implementation-matrix/README.md",
            ),
            (
                "scripts/validation/generate-security-automation-readiness.sh",
                "docs/90.references/data/0078-security-automation-readiness/README.md",
            ),
            (
                "scripts/security/generate-supply-chain-sample-service-summary.sh",
                "docs/90.references/data/0079-supply-chain-sample-service/README.md",
            ),
        ):
            with self.subTest(script=script):
                row = self.rows_by_path[script]
                self.assertEqual([output], row["outputs"])
                self.assertEqual(["bash", script, "--check"], row["check_command"])
                result = subprocess.run(
                    ["bash", script, "--help"],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("--write", result.stdout)

    def test_stage90_generators_require_write_and_touch_only_declared_output(
        self,
    ) -> None:
        scripts = (
            "scripts/operations/generate-compose-profile-service-coverage.sh",
            "scripts/operations/generate-tech-stack-version-provenance.sh",
            "scripts/validation/generate-audit-implementation-matrix.sh",
            "scripts/validation/generate-security-automation-readiness.sh",
            "scripts/security/generate-supply-chain-sample-service-summary.sh",
            "scripts/validation/report-provider-hook-parity.sh",
        )
        for script in scripts:
            with (
                self.subTest(script=script),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                inputs = {script}
                fixture_sources: dict[str, Path] = {}
                if "tech-stack" in script:
                    (root / "infra").mkdir()
                    (root / "infra/tech-stack.versions.json").write_text(
                        json.dumps(
                            {
                                "entries": [
                                    {
                                        "component": "fixture",
                                        "images": ["fixture:1"],
                                        "compose_files": [
                                            "infra/docker-compose.fixture.yml"
                                        ],
                                    }
                                ]
                            }
                        )
                    )
                    (root / "infra/image-tag-policy.exceptions.json").write_text("{}")
                    (root / "infra/docker-compose.fixture.yml").write_text(
                        "services:\n  fixture:\n    image: fixture:1\n"
                    )
                elif "audit-implementation" in script:
                    inputs.update(
                        {
                            "scripts/validation/audit_criterion_contract.py",
                            "scripts/validation/check-agentic-audit-semantic-freshness.py",
                            "scripts/validation/agentic-audit-semantic-contract.json",
                        }
                    )
                    semantic = json.loads(
                        (
                            ROOT
                            / "scripts/validation/agentic-audit-semantic-contract.json"
                        ).read_text()
                    )
                    inputs.update(
                        path.relative_to(ROOT).as_posix()
                        for path in (ROOT / "docs/90.references/audits").rglob("*.md")
                    )
                    inputs.add(semantic["task_evidence"])
                    fixture_sources[semantic["task_evidence"]] = (
                        ROOT / "tests/fixtures/agentic-audit/task-evidence.md"
                    )
                    inputs.update(
                        path
                        for assertion in semantic["assertions"]
                        for path in assertion["required_evidence_paths"]
                    )
                elif "supply-chain" in script:
                    inputs.update(
                        {
                            "scripts/validation/check-supply-chain-policy.py",
                            "scripts/lib/supply_chain/grype_db_seed.py",
                            "examples/sample-web-service/Dockerfile",
                        }
                    )
                    inputs.update(
                        path.relative_to(ROOT).as_posix()
                        for path in (ROOT / "infra").glob("supply-chain*.json")
                    )
                    inputs.update(
                        path.relative_to(ROOT).as_posix()
                        for path in (ROOT / "tests/fixtures/supply-chain").rglob("*")
                        if path.is_file()
                    )
                elif "hook-parity" in script:
                    from tests.validation.test_provider_hook_parity import copy_fixture

                    copy_fixture(root)
                self.assertLess(
                    len(inputs), 180, "fixture must remain a bounded producer input set"
                )
                for relative in sorted(inputs):
                    source = fixture_sources.get(relative, ROOT / relative)
                    target = root / relative
                    self.assertTrue(source.is_file(), relative)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
                output = self.rows_by_path[script]["outputs"][0]
                target = root / output
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("stale output\n", encoding="utf-8")
                subprocess.run(
                    ["git", "init", "-q"], cwd=root, check=True, capture_output=True
                )
                subprocess.run(
                    ["git", "add", "."], cwd=root, check=True, capture_output=True
                )
                environment = {
                    **os.environ,
                    "PYTHONPATH": str(ROOT),
                    "PYTHONDONTWRITEBYTECODE": "1",
                }
                environment.pop("HYHOME_CI_GATE_ROOT", None)
                command = ["bash", str(root / script)]
                extra = ["--root", str(root)] if "hook-parity" in script else []

                def snapshot():
                    return {
                        path.relative_to(root).as_posix(): path.read_bytes()
                        for path in root.rglob("*")
                        if path.is_file() and ".git" not in path.relative_to(root).parts
                    }

                before = snapshot()
                for mode in ([], ["--check"]):
                    result = subprocess.run(
                        [*command, *mode, *extra],
                        cwd=root,
                        env=environment,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    self.assertNotEqual(0, result.returncode, script)
                    self.assertEqual(before, snapshot(), script)
                result = subprocess.run(
                    [*command, "--write", *extra],
                    cwd=root,
                    env=environment,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                after = snapshot()
                self.assertEqual(
                    {output},
                    {
                        path
                        for path in before.keys() | after.keys()
                        if before.get(path) != after.get(path)
                    },
                )
                for mode in ([], ["--check"]):
                    result = subprocess.run(
                        [*command, *mode, *extra],
                        cwd=root,
                        env=environment,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    self.assertEqual(
                        0, result.returncode, result.stdout + result.stderr
                    )
                    self.assertEqual(after, snapshot())

    def test_task12_retires_only_the_proven_successor_scripts(self) -> None:
        self.assertTrue(TASK12_RETIRED_SCRIPTS.isdisjoint(self.tracked))
        self.assertTrue(TASK12_RETIRED_SCRIPTS.isdisjoint(self.rows_by_path))
        self.assertIn(
            "scripts/operations/rehearse-sample-service-delivery.sh",
            self.tracked,
        )

    def test_records_are_sorted_and_use_the_complete_schema(self) -> None:
        paths = [row["path"] for row in self.rows]
        self.assertEqual(paths, sorted(paths))
        for row in self.rows:
            expected_fields = REQUIRED_FIELDS
            if (
                row["kind"] in {"generator", "validator"}
                and row["mutation"] == "check-write"
                and row["disposition"] == "retain"
                and ("check_command" in row or "outputs" in row)
            ):
                expected_fields = REQUIRED_FIELDS | {"check_command", "outputs"}
            if row["kind"] == "validator":
                expected_fields = expected_fields | {
                    "public_suites",
                    "execution_contexts",
                }
                if row.get("execution_argv"):
                    expected_fields = expected_fields | {"execution_argv"}
            self.assertEqual(expected_fields, set(row))
            self.assertIn(row["kind"], KINDS)
            self.assertIn(row["lifecycle"], LIFECYCLES)
            self.assertIn(row["mutation"], MUTATIONS)
            self.assertIn(row["disposition"], DISPOSITIONS)
            if row["kind"] == "validator":
                self.assertEqual(1, len(row["public_suites"]))
                self.assertIn(row["public_suites"][0], PUBLIC_SUITE_NAMES)
            self.assertIsInstance(row["authority"], str)
            self.assertTrue(row["authority"])
            self.assertNotEqual(row["authority"], "sdlc-taxonomy-convergence")
            self.assertIn(row["authority"], self.repository_paths)

    def test_consumer_successor_and_test_references_are_evidenced(self) -> None:
        for row in self.rows:
            with self.subTest(path=row["path"]):
                self.assertIsInstance(row["consumers"], list)
                self.assertEqual(row["consumers"], sorted(set(row["consumers"])))
                self.assertIsInstance(row["tests"], list)
                self.assertEqual(row["tests"], sorted(set(row["tests"])))
                for reference in [*row["consumers"], *row["tests"]]:
                    self.assertIn(reference, self.repository_paths)
                    self.assertTrue((ROOT / reference).is_file())
                    self.assertFalse(reference.startswith(FORBIDDEN_EVIDENCE_PREFIXES))
                    self.assertTrue(
                        reference_proves_use(reference, row["path"]),
                        f"{reference} does not invoke/import {row['path']}",
                    )
                successor = row["successor"]
                if row["disposition"] == "retain":
                    self.assertIsNone(successor)
                else:
                    self.assertIsInstance(successor, str)
                    self.assertIn(successor, self.repository_paths)
                if row["disposition"] == "retain" and row["kind"] != "library":
                    self.assertTrue(row["consumers"])
                if row["disposition"] == "retain" and row["kind"] not in {
                    "contract",
                    "dependency-manifest",
                }:
                    self.assertTrue(row["tests"])
                if row["mutation"] == "runtime" and row["disposition"] == "retain":
                    self.assertTrue(is_runbook_authority(row["authority"]))
                    self.assertTrue(row["tests"])
                if (
                    row["kind"] in {"generator", "validator"}
                    and row["mutation"] == "check-write"
                    and row["disposition"] == "retain"
                    and "check_command" in row
                ):
                    self.assertIn("--check", row["check_command"])
                    self.assertNotIn("--write", row["check_command"])
                    self.assertTrue(row["outputs"])

    def test_manifest_inventory_is_not_a_consumer_of_other_scripts(self) -> None:
        offenders = [
            row["path"]
            for row in self.rows
            if row["path"] != "scripts/manifest.yaml"
            and "scripts/manifest.yaml" in row["consumers"]
        ]
        self.assertEqual([], offenders)

    def test_taxonomy_library_declares_exact_real_consumers_and_tests(self) -> None:
        row = self.rows_by_path["scripts/lib/document_governance/taxonomy.py"]
        self.assertEqual("retain", row["disposition"])
        self.assertEqual(
            [
                "scripts/lib/document_governance/metadata/lifecycle.py",
                "scripts/lib/document_governance/metadata/profile.py",
            ],
            row["consumers"],
        )
        self.assertEqual(
            ["tests/lib/document_governance/test_taxonomy.py"],
            row["tests"],
        )

    def test_python_import_evidence_recognizes_package_member_imports(self) -> None:
        adapter = "scripts/validation/check-document-metadata.py"
        self.assertTrue(
            _python_imports_target(
                adapter,
                "scripts/lib/document_governance/metadata_contract.py",
            )
        )
        self.assertTrue(
            _python_imports_target(
                adapter,
                "scripts/lib/document_governance/metadata_validator.py",
            )
        )
        self.assertFalse(
            _python_imports_target(
                adapter,
                "scripts/lib/target_surface/target_surface_contract.py",
            )
        )

    def test_mutation_classes_follow_observed_script_behavior(self) -> None:
        for row in self.rows:
            with self.subTest(path=row["path"]):
                expected = MUTATION_OVERRIDES.get(row["path"], "none")
                self.assertEqual(expected, row["mutation"])
                if (
                    row["kind"] in {"generator", "validator"}
                    and row["mutation"] == "check-write"
                    and row["disposition"] == "retain"
                    and "check_command" in row
                ):
                    self.assertEqual(row["path"], row["check_command"][1])

    def test_plan_mandatory_dispositions_and_high_risk_operations(self) -> None:
        for path, disposition in MANDATORY_DISPOSITIONS.items():
            with self.subTest(path=path):
                self.assertEqual(disposition, self.rows_by_path[path]["disposition"])

        for path in (
            "scripts/operations/gen-secrets.sh",
            "scripts/security/seed-grype-db-cache.sh",
        ):
            with self.subTest(path=path):
                row = self.rows_by_path[path]
                if row["disposition"] == "retain":
                    self.assertTrue(row["consumers"])
                    self.assertTrue(row["tests"])
                    self.assertTrue(is_runbook_authority(row["authority"]))

    def test_postgres_logical_upgrade_uses_the_mirrored_ops_test(self) -> None:
        postgres = self.rows_by_path[
            "scripts/lib/ops/rehearse-postgres-logical-upgrade.sh"
        ]
        self.assertEqual("retain", postgres["disposition"])
        self.assertEqual(
            "docs/05.operations/catalog/04-data/0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md",
            postgres["authority"],
        )
        self.assertEqual(
            [postgres["authority"]],
            postgres["consumers"],
        )
        self.assertEqual(
            ["tests/lib/ops/test_postgres_logical_upgrade_rehearsal.py"],
            postgres["tests"],
        )

    def test_authority_is_specific_and_runtime_retention_is_runbook_bound(self) -> None:
        unrelated = {
            "docs/05.operations/runbooks/03-security/vault.md",
            "docs/05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md",
        }
        for row in self.rows:
            with self.subTest(path=row["path"]):
                authority = row["authority"]
                self.assertFalse(
                    authority.startswith("docs/03.specs/"),
                    "script authority must be a current policy, architecture, "
                    "operations, registry, or workflow owner",
                )
                authority_text = (ROOT / authority).read_text(encoding="utf-8")
                basename = PurePosixPath(row["path"]).name
                if (
                    authority in unrelated
                    and basename not in authority_text
                    and row["path"] not in authority_text
                ):
                    self.fail(
                        f"blanket authority {authority} does not govern {row['path']}"
                    )
                if row["mutation"] == "runtime" and row["disposition"] == "retain":
                    self.assertTrue(is_runbook_authority(authority))
                    self.assertTrue(
                        basename in authority_text or row["path"] in authority_text,
                        f"runtime Runbook does not name {row['path']}",
                    )
                elif row["mutation"] == "runtime" and not is_runbook_authority(
                    authority
                ):
                    self.assertNotEqual("retain", row["disposition"])
                    self.assertEqual(row["path"], row["successor"])

    def test_operations_implementation_and_gate_use_the_registry_authority(
        self,
    ) -> None:
        for path in OPERATIONS_MANIFEST_PATHS:
            with self.subTest(path=path):
                row = self.rows_by_path[path]
                self.assertEqual("docs/99.templates/registry.json", row["authority"])
                self.assertNotIn("current_authorities", row)
                self.assertNotIn("semantic_witnesses", row)

    def test_runbook_authority_accepts_only_canonical_catalog_leaf_shape(self) -> None:
        self.assertTrue(
            is_runbook_authority(
                "docs/05.operations/catalog/04-data/"
                "0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md"
            )
        )
        rejected = (
            "docs/05.operations/04-data/ops-0032-example/runbook.md",
            "docs/05.operations/runbooks/04-data/example.md",
            "docs/05.operations/catalog/4-data/ops-0032-example/runbook.md",
            "docs/05.operations/catalog/04-data/ops-032-example/runbook.md",
            "docs/05.operations/catalog/04-data/ops-0032-example/guide.md",
            "docs/05.operations/catalog/04-data/nested/ops-0032-example/runbook.md",
        )
        for path in rejected:
            with self.subTest(path=path):
                self.assertFalse(is_runbook_authority(path))

    def test_scripts_readme_preserves_invocation_warnings(self) -> None:
        text = (ROOT / "scripts/README.md").read_text(encoding="utf-8")
        compact = re.sub(r"\s+", " ", text)
        self.assertIn("Do not invoke a `mutation: runtime` row", compact)
        self.assertIn("Do not invoke a default-write generator without", compact)
        self.assertIn("semantic invocation/import evidence", compact)

    def test_ledger_has_one_complete_sorted_row_for_every_migration_document(
        self,
    ) -> None:
        rows = self.ledger_rows
        expected = set(
            subprocess.run(
                [
                    "git",
                    "ls-tree",
                    "-r",
                    "--name-only",
                    BASELINE,
                    "--",
                    *MIGRATION_ROOTS,
                ],
                cwd=ROOT,
                text=True,
                check=True,
                capture_output=True,
            ).stdout.splitlines()
        )
        declared = [row["legacy_path"] for row in rows]
        self.assertEqual(declared, sorted(declared))
        self.assertEqual(len(declared), len(set(declared)))
        self.assertEqual(expected, set(declared))
        required = {
            "legacy_path",
            "stable_path",
            "artifact_id",
            "action",
            "replacement",
            "source_commit",
            "reason",
        }
        destructive = {"merge", "delete"}
        for row in rows:
            with self.subTest(path=row["legacy_path"]):
                self.assertEqual(required, set(row))
                self.assertIn(
                    row["action"],
                    {"archive", "delete", "merge", "move", "retain", "rewrite"},
                )
                self.assertEqual(
                    BASELINE,
                    row["source_commit"],
                )
                self.assertTrue(row["reason"])
                if row["action"] == "delete":
                    self.assertIsNone(row["stable_path"])
                else:
                    self.assertIsInstance(row["stable_path"], str)
                    self.assertTrue(row["stable_path"])
                if row["action"] in destructive:
                    self.assertIsInstance(row["replacement"], str)
                    self.assertTrue(row["replacement"])
                elif row["action"] != "archive":
                    self.assertIsNone(row["replacement"])

    def test_ledger_targets_match_stable_typed_taxonomy(self) -> None:
        for row in self.ledger_rows:
            with self.subTest(path=row["legacy_path"]):
                target = row["stable_path"]
                replacement = row["replacement"]
                if target is not None:
                    self.assertIsNotNone(stable_target_type(target), target)
                    parts = PurePosixPath(target).parts
                    self.assertNotIn("docs/04.execution", target)
                    self.assertNotIn("README.md/", target)
                    self.assertFalse(
                        any(re.fullmatch(r"[0-9]{4}", part) for part in parts)
                    )
                    self.assertFalse(
                        any(
                            re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-", part)
                            for part in parts
                        )
                    )
                    self.assertFalse(
                        target.startswith(
                            (
                                "docs/05.operations/guides/",
                                "docs/05.operations/policies/",
                                "docs/05.operations/runbooks/",
                            )
                        )
                    )
                if replacement is not None:
                    self.assertNotEqual(row["legacy_path"], replacement)
                    if row["action"] == "archive":
                        self.assertNotEqual(target, replacement)
                    self.assertIsNotNone(stable_target_type(replacement), replacement)

                if target and "/changes/chg-" in target:
                    match = re.fullmatch(
                        r"docs/98\.archive/changes/chg-([0-9]{4})-[^/]+/(plan|task)\.md",
                        target,
                    )
                    self.assertIsNotNone(match)
                    identity, role = match.groups()
                    if role == "plan":
                        self.assertEqual(f"plan-{identity}", row["artifact_id"])
                    else:
                        self.assertRegex(
                            str(row["artifact_id"]), rf"^task-{identity}-[0-9]{{2}}$"
                        )

    def test_ledger_artifact_ids_match_target_profile_identities(self) -> None:
        direct_profiles = {
            "prd": (r".*/prd-([0-9]{4})-[^/]+\.md", "prd"),
            "ad": (r".*/ad-([0-9]{4})-[^/]+\.md", "ad"),
            "adr": (r".*/adr-([0-9]{4})-[^/]+\.md", "adr"),
            "spec": (r".*/spec-([0-9]{4})-[^/]+/spec\.md", "spec"),
            "event": (r".*/inc-([0-9]{4})-[^/]+/incident\.md", "inc"),
            "release": (r".*/rel-([0-9]{4})-[^/]+/release\.md", "rel"),
            "reference": (
                r".*/ref-([0-9]{4})-[^/]+(?:\.(?:md|yaml|yml|json)|/README\.md)",
                "ref",
            ),
            "migration": (r".*/mig-([0-9]{4})-[^/]+\.md", "mig"),
        }
        for row in self.ledger_rows:
            target = row["stable_path"]
            if target is None:
                continue
            target_type = stable_target_type(target)
            artifact_id = row["artifact_id"]
            with self.subTest(path=row["legacy_path"], target=target):
                if target_type == "readme":
                    self.assertIsNone(artifact_id)
                    continue
                self.assertIsInstance(artifact_id, str)
                if target_type in direct_profiles:
                    pattern, prefix = direct_profiles[target_type]
                    match = re.fullmatch(pattern, target)
                    self.assertIsNotNone(match)
                    self.assertEqual(f"{prefix}-{match.group(1)}", artifact_id)
                elif target_type in {"plan", "task"}:
                    match = re.fullmatch(
                        r"docs/03\.specs/spec-([0-9]{4})-[^/]+/(plan|task)\.md",
                        target,
                    )
                    self.assertIsNotNone(match)
                    identity, role = match.groups()
                    expected = (
                        f"plan-{identity}" if role == "plan" else f"task-{identity}-01"
                    )
                    self.assertEqual(expected, artifact_id)
                elif target_type == "ops-role":
                    match = re.fullmatch(
                        r"docs/05\.operations/[^/]+/ops-([0-9]{4})-[^/]+/(guide|policy|runbook)\.md",
                        target,
                    )
                    self.assertIsNotNone(match)
                    identity, role = match.groups()
                    self.assertEqual(f"{role}-{identity}", artifact_id)
                elif target_type == "change":
                    match = re.fullmatch(
                        r"docs/98\.archive/changes/chg-([0-9]{4})-[^/]+/(plan|task)\.md",
                        target,
                    )
                    self.assertIsNotNone(match)
                    identity, role = match.groups()
                    if role == "plan":
                        self.assertEqual(f"plan-{identity}", artifact_id)
                    else:
                        self.assertRegex(artifact_id, rf"^task-{identity}-[0-9]{{2}}$")
                    target_path = ROOT / target
                    if target_path.is_file():
                        target_metadata = frontmatter(
                            target_path.read_text(encoding="utf-8")
                        )
                        self.assertEqual(
                            target_metadata.get("artifact_id"), artifact_id
                        )
                elif target_type == "tombstone":
                    filename = PurePosixPath(target).stem
                    self.assertTrue(
                        filename.startswith(f"{artifact_id}-")
                        or filename == artifact_id
                    )

    def test_active_and_draft_sources_never_route_to_archive(self) -> None:
        for row in self.ledger_rows:
            metadata = frontmatter(git_text(row["legacy_path"]))
            if metadata.get("status") not in {"active", "draft"}:
                continue
            with self.subTest(path=row["legacy_path"]):
                self.assertNotEqual("archive", row["action"])
                self.assertFalse(str(row["stable_path"]).startswith("docs/98.archive/"))

    def test_semantic_helpers_reject_known_bad_mutations(self) -> None:
        taxonomy = "scripts/lib/document_governance/taxonomy.py"
        self.assertFalse(reference_proves_use("scripts/manifest.yaml", taxonomy))
        self.assertFalse(reference_proves_use(".github/CODEOWNERS", taxonomy))
        self.assertIsNone(stable_target_type("docs/04.execution/plans/plan.md"))
        self.assertIsNone(stable_target_type("docs/03.specs/spec-131-example/spec.md"))
        self.assertIsNone(stable_target_type("docs/05.operations/runbooks/example.md"))

    def test_tombstones_are_terminal_and_only_name_active_replacements(self) -> None:
        for row in self.ledger_rows:
            if row["action"] != "archive":
                continue
            with self.subTest(path=row["legacy_path"]):
                metadata = frontmatter(git_text(row["legacy_path"]))
                self.assertIn(
                    metadata.get("status"), {"completed", "superseded", "archived"}
                )
                self.assertTrue(
                    str(row["stable_path"]).startswith("docs/98.archive/tombstones/")
                )
                replacement = row["replacement"]
                if replacement is not None:
                    self.assertFalse(str(replacement).startswith("docs/98.archive/"))

    def test_link_form_tombstone_replacements_are_parsed(self) -> None:
        for legacy_path, expected in LINK_FORM_BASELINE_DECLARATIONS.items():
            with self.subTest(path=legacy_path):
                self.assertEqual(
                    expected,
                    tuple(
                        declared_tombstone_replacements(
                            git_text(legacy_path), legacy_path
                        )
                    ),
                )
        self.assertEqual(
            ["docs/05.operations/example.md"],
            repository_docs_targets(
                "[local](../05.operations/example.md#procedure) "
                "[external](https://example.com/docs/ignored.md)",
                "docs/98.archive/tombstone.md",
            ),
        )

    def test_baseline_tombstone_replacements_are_preserved_as_stable_targets(
        self,
    ) -> None:
        index_replacements: dict[str, list[str]] = {}
        index_path = "docs/98.archive/README.md"
        for line in git_text(index_path).splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 4:
                continue
            archived_paths = repository_docs_targets(cells[1], index_path)
            replacements = repository_docs_targets(cells[3], index_path)
            if (
                len(archived_paths) == 1
                and archived_paths[0].startswith("docs/98.archive/05.operations/")
                and replacements
            ):
                index_replacements[archived_paths[0]] = replacements

        checked: set[str] = set()
        self.assertEqual(9, len(index_replacements))
        for legacy_path in sorted(index_replacements):
            self.assertIn(legacy_path, self.ledger_by_path)
            row = self.ledger_by_path[legacy_path]
            declarations = declared_tombstone_replacements(
                git_text(legacy_path), legacy_path
            )
            checked.add(legacy_path)
            with self.subTest(path=legacy_path):
                self.assertEqual("archive", row["action"])
                self.assertTrue(declarations)
                self.assertEqual(len(declarations), len(set(declarations)))
                self.assertEqual(declarations, index_replacements.get(legacy_path))
                translated: list[str] = []
                for declaration in declarations:
                    self.assertIn(declaration, self.ledger_by_path)
                    target = self.ledger_by_path[declaration]["stable_path"]
                    self.assertIsInstance(target, str)
                    canonical_target = canonical_current_path(str(target))
                    self.assertFalse(canonical_target.startswith("docs/98.archive/"))
                    self.assertIsNotNone(
                        stable_target_type(canonical_target), canonical_target
                    )
                    translated.append(canonical_target)

                self.assertEqual([], replacement_preservation_errors(row, translated))
                if legacy_path in KNOWN_TOMBSTONE_REPLACEMENTS:
                    self.assertEqual(
                        KNOWN_TOMBSTONE_REPLACEMENTS[legacy_path],
                        tuple(translated),
                    )

        known_paths = set(KNOWN_TOMBSTONE_REPLACEMENTS)
        self.assertEqual(known_paths, checked)

    def test_null_link_form_replacement_mutation_is_rejected(self) -> None:
        legacy_path = (
            "docs/98.archive/05.operations/guides/07-workflow/01.airflow-dag-dev.md"
        )
        declarations = declared_tombstone_replacements(
            git_text(legacy_path), legacy_path
        )
        translated = [
            str(self.ledger_by_path[declaration]["stable_path"])
            for declaration in declarations
        ]
        mutated = dict(self.ledger_by_path[legacy_path])
        mutated["replacement"] = None
        self.assertIn(
            "replacement-null",
            replacement_preservation_errors(mutated, translated),
        )

    def test_active_stage04_sources_follow_owning_spec_and_never_archive(self) -> None:
        for path, row in self.ledger_by_path.items():
            if not path.startswith("docs/04.execution/") or path.endswith("README.md"):
                continue
            metadata = frontmatter(git_text(path))
            if metadata.get("status") not in {"active", "draft"}:
                continue
            target = row["stable_path"] or ""
            self.assertFalse(target.startswith("docs/98.archive/"), path)
            parents = metadata.get("parent_ids") or []
            spec_parent = next(
                (str(value) for value in parents if str(value).startswith("spec:")),
                None,
            )
            if spec_parent is None:
                self.assertIn(row["action"], {"merge", "rewrite"})
                continue
            match = re.match(r"spec:(?:0*)([0-9]+)-(.+)", spec_parent)
            self.assertIsNotNone(match, spec_parent)
            identity, slug = match.groups()
            role = "plan" if "/plans/" in path else "task"
            expected = f"docs/03.specs/spec-{int(identity):04d}-{slug}/{role}.md"
            self.assertEqual(expected, target)
            expected_id = (
                f"plan-{int(identity):04d}"
                if role == "plan"
                else f"task-{int(identity):04d}-01"
            )
            self.assertEqual(expected_id, row["artifact_id"])

    def test_completed_linked_plan_task_pairs_share_typed_change_packet(self) -> None:
        plans_by_id: dict[str, str] = {}
        plans_by_slug: dict[str, str] = {}
        for path in self.ledger_by_path:
            if not path.startswith("docs/04.execution/plans/") or path.endswith(
                "README.md"
            ):
                continue
            metadata = frontmatter(git_text(path))
            if isinstance(metadata.get("artifact_id"), str):
                plans_by_id[str(metadata["artifact_id"])] = path
            slug = PurePosixPath(path).stem.removesuffix("-plan")
            plans_by_slug[slug] = path

        pairs: set[tuple[str, str]] = set()
        for task_path in self.ledger_by_path:
            if not task_path.startswith(
                "docs/04.execution/tasks/"
            ) or task_path.endswith("README.md"):
                continue
            body = git_text(task_path)
            metadata = frontmatter(body)
            if metadata.get("status") != "completed":
                continue
            paired = False
            for parent in metadata.get("parent_ids") or []:
                if str(parent) in plans_by_id:
                    pairs.add((plans_by_id[str(parent)], task_path))
                    paired = True
                    break
            task_slug = PurePosixPath(task_path).stem.removesuffix("-tasks")
            if not paired and task_slug in plans_by_slug:
                pairs.add((plans_by_slug[task_slug], task_path))

        self.assertGreater(len(pairs), 80)
        for plan_path, task_path in sorted(pairs):
            with self.subTest(plan=plan_path, task=task_path):
                plan = self.ledger_by_path[plan_path]
                task = self.ledger_by_path[task_path]
                self.assertEqual(
                    PurePosixPath(plan["stable_path"]).parent,
                    PurePosixPath(task["stable_path"]).parent,
                )
                plan_match = re.fullmatch(r"plan-([0-9]{4})", str(plan["artifact_id"]))
                task_match = re.fullmatch(
                    r"task-([0-9]{4})-[0-9]{2}", str(task["artifact_id"])
                )
                self.assertIsNotNone(plan_match)
                self.assertIsNotNone(task_match)
                self.assertEqual(plan_match.group(1), task_match.group(1))

    def test_duplicate_targets_have_exactly_one_non_merge_owner(self) -> None:
        grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in self.ledger_rows:
            if row["stable_path"] is not None:
                grouped[str(row["stable_path"])].append(row)
        duplicates = {target: rows for target, rows in grouped.items() if len(rows) > 1}
        self.assertTrue(duplicates)
        for target, rows in duplicates.items():
            with self.subTest(target=target):
                owners = [row for row in rows if row["action"] != "merge"]
                self.assertEqual(1, len(owners))
                self.assertTrue(
                    all(
                        row["action"] == "merge" for row in rows if row is not owners[0]
                    )
                )

    def test_current_archived_capabilities_are_restored_to_stage03(self) -> None:
        for identity, slug in (
            (123, "agentic-engineering-audit-remediation"),
            (131, "document-corpus-lifecycle-migration-foundation"),
            (132, "agent-governance-harness-convergence"),
            (133, "target-surface-contract-convergence"),
        ):
            path = f"docs/98.archive/03.specs/{identity}-{slug}/spec.md"
            row = self.ledger_by_path[path]
            self.assertEqual("move", row["action"])
            self.assertEqual(f"spec-{identity:04d}", row["artifact_id"])
            self.assertEqual(
                f"docs/03.specs/spec-{identity:04d}-{slug}/spec.md",
                row["stable_path"],
            )
            self.assertIsNone(row["replacement"])
            self.assertIn("current", row["reason"])

    def test_operations_root_is_single_and_possible(self) -> None:
        root = self.ledger_by_path["docs/05.operations/README.md"]
        self.assertEqual("docs/05.operations/README.md", root["stable_path"])
        self.assertEqual("rewrite", root["action"])
        impossible = [
            row["stable_path"]
            for row in self.ledger_rows
            if isinstance(row["stable_path"], str)
            and (
                "docs/04.execution" in row["stable_path"]
                or row["stable_path"].startswith("docs/05.operations/operations/")
            )
        ]
        self.assertEqual([], impossible)


class ScriptManifestValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.checker = load_manifest_checker()
        self.tracked = {
            ".github/workflow-contract.yml",
            "docs/authority.md",
            "docs/consumer.md",
            "docs/output.md",
            "scripts/example.py",
            "tests/validation/test_example.py",
        }

    def row(self, **updates: object) -> dict[str, object]:
        row: dict[str, object] = {
            "path": "scripts/example.py",
            "kind": "validator",
            "public_suites": ["repository-integrity"],
            "execution_contexts": [
                "local",
                "pull_request",
                "push",
                "workflow_dispatch",
            ],
            "authority": "docs/authority.md",
            "lifecycle": "active",
            "mutation": "none",
            "consumers": ["docs/consumer.md"],
            "disposition": "retain",
            "successor": None,
            "tests": ["tests/validation/test_example.py"],
        }
        return {**row, **updates}

    def codes(
        self, row: dict[str, object], tracked: set[str] | None = None
    ) -> set[str]:
        document = {"schema_version": 1, "files": [row]}
        return {
            finding.code
            for finding in self.checker.validate_manifest_document(
                document, self.tracked if tracked is None else tracked
            )
        }

    def test_manifest_rejects_unreferenced_executable(self) -> None:
        findings = self.checker.validate_manifest_document(
            {
                "schema_version": 1,
                "files": [
                    {
                        "path": "scripts/example.sh",
                        "kind": "validator",
                        "authority": "docs/authority.md",
                        "lifecycle": "active",
                        "mutation": "none",
                        "consumers": [],
                        "disposition": "retain",
                        "successor": None,
                        "tests": ["tests/validation/test_example.py"],
                    }
                ],
            },
            {
                "scripts/example.sh",
                "docs/authority.md",
                "tests/validation/test_example.py",
            },
        )
        self.assertIn("consumer-missing", {finding.code for finding in findings})

    def test_manifest_rejects_missing_and_invalid_authority(self) -> None:
        self.assertIn(
            "fields-missing",
            self.codes(
                {key: value for key, value in self.row().items() if key != "authority"}
            ),
        )
        self.assertIn("authority-invalid", self.codes(self.row(authority="")))
        self.assertIn(
            "authority-untracked", self.codes(self.row(authority="docs/unknown.md"))
        )

    def test_manifest_rejects_retired_operations_authority_fields(self) -> None:
        for field in ("current_authorities", "semantic_witnesses"):
            with self.subTest(field=field):
                self.assertIn(
                    "fields-unknown",
                    self.codes(self.row(**{field: ["docs/authority.md"]})),
                )

    def test_manifest_rejects_invalid_disposition_and_successor_contract(self) -> None:
        self.assertIn(
            "disposition-invalid", self.codes(self.row(disposition="deprecated"))
        )
        self.assertIn(
            "successor-invalid", self.codes(self.row(successor="scripts/next.py"))
        )
        self.assertIn(
            "successor-missing",
            self.codes(self.row(disposition="merge", successor=None)),
        )
        self.assertIn(
            "successor-untracked",
            self.codes(self.row(disposition="merge", successor="scripts/next.py")),
        )

    def test_manifest_rejects_missing_behavioral_tests_and_invalid_mutation(
        self,
    ) -> None:
        self.assertIn("tests-missing", self.codes(self.row(tests=[])))
        self.assertIn(
            "mutation-invalid", self.codes(self.row(mutation="default-write"))
        )

    def test_manifest_rejects_retired_placeholder_test_roots(self) -> None:
        for root in ("docs", "qa", "setup"):
            test_path = f"tests/{root}/test_example.py"
            with self.subTest(root=root):
                self.assertIn(
                    "tests-location-invalid",
                    self.codes(
                        self.row(tests=[test_path]),
                        self.tracked | {test_path},
                    ),
                )

    def test_manifest_requires_retained_library_tests_and_document_governance_mirrors(
        self,
    ) -> None:
        library = self.row(
            path="scripts/lib/document_governance/example.py",
            kind="library",
            consumers=[],
            tests=[],
        )
        library.pop("public_suites")
        library.pop("execution_contexts")
        tracked = self.tracked | {"scripts/lib/document_governance/example.py"}
        self.assertIn("tests-missing", self.codes(library, tracked))

        library["tests"] = ["tests/validation/test_example.py"]
        self.assertIn("tests-mirror-missing", self.codes(library, tracked))

    def test_manifest_rejects_invalid_generated_check_command(self) -> None:
        generator = self.row(
            kind="generator",
            mutation="check-write",
            authority=".github/workflow-contract.yml",
        )
        self.assertIn("generated-check-invalid", self.codes(generator))
        adversarial = (
            ["python3", "scripts/example.py", "--write"],
            ["bash", "scripts/example.py", "--check"],
            ["sh", "-c", "python3 scripts/example.py --check"],
            ["python3", "-c", "pass", "scripts/example.py", "--check"],
            ["python3", "-m", "scripts.example", "--check"],
            ["python3", "scripts/example.py", "--check", "extra"],
            [
                "python3",
                "scripts/validation/check-script-manifest.py",
                "scripts/example.py",
                "--check",
            ],
        )
        for command in adversarial:
            with self.subTest(command=command):
                self.assertIn(
                    "generated-check-invalid",
                    self.codes(
                        self.row(
                            kind="generator",
                            mutation="check-write",
                            authority=".github/workflow-contract.yml",
                            check_command=command,
                            outputs=["docs/output.md"],
                        )
                    ),
                )
        self.assertNotIn(
            "generated-check-invalid",
            self.codes(
                self.row(
                    kind="generator",
                    mutation="check-write",
                    authority=".github/workflow-contract.yml",
                    check_command=["python3", "scripts/example.py", "--check"],
                    outputs=["docs/output.md"],
                )
            ),
        )
        self.assertIn(
            "generated-output-untracked",
            self.codes(
                self.row(
                    kind="generator",
                    mutation="check-write",
                    authority=".github/workflow-contract.yml",
                    check_command=["python3", "scripts/example.py", "--check"],
                    outputs=["docs/unknown-output.md"],
                )
            ),
        )

    def test_manifest_rejects_unknown_fields_and_untracked_paths(self) -> None:
        self.assertIn("fields-unknown", self.codes(self.row(legacy=True)))
        self.assertIn(
            "path-untracked",
            self.codes(self.row(path="scripts/unknown.py")),
        )
        self.assertIn(
            "consumers-untracked",
            self.codes(self.row(consumers=["docs/unknown.md"])),
        )
        self.assertIn(
            "tests-untracked",
            self.codes(self.row(tests=["tests/unknown.py"])),
        )

    def test_manifest_rejects_tests_outside_approved_roots(self) -> None:
        tracked = {*self.tracked, "docs/test_example.py"}
        self.assertIn(
            "tests-location-invalid",
            self.codes(self.row(tests=["docs/test_example.py"]), tracked),
        )

    def test_retained_runtime_rejects_unrelated_spec_authority(self) -> None:
        self.assertIn(
            "runtime-authority-invalid",
            self.codes(
                self.row(
                    kind="operations",
                    mutation="runtime",
                    authority="docs/authority.md",
                )
            ),
        )

    def _generator_repo(
        self, root: Path, script: str, script_path: str = "scripts/example.py"
    ) -> Path:
        for relative in ("scripts", "docs", "tests"):
            (root / relative).mkdir(parents=True, exist_ok=True)
        (root / script_path).parent.mkdir(parents=True, exist_ok=True)
        (root / script_path).write_text(script, encoding="utf-8")
        (root / ".github").mkdir(parents=True, exist_ok=True)
        (root / ".github/workflow-contract.yml").write_text(
            f'entrypoint: "{script_path}"\n', encoding="utf-8"
        )
        (root / "docs/authority.md").write_text("authority\n", encoding="utf-8")
        (root / "docs/consumer.md").write_text(
            f"`{script_path}`\n`scripts/manifest.yaml`\n", encoding="utf-8"
        )
        (root / "docs/output.md").write_text("before\n", encoding="utf-8")
        (root / "tests/validation").mkdir(parents=True, exist_ok=True)
        (root / "tests/validation/test_example.py").write_text(
            f"import subprocess\nsubprocess.run(['python3', '{script_path}', '--check'], check=False)\n",
            encoding="utf-8",
        )
        generator = self.row(
            path=script_path,
            kind="generator",
            mutation="check-write",
            authority=".github/workflow-contract.yml",
            check_command=["python3", script_path, "--check"],
            outputs=["docs/output.md"],
        )
        generator.pop("public_suites")
        generator.pop("execution_contexts")
        manifest = {
            "schema_version": 1,
            "files": [
                generator,
                {
                    "path": "scripts/manifest.yaml",
                    "kind": "contract",
                    "authority": "docs/authority.md",
                    "lifecycle": "active",
                    "mutation": "none",
                    "consumers": ["docs/consumer.md"],
                    "disposition": "retain",
                    "successor": None,
                    "tests": [],
                },
            ],
        }
        manifest["files"].sort(key=lambda row: row["path"])
        manifest_path = root / "scripts/manifest.yaml"
        manifest_path.write_text(
            yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
        )
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Task Test",
                "-c",
                "user.email=task@example.invalid",
                "commit",
                "-qm",
                "fixture",
            ],
            cwd=root,
            check=True,
        )
        return manifest_path

    def test_generated_checks_fail_closed_on_stale_missing_and_mutating_commands(
        self,
    ) -> None:
        valid_script = "import argparse\nargparse.ArgumentParser().add_argument('--check', action='store_true')\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script_path = "scripts/validation/check-supply-chain-policy.py"
            manifest_path = self._generator_repo(root, valid_script, script_path)
            self.assertEqual([], self.checker.check_generated(root, manifest_path))

            (root / script_path).write_text("raise SystemExit(9)\n", encoding="utf-8")
            self.assertIn(
                "generated-check-failed",
                {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                },
            )
            producer = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            next(row for row in producer["files"] if row["path"] == script_path).update(
                kind="validator",
                public_suites=["repository-integrity"],
                execution_argv=["--check"],
                execution_contexts=[
                    "local",
                    "pull_request",
                    "push",
                    "workflow_dispatch",
                ],
            )
            manifest_path.write_text(
                yaml.safe_dump(producer, sort_keys=False), encoding="utf-8"
            )
            self.assertIn(
                "generated-check-failed",
                {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                },
            )

            (root / script_path).write_text(
                "from pathlib import Path\nPath('docs/output.md').write_text('mutated\\n')\n",
                encoding="utf-8",
            )
            self.assertIn(
                "generated-check-mutated",
                {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                },
            )

            for surface in ("docs", "tests", "infra"):
                with self.subTest(ignored_surface=surface):
                    subprocess.run(
                        ["git", "restore", "docs/output.md"], cwd=root, check=True
                    )
                    marker = f"{surface}/.ignored-mutation"
                    (root / surface).mkdir(parents=True, exist_ok=True)
                    (root / script_path).write_text(
                        f"from pathlib import Path\nPath('{marker}').write_text('mutated\\n')\n",
                        encoding="utf-8",
                    )
                    (root / ".gitignore").write_text(f"{marker}\n", encoding="utf-8")
                    self.assertIn(
                        "generated-check-mutated",
                        {
                            finding.code
                            for finding in self.checker.check_generated(
                                root, manifest_path
                            )
                        },
                    )
                    (root / marker).unlink()

            subprocess.run(["git", "restore", "docs/output.md"], cwd=root, check=True)
            document = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            missing = deepcopy(document)
            next(row for row in missing["files"] if row["path"] == script_path)[
                "check_command"
            ] = [
                "missing-task9-generator-command",
                script_path,
                "--check",
            ]
            manifest_path.write_text(
                yaml.safe_dump(missing, sort_keys=False), encoding="utf-8"
            )
            self.assertIn(
                "generated-check-invalid",
                {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                },
            )

    def test_semantic_evidence_rejects_prose_comments_and_non_test_paths(self) -> None:
        valid_script = "import argparse\nargparse.ArgumentParser().add_argument('--check', action='store_true')\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest_path = self._generator_repo(root, valid_script)
            (root / "docs/consumer.md").write_text(
                "This prose merely mentions scripts/example.py.\n", encoding="utf-8"
            )
            (root / "tests/validation/test_example.py").write_text(
                "# subprocess.run(['python3', 'scripts/example.py', '--check'])\n",
                encoding="utf-8",
            )
            codes = {
                finding.code
                for finding in self.checker.check_manifest(root, manifest_path)
            }
            self.assertIn("consumers-unproven", codes)
            self.assertIn("tests-unproven", codes)
            (root / "tests/validation/test_example.py").write_text(
                '"""Prose only: scripts/example.py."""\n', encoding="utf-8"
            )
            codes = {
                finding.code
                for finding in self.checker.check_manifest(root, manifest_path)
            }
            self.assertIn("tests-unproven", codes)
            (root / "tests/validation/test_example.py").write_text(
                "TARGET = 'scripts/example.py'\nprint('unrelated')\n",
                encoding="utf-8",
            )
            codes = {
                finding.code
                for finding in self.checker.check_manifest(root, manifest_path)
            }
            self.assertIn("tests-unproven", codes)

    def test_yaml_semantic_evidence_accepts_exact_entry_only(self) -> None:
        target = "scripts/example.py"
        exact = "entry: python3 scripts/example.py --check\n"
        comment = "# entry: python3 scripts/example.py --check\n"
        collision = "entry: python3 scripts/example.py-extra --check\n"

        self.assertTrue(
            self.checker._reference_proves_use(
                ".pre-commit-config.yaml", exact, target, is_test=False
            )
        )
        self.assertFalse(
            self.checker._reference_proves_use(
                ".pre-commit-config.yaml", comment, target, is_test=False
            )
        )
        self.assertFalse(
            self.checker._reference_proves_use(
                ".pre-commit-config.yaml", collision, target, is_test=False
            )
        )

    def test_yaml_semantic_evidence_cycle_is_an_explicit_finding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            consumer = root / ".pre-commit-config.yaml"
            consumer.write_text("entry: &loop\n  - *loop\n", encoding="utf-8")
            document = {
                "files": [
                    {
                        "path": "scripts/example.py",
                        "consumers": [".pre-commit-config.yaml"],
                        "tests": [],
                    }
                ]
            }
            codes = {
                finding.code
                for finding in self.checker._semantic_findings(root, document)
            }
        self.assertIn("consumers-invalid", codes)

    def test_python_semantic_evidence_accepts_target_linked_uses(self) -> None:
        positives = (
            "import scripts.example\n",
            "import subprocess\nsubprocess.run(['python3', 'scripts/example.py', '--check'])\n",
            "from scripts import example\nexample.validate_manifest_document({}, set())\n",
            "import importlib.util\nfrom pathlib import Path\n"
            "TARGET = Path('scripts/example.py')\n"
            "importlib.util.spec_from_file_location('scripts.example', TARGET)\n",
        )
        for source in positives:
            with self.subTest(source=source):
                self.assertTrue(
                    self.checker._python_proves_use(source, "scripts/example.py")
                )

    def test_python_semantic_evidence_rejects_unrelated_calls_and_collisions(
        self,
    ) -> None:
        negatives = (
            "from unrelated import example\n",
            "TARGET = 'scripts/example.py'\nlen(TARGET)\n",
            "len('scripts/example.py')\n",
            "import logging\nTARGET = 'scripts/example.py'\nlogging.info(TARGET)\n",
            "import logging\nlogging.info('scripts/example.py')\n",
            "from pathlib import Path\nTARGET = Path('scripts/example.py')\nTARGET.unrelated()\n",
            "import subprocess\nsubprocess.run(['python3', 'other/scripts/example.py'])\n",
            "import scripts.example_extra\n",
        )
        for source in negatives:
            with self.subTest(source=source):
                self.assertFalse(
                    self.checker._python_proves_use(source, "scripts/example.py")
                )

    def test_python_semantic_evidence_rejects_ambiguous_path_reassignment(self) -> None:
        source = (
            "import subprocess\n"
            "TARGET = 'scripts/example.py'\n"
            "TARGET = 'scripts/other.py'\n"
            "subprocess.run(['python3', TARGET])\n"
        )
        self.assertFalse(self.checker._python_proves_use(source, "scripts/example.py"))

    def test_python_semantic_evidence_rejects_sibling_function_scope_join(self) -> None:
        source = (
            "from pathlib import Path\n"
            "def one():\n"
            "    BASE = Path('scripts')\n"
            "def two():\n"
            "    from example import helper\n"
        )
        self.assertFalse(self.checker._python_proves_use(source, "scripts/example.py"))

    def test_python_semantic_evidence_rejects_sibling_class_scope_join(self) -> None:
        source = (
            "from pathlib import Path\n"
            "class One:\n"
            "    BASE = Path('scripts')\n"
            "class Two:\n"
            "    from example import helper\n"
        )
        self.assertFalse(self.checker._python_proves_use(source, "scripts/example.py"))

    def test_python_semantic_evidence_allows_explicit_module_path_visibility(
        self,
    ) -> None:
        source = (
            "from pathlib import Path\n"
            "BASE = Path('scripts')\n"
            "def use():\n"
            "    from example import helper\n"
        )
        self.assertTrue(self.checker._python_proves_use(source, "scripts/example.py"))

    def test_declared_paths_reject_symlinks_before_execution(self) -> None:
        valid_script = "raise SystemExit('must not execute')\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest_path = self._generator_repo(root, valid_script)
            outside = root.parent / f"{root.name}-outside.py"
            outside.write_text(valid_script, encoding="utf-8")
            (root / "scripts/example.py").unlink()
            (root / "scripts/example.py").symlink_to(outside)
            try:
                codes = {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                }
                self.assertIn("declared-path-invalid", codes)
                self.assertNotIn("generated-check-failed", codes)
            finally:
                outside.unlink(missing_ok=True)

    def test_declared_output_symlink_outside_repo_is_never_followed(self) -> None:
        valid_script = "raise SystemExit('must not execute')\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest_path = self._generator_repo(root, valid_script)
            outside = root.parent / f"{root.name}-outside-output.md"
            outside.write_text("outside\n", encoding="utf-8")
            (root / "docs/output.md").unlink()
            (root / "docs/output.md").symlink_to(outside)
            try:
                codes = {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                }
                self.assertIn("declared-path-invalid", codes)
                self.assertEqual("outside\n", outside.read_text(encoding="utf-8"))
                self.assertNotIn("generated-check-failed", codes)
            finally:
                outside.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
