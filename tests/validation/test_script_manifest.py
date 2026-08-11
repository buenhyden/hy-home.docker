from __future__ import annotations

import ast
from collections import Counter, defaultdict
import posixpath
import re
import subprocess
import unittest
from pathlib import Path, PurePosixPath

import yaml


ROOT = Path(__file__).resolve().parents[2]
BASELINE = "232effd9a5e00907bdbe30efc6665023fb2d07f4"
MANIFEST = ROOT / "scripts/manifest.yaml"
LEDGER = ROOT / "docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md"
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
    "docs/90.references/llm-wiki/",
)
MUTATION_OVERRIDES = {
    "scripts/hooks/patch-graphify-post-commit.sh": "check-write",
    "scripts/hooks/post-tool-validate.sh": "check-write",
    "scripts/knowledge/generate-llm-wiki-coverage.sh": "check-write",
    "scripts/knowledge/generate-llm-wiki-index.sh": "check-write",
    "scripts/operations/gen-secrets.sh": "runtime",
    "scripts/operations/generate-compose-profile-service-coverage.sh": "check-write",
    "scripts/operations/generate-tech-stack-version-provenance.sh": "check-write",
    "scripts/operations/provider_surface_renderer.py": "check-write",
    "scripts/operations/rehearse-sample-service-delivery.sh": "runtime",
    "scripts/operations/sync-provider-surfaces.sh": "check-write",
    "scripts/operations/sync-tech-stack-versions.sh": "check-write",
    "scripts/security/generate-supply-chain-sample-service-summary.sh": "check-write",
    "scripts/security/seed-grype-db-cache.sh": "runtime",
    "scripts/security/verify-sample-service-supply-chain.sh": "runtime",
    "scripts/validation/check-document-corpus-lifecycle.py": "check-write",
    "scripts/validation/check-document-metadata.py": "check-write",
    "scripts/validation/check-target-surface-delta-contract.py": "check-write",
    "scripts/validation/generate-audit-implementation-matrix.sh": "check-write",
    "scripts/validation/generate-security-automation-readiness.sh": "check-write",
    "scripts/validation/rehearse-postgres-logical-upgrade.sh": "runtime",
    "scripts/validation/report-provider-hook-parity.sh": "check-write",
    "scripts/validation/run-agent-precommit-all-files.sh": "check-write",
    "scripts/validation/run-compose-core-readiness.sh": "runtime",
    "scripts/validation/compose-core-readiness.lib.sh": "runtime",
    "scripts/validation/validate-docker-compose.sh": "runtime",
}
MANDATORY_DISPOSITIONS = {
    "scripts/hooks/patch-graphify-post-commit.sh": "merge",
    "scripts/hooks/post-tool-validate.sh": "rewrite",
    "scripts/knowledge/generate-llm-wiki-coverage.sh": "merge",
    "scripts/knowledge/generate-llm-wiki-index.sh": "merge",
    "scripts/validation/check-doc-implementation-alignment.sh": "merge",
    "scripts/validation/check-doc-traceability.sh": "merge",
    "scripts/validation/check-repo-contracts.sh": "merge",
    "scripts/validation/recommend-gap-routing.sh": "delete",
    "scripts/validation/recommend-qa-gates.sh": "merge",
    "scripts/validation/report-provider-hook-parity.sh": "merge",
}
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
        "docs/03.specs/spec-0008-workflow/spec.md",
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
        "docs/03.specs/spec-0008-workflow/spec.md",
    ),
    "docs/98.archive/05.operations/runbooks/07-workflow/airbyte.md": (
        "docs/03.specs/spec-0008-workflow/spec.md",
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


def tracked_paths(pathspec: str) -> set[str]:
    return set(
        subprocess.run(
            ["git", "ls-files", pathspec],
            cwd=ROOT,
            text=True,
            check=True,
            capture_output=True,
        ).stdout.splitlines()
    )


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


def replacement_preservation_errors(
    row: dict[str, object], translated: list[str]
) -> list[str]:
    if not translated:
        return ["declared-replacement-empty"]
    errors: list[str] = []
    if row["replacement"] is None:
        errors.append("replacement-null")
    elif row["replacement"] != translated[0]:
        errors.append("primary-replacement-mismatch")
    evidence = f"{row['replacement']} {row['reason']}"
    if any(target not in evidence for target in translated):
        errors.append("translated-replacement-evidence-missing")
    return errors


def _python_imports_target(reference: str, target: str) -> bool:
    if not reference.endswith(".py") or not target.endswith(".py"):
        return False
    module = target.removesuffix(".py").replace("/", ".")
    try:
        tree = ast.parse((ROOT / reference).read_text(encoding="utf-8"))
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == module for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom) and node.module == module:
            return True
    return False


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
        return any(
            (target in line or basename in line)
            and re.search(r'(?:command|implementation|run|script|entrypoint|argv|path)"?\s*:', line)
            for line in text.splitlines()
        )
    if reference.endswith((".sh", ".bash")):
        return any(
            (target in line or basename in line)
            and not line.lstrip().startswith("#")
            for line in text.splitlines()
        )
    if reference.endswith(".py"):
        return any(
            marker in text
            for marker in ("subprocess.run", "subprocess.Popen", "runpy.run_path", "importlib")
        )
    return target in text


def stable_target_type(path: str) -> str | None:
    patterns = (
        (r"docs/01\.requirements/prd-[0-9]{3}-[^/]+\.md", "prd"),
        (r"docs/02\.architecture/descriptions/ad-[0-9]{4}-[^/]+\.md", "ad"),
        (r"docs/02\.architecture/decisions/adr-[0-9]{4}-[^/]+\.md", "adr"),
        (r"docs/03\.specs/spec-[0-9]{4}-[^/]+/spec\.md", "spec"),
        (r"docs/03\.specs/spec-[0-9]{4}-[^/]+/plan\.md", "plan"),
        (r"docs/03\.specs/spec-[0-9]{4}-[^/]+/task\.md", "task"),
        (r"docs/05\.operations/(?:[0-9]{2}-[^/]+)/(?:ops-[0-9]{4}-[^/]+)/(?:guide|policy|runbook)\.md", "ops-role"),
        (r"docs/05\.operations/incidents/inc-[0-9]{4}-[^/]+/(?:incident|postmortem)\.md", "event"),
        (r"docs/05\.operations/releases/rel-[0-9]{4}-[^/]+/release\.md", "release"),
        (r"docs/90\.references/.*/ref-[0-9]{4}-[^/]+(?:\.(?:md|yaml|yml|json)|/README\.md)", "reference"),
        (r"docs/98\.archive/changes/chg-[0-9]{4}-[^/]+/(?:plan|task)\.md", "change"),
        (r"docs/98\.archive/tombstones/(?:01\.requirements|02\.architecture|03\.specs|05\.operations)/[^/]+\.md", "tombstone"),
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
        ledger_text = LEDGER.read_text(encoding="utf-8").split("```yaml\n", 1)[1].split("```", 1)[0]
        cls.ledger_rows = yaml.safe_load(ledger_text)["records"]
        cls.ledger_by_path = {row["legacy_path"]: row for row in cls.ledger_rows}

    def test_every_tracked_script_has_one_manifest_record(self) -> None:
        declared = [row["path"] for row in self.rows]
        self.assertEqual(len(declared), len(set(declared)))
        self.assertEqual(self.tracked, set(declared))

    def test_records_are_sorted_and_use_the_complete_schema(self) -> None:
        paths = [row["path"] for row in self.rows]
        self.assertEqual(paths, sorted(paths))
        for row in self.rows:
            self.assertEqual(REQUIRED_FIELDS, set(row))
            self.assertIn(row["kind"], KINDS)
            self.assertIn(row["lifecycle"], LIFECYCLES)
            self.assertIn(row["mutation"], MUTATIONS)
            self.assertIn(row["disposition"], DISPOSITIONS)
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
                if row["disposition"] == "retain":
                    self.assertTrue(row["consumers"])
                if row["disposition"] == "retain" and row["kind"] not in {"contract", "dependency-manifest"}:
                    self.assertTrue(row["tests"])
                if row["mutation"] == "runtime" and row["disposition"] == "retain":
                    self.assertTrue(row["authority"].startswith("docs/05.operations/runbooks/"))
                    self.assertTrue(row["tests"])
                if row["kind"] == "generator" and row["mutation"] == "check-write":
                    self.assertIn(row["disposition"], {"merge", "rewrite"})

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
            ["scripts/validation/check-document-metadata.py"],
            row["consumers"],
        )
        self.assertEqual(
            [
                "tests/validation/test_document_metadata.py",
                "tests/validation/test_document_taxonomy.py",
            ],
            row["tests"],
        )

    def test_mutation_classes_follow_observed_script_behavior(self) -> None:
        for row in self.rows:
            with self.subTest(path=row["path"]):
                expected = MUTATION_OVERRIDES.get(row["path"], "none")
                self.assertEqual(expected, row["mutation"])
                if row["kind"] == "generator" and row["mutation"] == "check-write":
                    self.assertNotEqual("retain", row["disposition"])

    def test_plan_mandatory_dispositions_and_high_risk_operations(self) -> None:
        for path, disposition in MANDATORY_DISPOSITIONS.items():
            with self.subTest(path=path):
                self.assertEqual(disposition, self.rows_by_path[path]["disposition"])

        postgres = self.rows_by_path[
            "scripts/validation/rehearse-postgres-logical-upgrade.sh"
        ]
        self.assertEqual("retain", postgres["disposition"])
        self.assertEqual(
            "docs/05.operations/runbooks/04-data/relational/postgresql-logical-upgrade-restore-rehearsal.md",
            postgres["authority"],
        )
        self.assertEqual(
            [postgres["authority"]],
            postgres["consumers"],
        )
        self.assertEqual(
            ["tests/validation/test_postgres_logical_upgrade_rehearsal.py"],
            postgres["tests"],
        )
        for path in (
            "scripts/operations/gen-secrets.sh",
            "scripts/security/seed-grype-db-cache.sh",
        ):
            with self.subTest(path=path):
                row = self.rows_by_path[path]
                if row["disposition"] == "retain":
                    self.assertTrue(row["consumers"])
                    self.assertTrue(row["tests"])
                    self.assertTrue(row["authority"].startswith("docs/05.operations/runbooks/"))

    def test_authority_is_specific_and_runtime_retention_is_runbook_bound(self) -> None:
        unrelated = {
            "docs/05.operations/runbooks/03-security/vault.md",
            "docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md",
        }
        migration_authority = "docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md"
        for row in self.rows:
            with self.subTest(path=row["path"]):
                authority = row["authority"]
                authority_text = (ROOT / authority).read_text(encoding="utf-8")
                basename = PurePosixPath(row["path"]).name
                if authority in unrelated and basename not in authority_text and row["path"] not in authority_text:
                    self.fail(f"blanket authority {authority} does not govern {row['path']}")
                if row["mutation"] == "runtime" and row["disposition"] == "retain":
                    self.assertTrue(authority.startswith("docs/05.operations/runbooks/"))
                    self.assertTrue(
                        basename in authority_text or row["path"] in authority_text,
                        f"runtime Runbook does not name {row['path']}",
                    )
                elif row["mutation"] == "runtime" and not authority.startswith(
                    "docs/05.operations/runbooks/"
                ):
                    self.assertNotEqual("retain", row["disposition"])
                    self.assertEqual(migration_authority, authority)

    def test_scripts_readme_preserves_invocation_warnings(self) -> None:
        text = (ROOT / "scripts/README.md").read_text(encoding="utf-8")
        compact = re.sub(r"\s+", " ", text)
        self.assertIn("Do not invoke a `mutation: runtime` row", compact)
        self.assertIn("Do not invoke a default-write generator without", compact)
        self.assertIn("semantic invocation/import evidence", compact)

    def test_ledger_has_one_complete_sorted_row_for_every_migration_document(self) -> None:
        rows = self.ledger_rows
        expected = set(
            subprocess.run(
                [
                    "git", "ls-tree", "-r", "--name-only",
                    BASELINE,
                    "--", *MIGRATION_ROOTS,
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
                self.assertIn(row["action"], {"archive", "delete", "merge", "move", "retain", "rewrite"})
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
                    self.assertFalse(any(re.fullmatch(r"[0-9]{4}", part) for part in parts))
                    self.assertFalse(any(re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-", part) for part in parts))
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
            "prd": (r".*/prd-([0-9]{3})-[^/]+\.md", "prd"),
            "ad": (r".*/ad-([0-9]{4})-[^/]+\.md", "ad"),
            "adr": (r".*/adr-([0-9]{4})-[^/]+\.md", "adr"),
            "spec": (r".*/spec-([0-9]{4})-[^/]+/spec\.md", "spec"),
            "event": (r".*/inc-([0-9]{4})-[^/]+/incident\.md", "inc"),
            "release": (r".*/rel-([0-9]{4})-[^/]+/release\.md", "rel"),
            "reference": (r".*/ref-([0-9]{4})-[^/]+(?:\.(?:md|yaml|yml|json)|/README\.md)", "ref"),
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
                    expected = f"plan-{identity}" if role == "plan" else f"task-{identity}-01"
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
                    self.assertTrue(filename.startswith(f"{artifact_id}-") or filename == artifact_id)

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
                self.assertIn(metadata.get("status"), {"completed", "superseded", "archived"})
                self.assertTrue(str(row["stable_path"]).startswith("docs/98.archive/tombstones/"))
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

    def test_baseline_tombstone_replacements_are_preserved_as_stable_targets(self) -> None:
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
                    self.assertFalse(str(target).startswith("docs/98.archive/"))
                    self.assertIsNotNone(stable_target_type(str(target)), target)
                    translated.append(str(target))

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
            expected_id = f"plan-{int(identity):04d}" if role == "plan" else f"task-{int(identity):04d}-01"
            self.assertEqual(expected_id, row["artifact_id"])

    def test_completed_linked_plan_task_pairs_share_typed_change_packet(self) -> None:
        plans_by_id: dict[str, str] = {}
        plans_by_slug: dict[str, str] = {}
        for path in self.ledger_by_path:
            if not path.startswith("docs/04.execution/plans/") or path.endswith("README.md"):
                continue
            metadata = frontmatter(git_text(path))
            if isinstance(metadata.get("artifact_id"), str):
                plans_by_id[str(metadata["artifact_id"])] = path
            slug = PurePosixPath(path).stem.removesuffix("-plan")
            plans_by_slug[slug] = path

        pairs: set[tuple[str, str]] = set()
        for task_path in self.ledger_by_path:
            if not task_path.startswith("docs/04.execution/tasks/") or task_path.endswith("README.md"):
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
                self.assertEqual(PurePosixPath(plan["stable_path"]).parent, PurePosixPath(task["stable_path"]).parent)
                plan_match = re.fullmatch(r"plan-([0-9]{4})", str(plan["artifact_id"]))
                task_match = re.fullmatch(r"task-([0-9]{4})-[0-9]{2}", str(task["artifact_id"]))
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
                self.assertTrue(all(row["action"] == "merge" for row in rows if row is not owners[0]))

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


if __name__ == "__main__":
    unittest.main()
