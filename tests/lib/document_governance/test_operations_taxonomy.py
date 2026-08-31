from __future__ import annotations

import pathlib
import shutil
import stat
import subprocess
import tempfile
import unittest
from unittest import mock

import yaml

from scripts.lib.document_governance.operations_catalog import (
    MIGRATION_PATH,
    SEMANTIC_WITNESS_PATH,
    TASK8_ROW_IDS,
    GitCommandResult,
    OperationsAuthorityError,
    _markdown_body_text,
    _validate_semantic_witnesses,
    extract_task8_consumers,
    load_task8_migration,
    validate_active_operations_references,
)
from scripts.lib.gate.ci_gate_contract import (
    load_contract_document,
    load_public_suite_registry,
    parse_public_gate_contract,
    select_public_suites,
)


ROOT = pathlib.Path(__file__).resolve().parents[3]


def _public_suites_for(*changed_paths: str) -> tuple[str, ...]:
    registry = load_public_suite_registry(ROOT / "scripts/manifest.yaml")
    contract = parse_public_gate_contract(load_contract_document(ROOT), registry)
    return select_public_suites(contract, "changed", changed_paths)


class OperationsAuthorityTests(unittest.TestCase):
    def test_operations_checker_is_executable_and_publishes_required_mode_usage(self) -> None:
        checker = ROOT / "scripts/validation/check-operations-catalog.py"
        self.assertTrue(checker.stat().st_mode & stat.S_IXUSR)
        result = subprocess.run(
            [str(checker), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("--mode", result.stdout)
        self.assertIn("complete", result.stdout)

    def test_active_corpus_has_no_generic_predecessor_or_release_role_routes(self) -> None:
        self.assertEqual((), validate_active_operations_references(ROOT))

    def test_active_reference_scan_has_explicit_history_and_negative_exclusions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            fixtures = {
                "docs/00.agent-governance/active.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-subject/guide.md.\n"
                ),
                "docs/90.references/history.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-historical/guide.md.\n"
                ),
                "docs/03.specs/0136-sdlc-taxonomy-convergence/spec.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-evidence/guide.md.\n"
                ),
                "docs/03.specs/0153-workspace-governance-simplification/plan.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-migration/guide.md.\n"
                ),
                "docs/03.specs/0999-new-active-spec/spec.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-active-spec/guide.md.\n"
                ),
                "tests/fixtures/negative.md": (
                    "See docs/05.operations/catalog/00-workspace/ops-####-negative/guide.md.\n"
                ),
                "docs/00.agent-governance/negative.md": "No separate Release document role.\n",
            }
            for relative, content in fixtures.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            subprocess.run(["git", "add", *fixtures], cwd=root, check=True)
            findings = validate_active_operations_references(root)
            self.assertEqual(2, len(findings))
            self.assertEqual(
                {
                    "docs/00.agent-governance/active.md",
                    "docs/03.specs/0999-new-active-spec/spec.md",
                },
                {finding.path.split(":", 1)[0] for finding in findings},
            )

    def test_active_reference_scan_covers_scripts_and_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            fixtures = {
                "scripts/validation/active.sh": (
                    'guide="docs/05.operations/guides/00-workspace/example.md"\n'
                ),
                ".github/operations.yaml": (
                    "policy: docs/05.operations/policies/00-workspace/example.md\n"
                ),
                "tests/fixtures/negative.sh": (
                    'runbook="docs/05.operations/runbooks/00-workspace/example.md"\n'
                ),
                "docs/98.archive/migrations/history.toml": (
                    'route = "docs/05.operations/guides/00-workspace/example.md"\n'
                ),
                "docs/99.templates/support/document-corpus-migration-contract.yaml": (
                    "source: docs/05.operations/policies/00-workspace/example.md\n"
                ),
            }
            for relative, content in fixtures.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            subprocess.run(["git", "add", *fixtures], cwd=root, check=True)
            findings = validate_active_operations_references(root)
            self.assertEqual(
                {
                    ".github/operations.yaml",
                    "scripts/validation/active.sh",
                },
                {finding.path.split(":", 1)[0] for finding in findings},
            )

    def test_current_drift_guides_exist_at_canonical_catalog_paths(self) -> None:
        expected = (
            "docs/05.operations/catalog/00-workspace/"
            "0003-env-key-comparison/guide.md",
            "docs/05.operations/catalog/00-workspace/"
            "0010-sensitive-env-vars-comparison/guide.md",
        )
        for relative in expected:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_public_operations_suite_owns_focused_validators_exactly_once(self) -> None:
        registry = load_public_suite_registry(ROOT / "scripts/manifest.yaml")
        operations = next(
            suite for suite in registry.suites if suite.name == "operations"
        )
        self.assertEqual(
            (
                pathlib.PurePosixPath(
                    "scripts/lib/ops/rehearse-postgres-logical-upgrade.sh"
                ),
                pathlib.PurePosixPath(
                    "scripts/validation/check-operations-catalog.py"
                ),
            ),
            operations.validators,
        )
        manifest = yaml.safe_load(
            (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
        )
        rehearsal = next(
            row
            for row in manifest["files"]
            if row["path"]
            == "scripts/lib/ops/rehearse-postgres-logical-upgrade.sh"
        )
        self.assertEqual("validator", rehearsal["kind"])
        self.assertEqual("runtime", rehearsal["mutation"])
        self.assertEqual(["operations"], rehearsal["public_suites"])
        self.assertEqual([], rehearsal["execution_contexts"])

    def test_public_changed_profile_routes_operations_paths_fail_closed(self) -> None:
        expected = (
            "document-contract",
            "document-graph",
            "document-lifecycle",
            "operations",
            "repository-integrity",
        )
        self.assertEqual(
            expected,
            _public_suites_for(
                "docs/05.operations/catalog/01-gateway/0013-traefik/guide.md"
            ),
        )
        self.assertEqual(
            expected,
            _public_suites_for("infra/01-gateway/traefik/docker-compose.yml"),
        )

    def test_selected_spec_role_links_use_exact_current_role_leaves(self) -> None:
        expected = {
            "docs/03.specs/0001-gateway/spec.md": {
                "Guide": "../../05.operations/catalog/01-gateway/0012-edge-routing-stack/guide.md",
                "Policy": "../../05.operations/catalog/01-gateway/0013-traefik/policy.md",
                "Runbook": "../../05.operations/catalog/01-gateway/0013-traefik/runbook.md",
            },
            "docs/03.specs/0002-auth/spec.md": {
                role: f"../../05.operations/catalog/02-auth/0014-keycloak/{role.lower()}.md"
                for role in ("Guide", "Policy", "Runbook")
            },
            "docs/03.specs/0005-data-analytics/spec.md": {
                role: f"../../05.operations/catalog/04-data/0017-influxdb/{role.lower()}.md"
                for role in ("Guide", "Policy", "Runbook")
            },
            "docs/03.specs/0095-infra-secrets-docs-refresh/spec.md": {
                role: f"../../05.operations/catalog/03-security/0016-vault/{role.lower()}.md"
                for role in ("Guide", "Policy", "Runbook")
            },
        }
        for relative, roles in expected.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            for role, href in roles.items():
                with self.subTest(path=relative, role=role):
                    self.assertIn(f"- **{role}**: [{href}]({href})", text)

    def test_public_script_changes_select_every_registered_suite(self) -> None:
        registry = load_public_suite_registry(ROOT / "scripts/manifest.yaml")
        self.assertEqual(
            registry.public_names,
            _public_suites_for("scripts/lib/gate/ci_gate_contract.py"),
        )

    def test_migration0003_slice_is_exact_and_preconditions_are_resolved(self) -> None:
        migration = load_task8_migration(ROOT)
        self.assertEqual(TASK8_ROW_IDS, tuple(row.row_id for row in migration.rows))
        self.assertEqual(192, sum(row.action == "rename" for row in migration.rows))
        self.assertEqual(1, sum(row.action == "delete" for row in migration.rows))
        for row in migration.rows:
            source_exists = (ROOT / row.source_path).is_file()
            target_exists = row.target_path is not None and (ROOT / row.target_path).is_file()
            with self.subTest(row=row.row_id):
                if row.action == "rename":
                    self.assertNotEqual(source_exists, target_exists)
                else:
                    self.assertIsNone(row.target_path)

    def test_migration0002_is_rejected_as_current_structural_authority(self) -> None:
        with self.assertRaisesRegex(OperationsAuthorityError, "Migration 0003"):
            load_task8_migration(ROOT, SEMANTIC_WITNESS_PATH)

    def test_consumer_extractor_freezes_exact_declared_and_live_union(self) -> None:
        inventory = extract_task8_consumers(ROOT, load_task8_migration(ROOT))
        self.assertEqual(315, len(inventory.declared_raw))
        self.assertEqual(tuple(sorted(set(inventory.union))), inventory.union)
        self.assertTrue(inventory.declared_current)
        self.assertGreater(inventory.tracked_files, 0)
        self.assertLessEqual(inventory.tracked_files, 10_000)
        self.assertLessEqual(inventory.tracked_bytes, 300_000_000)

    def test_consumer_extractor_rejects_unbounded_file_count_and_bytes(self) -> None:
        migration = load_task8_migration(ROOT)
        with self.assertRaisesRegex(OperationsAuthorityError, "file bound"):
            extract_task8_consumers(ROOT, migration, max_files=1)
        with self.assertRaisesRegex(OperationsAuthorityError, "bound"):
            extract_task8_consumers(ROOT, migration, max_bytes=1)

    def test_semantic_merge_witnesses_are_body_derived_and_present(self) -> None:
        self.assertEqual([], _validate_semantic_witnesses(ROOT))
        text = (ROOT / SEMANTIC_WITNESS_PATH).read_text(encoding="utf-8")
        ledger = yaml.safe_load(
            text.split("## Archive Ledger", 1)[1]
            .split("```yaml", 1)[1]
            .split("```", 1)[0]
        )
        rows = [row for row in ledger["files"] if row["semantic_action"] == "merge"]
        self.assertEqual(2, len(rows))
        for row in rows:
            source = subprocess.run(
                ["git", "show", f"{row['source_commit']}:{row['legacy_path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            target_parts = pathlib.PurePosixPath(row["final_path"]).parts
            target = pathlib.PurePosixPath(
                *(target_parts[:4] + (target_parts[4][4:],) + target_parts[5:])
            )
            current_path = ROOT / target
            if not current_path.is_file():
                current_path = ROOT / row["final_path"]
            current = current_path.read_text(encoding="utf-8")
            witnesses = [
                value.split(":", 2)[2]
                for value in row["preserved_semantics"]
                if value.startswith("text:")
            ]
            with self.subTest(target=target):
                self.assertTrue(witnesses)
                self.assertTrue(all(value in source for value in witnesses))
                self.assertTrue(all(value in current for value in witnesses))

    def test_frozen_migration_hash_is_unchanged(self) -> None:
        result = subprocess.run(
            ["sha256sum", str(MIGRATION_PATH)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        # Repinned 2026-08-29. The governance simplification projected this
        # ledger from the reviewed schema-2 form to the compact schema-3 record
        # of what executed, so the old digest pinned a file that no longer
        # exists. The rewrite is authorized independently of this constant:
        # `archive._migration_document` compares the compact selection against
        # the approved frozen digest and rejects a single changed character,
        # which was verified by mutating one `target_path` and watching it fail.
        # This pin is a second, cheaper tripwire over the same bytes, not the
        # authority for them.
        self.assertTrue(
            result.stdout.startswith(
                "0f895f395360a4b33456c7fb5a651f71efb22b566c7b74dd1aacd0884f9abb95"
            )
        )


class SemanticWitnessBoundaryTests(unittest.TestCase):
    TARGETS = (
        pathlib.PurePosixPath(
            "docs/05.operations/catalog/00-workspace/"
            "0004-harness-agent-first-engineering/runbook.md"
        ),
        pathlib.PurePosixPath(
            "docs/05.operations/catalog/07-workflow/0051-airflow-dag-lifecycle/policy.md"
        ),
    )

    def _fixture(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        migration = root / SEMANTIC_WITNESS_PATH
        migration.parent.mkdir(parents=True)
        shutil.copy2(ROOT / SEMANTIC_WITNESS_PATH, migration)
        for relative in self.TARGETS:
            target = root / relative
            target.parent.mkdir(parents=True)
            shutil.copy2(ROOT / relative, target)
        return directory, root

    @staticmethod
    def _source_result(arguments: object) -> GitCommandResult:
        assert isinstance(arguments, list)
        result = subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        return GitCommandResult(result.returncode, result.stdout, result.stderr)

    def _validate(self, root: pathlib.Path) -> list[object]:
        def bounded_git(_root: pathlib.Path, arguments: list[str], **_kwargs: object) -> GitCommandResult:
            return self._source_result(arguments)

        with mock.patch(
            "scripts.lib.document_governance.operations_catalog._run_git_bounded",
            side_effect=bounded_git,
        ):
            return _validate_semantic_witnesses(root)

    def test_markdown_body_excludes_frontmatter_and_headings(self) -> None:
        text = "---\nnote: frontmatter-only\n---\n# heading-only\nbody-only\n"
        body = _markdown_body_text(text)
        self.assertNotIn("frontmatter-only", body)
        self.assertNotIn("heading-only", body)
        self.assertIn("body-only", body)

    def test_exact_merge_row_identity_is_required(self) -> None:
        context, root = self._fixture()
        with context:
            path = root / SEMANTIC_WITNESS_PATH
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "  final_path: docs/05.operations/catalog/00-workspace/"
                    "ops-0004-harness-agent-first-engineering/runbook.md\n"
                    "  semantic_action: merge",
                    "  final_path: docs/05.operations/catalog/00-workspace/"
                    "ops-0006-infrastructure-optimization-governance/runbook.md\n"
                    "  semantic_action: merge",
                    1,
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "semantic-witness-row-invalid",
                {finding.code for finding in self._validate(root)},
            )

    def test_stale_prefixed_target_is_never_a_fallback(self) -> None:
        context, root = self._fixture()
        with context:
            current = root / self.TARGETS[0]
            stale = root / (
                "docs/05.operations/catalog/00-workspace/"
                "ops-0004-harness-agent-first-engineering/runbook.md"
            )
            stale.parent.mkdir(parents=True, exist_ok=True)
            current.rename(stale)
            codes = {finding.code for finding in self._validate(root)}
            self.assertIn("file-unreadable", codes)

    def test_empty_and_oversize_text_witnesses_are_rejected(self) -> None:
        marker = (
            "text:graphify-advisory-corroboration:"
            "bash scripts/knowledge/report-graphify-health.sh"
        )
        for replacement in ("text:graphify-advisory-corroboration:", f"text:oversize:{'x' * 4097}"):
            with self.subTest(length=len(replacement)):
                context, root = self._fixture()
                with context:
                    path = root / SEMANTIC_WITNESS_PATH
                    path.write_text(
                        path.read_text(encoding="utf-8").replace(marker, replacement, 1),
                        encoding="utf-8",
                    )
                    self.assertIn(
                        "semantic-witness-invalid",
                        {finding.code for finding in self._validate(root)},
                    )


if __name__ == "__main__":
    unittest.main()
