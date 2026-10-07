from __future__ import annotations

import pathlib
import subprocess
import tempfile
import unittest

import yaml

from scripts.lib.document_governance.operations_catalog import (
    validate_active_operations_references,
)

ROOT = pathlib.Path(__file__).resolve().parents[3]


class OperationsAuthorityTests(unittest.TestCase):
    def test_active_reference_scan_excludes_evidence_but_not_current_authority(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            fixtures = {
                ".agents/governance/active.md": (
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
                ".agents/governance/negative.md": (
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
                    ".agents/governance/active.md",
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
                    'guide="docs/05.operations/catalog/00-workspace/0001-example/guide.md"\n'
                ),
                ".github/operations.yaml": (
                    "policy: docs/05.operations/catalog/00-workspace/0001-example/policy.md\n"
                ),
                "tests/fixtures/negative.sh": (
                    'runbook="docs/05.operations/catalog/00-workspace/0001-example/runbook.md"\n'
                ),
                "docs/98.archive/history.toml": (
                    'route = "docs/05.operations/catalog/00-workspace/0001-example/guide.md"\n'
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

    def test_release_commit_pattern_is_not_a_document_role(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            fixtures = {
                "hook.md": '---\npattern: "(feat|release|deps)"\n---\n',
                "roles.md": "| Role | Owner |\n| --- | --- |\n| Release | Ops |\n",
                "roles-second-column.md": "| Owner | Role |\n| --- | --- |\n| Ops | Release |\n",
                "roles-no-leading-pipe.md": "Owner | Role | Status\n--- | --- | ---\nOps | Release | Active\n",
                "code.md": "```text\n| Role |\n| --- |\n| Release |\n```\n",
                "prose.md": "Use the Release document role.\n",
                "unicode.md": ("no release\u2028" * 5)
                + "\nOwner | Role\n--- | ---\nOps | Release\n",
            }
            for relative, content in fixtures.items():
                (root / relative).write_text(content, encoding="utf-8")
            subprocess.run(["git", "add", *fixtures], cwd=root, check=True)
            findings = validate_active_operations_references(root)
            self.assertEqual(
                {
                    "roles.md",
                    "roles-second-column.md",
                    "roles-no-leading-pipe.md",
                    "unicode.md",
                    "prose.md",
                },
                {finding.path.split(":", 1)[0] for finding in findings},
            )
            self.assertIn("unicode.md:4", {finding.path for finding in findings})

    def test_current_drift_guides_exist_at_canonical_role_paths(self) -> None:
        expected = (
            "docs/05.operations/guides/0003-env-key-comparison.md",
            "docs/05.operations/guides/0010-sensitive-env-vars-comparison.md",
        )
        for relative in expected:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_postgres_rehearsal_keeps_operations_manifest_kind(self) -> None:
        manifest = yaml.safe_load(
            (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
        )
        rehearsal = next(
            row
            for row in manifest["files"]
            if row["path"] == "scripts/operations/rehearse-postgres-logical-upgrade.sh"
        )
        self.assertEqual("operations", rehearsal["kind"])


if __name__ == "__main__":
    unittest.main()
