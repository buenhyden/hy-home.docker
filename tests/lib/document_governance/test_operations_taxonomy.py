from __future__ import annotations

import pathlib
import stat
import subprocess
import tempfile
import unittest

import yaml

from scripts.lib.document_governance.operations_catalog import (
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
    def test_operations_checker_is_executable_and_has_one_complete_route(
        self,
    ) -> None:
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
        for retired in ("--mode", "--domains"):
            with self.subTest(option=retired):
                self.assertNotIn(retired, result.stdout)

        # The default route runs both validations, which is what --mode
        # complete did; the other four modes were subsets of it.
        default = subprocess.run(
            [str(checker)], cwd=ROOT, capture_output=True, text=True, check=False
        )
        self.assertEqual(0, default.returncode, default.stdout + default.stderr)
        self.assertIn("operations-catalog:", default.stdout)
        rejected = subprocess.run(
            [str(checker), "--mode", "complete"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, rejected.returncode)

    def test_active_corpus_has_no_generic_predecessor_or_release_role_routes(
        self,
    ) -> None:
        self.assertEqual((), validate_active_operations_references(ROOT))

    def test_active_reference_scan_excludes_evidence_but_not_current_authority(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            fixtures = {
                "docs/00.agent-governance/active.md": (
                    "See docs/05.operations/catalog/00-workspace/"
                    "ops-####-subject/guide.md.\n"
                ),
                "docs/90.references/history.md": (
                    "See docs/05.operations/catalog/00-workspace/"
                    "ops-####-historical/guide.md.\n"
                ),
                "docs/03.specs/0998-history/plan.md": (
                    "See docs/05.operations/catalog/00-workspace/"
                    "ops-####-execution/guide.md.\n"
                ),
                "docs/03.specs/0997-retired/spec.md": (
                    "---\nprofile_id: spec\nstatus: superseded\n---\n"
                    "See docs/05.operations/catalog/00-workspace/"
                    "ops-####-retired/guide.md.\n"
                ),
                "docs/03.specs/0999-current/spec.md": (
                    "See docs/05.operations/catalog/00-workspace/"
                    "ops-####-active-spec/guide.md.\n"
                ),
                "tests/fixtures/negative.md": (
                    "See docs/05.operations/catalog/00-workspace/"
                    "ops-####-negative/guide.md.\n"
                ),
                "docs/00.agent-governance/negative.md": (
                    "No separate Release document role.\n"
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
                    "docs/00.agent-governance/active.md",
                    "docs/03.specs/0999-current/spec.md",
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
                "docs/98.archive/history.toml": (
                    'route = "docs/05.operations/guides/00-workspace/example.md"\n'
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
            "docs/05.operations/catalog/00-workspace/0003-env-key-comparison/guide.md",
            "docs/05.operations/catalog/00-workspace/"
            "0010-sensitive-env-vars-comparison/guide.md",
        )
        for relative in expected:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_public_operations_suite_owns_focused_validators_exactly_once(
        self,
    ) -> None:
        registry = load_public_suite_registry(ROOT / "scripts/manifest.yaml")
        operations = next(
            suite for suite in registry.suites if suite.name == "operations"
        )
        self.assertEqual(
            (
                pathlib.PurePosixPath(
                    "scripts/lib/ops/rehearse-postgres-logical-upgrade.sh"
                ),
                pathlib.PurePosixPath("scripts/validation/check-operations-catalog.py"),
            ),
            operations.validators,
        )
        manifest = yaml.safe_load(
            (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
        )
        rehearsal = next(
            row
            for row in manifest["files"]
            if row["path"] == "scripts/lib/ops/rehearse-postgres-logical-upgrade.sh"
        )
        self.assertEqual("validator", rehearsal["kind"])
        self.assertEqual("runtime", rehearsal["mutation"])
        self.assertEqual(["operations"], rehearsal["public_suites"])
        self.assertEqual([], rehearsal["execution_contexts"])

    def test_public_changed_profile_routes_operations_paths_fail_closed(
        self,
    ) -> None:
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
        # The twelve domain packages that also carried role links were retired:
        # they described a steady state the catalog owns, so their links moved
        # with them. What remains are bounded change packages.
        # The package is completed, so it is preserved under the archive; its
        # role links are relative to that location.
        expected = {
            "docs/98.archive/completed/03.specs/0095-infra-secrets-docs-refresh/spec.md": {
                role: (
                    "../../../../05.operations/catalog/03-security/0016-vault/"
                    f"{role.lower()}.md"
                )
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


if __name__ == "__main__":
    unittest.main()
