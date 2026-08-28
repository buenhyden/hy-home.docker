from __future__ import annotations

import os
import pathlib
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[3]


def policy_api():
    try:
        from scripts.lib.document_governance import provenance_policy
    except ImportError as exc:
        raise AssertionError("Task 10 provenance policy is missing") from exc
    return provenance_policy


class ProvenancePolicyTests(unittest.TestCase):
    def test_integration_guidance_preserves_exact_recovery_history(self) -> None:
        for relative in ("docs/00.agent-governance/policies/github-governance.md", "docs/00.agent-governance/policies/git-workflow.md", ".github/rulesets/main-protection.md"):
            with self.subTest(path=relative):
                text = " ".join((ROOT / relative).read_text(encoding="utf-8").split()).lower()
                self.assertIn("recovery commits", text)
                self.assertIn("merge commit", text)
                self.assertIn("fast-forward", text)
                self.assertNotIn("prefer squash or rebase", text)
        policy = (ROOT / "docs/00.agent-governance/policies/github-governance.md").read_text()
        self.assertIn("only after referenced recovery commits are reachable", policy)
        self.assertIn("verify recovery blobs after integration", policy)

    def setUp(self) -> None:
        self.policy = policy_api()

    def finding_codes(self, path: str, text: str) -> set[str]:
        return {
            item.code
            for item in self.policy.validate_provenance_text(
                pathlib.PurePosixPath(path), text
            )
        }

    def test_prohibited_repository_provenance_forms_are_rejected(self) -> None:
        mutations = {
            "branch-snapshot-prohibited": "branch_snapshot: feature/archive\n",
            "line-sha-prohibited": "recovery_commit: deadbeef:42\n",
            "snapshot-count-prohibited": "archive_snapshot_count: 184\n",
            "fixed-head-fixture-prohibited": "EXPECTED_HEAD = \"" + "a" * 40 + "\"\n",
            "duplicate-digest-prohibited": "content_sha256: " + "b" * 64 + "\narchived_blob: " + "c" * 40 + "\n",
        }
        for code, text in mutations.items():
            with self.subTest(code=code):
                self.assertIn(code, self.finding_codes("docs/current.md", text))

    def test_allowed_security_recovery_generated_and_runtime_provenance(self) -> None:
        fixtures = {
            "infra/pins.json": '{"image":"example.invalid/tool@sha256:' + "a" * 64 + '"}\n',
            "docs/98.archive/tombstones/03.specs/0001-old.md": "## Recovery Commit\n\n`" + "b" * 40 + "`\n",
            "docs/90.references/data/0001-generated/README.md": "generated_by: scripts/generate.py\ncontent_sha256: " + "c" * 64 + "\n",
            ".github/workflows/ci.yml": "base: ${{ github.event.pull_request.base.sha }}\nhead: ${{ github.sha }}\n",
        }
        for path, text in fixtures.items():
            with self.subTest(path=path):
                self.assertEqual(set(), self.finding_codes(path, text))

    def test_active_documents_may_not_link_individual_tombstones(self) -> None:
        self.assertIn(
            "active-tombstone-link-prohibited",
            self.finding_codes(
                "docs/03.specs/0001-current/spec.md",
                "[old](../../98.archive/tombstones/03.specs/0001-old.md)\n",
            ),
        )
        self.assertEqual(
            set(),
            self.finding_codes(
                "docs/03.specs/0001-current/spec.md",
                "[archive](../../98.archive/README.md) [migration](../../98.archive/migrations/0001-map.md)\n",
            ),
        )

    def test_superseded_adr_must_not_be_archived(self) -> None:
        self.assertIn(
            "superseded-adr-archive-prohibited",
            self.finding_codes(
                "docs/98.archive/tombstones/02.architecture/0001-choice.md",
                "## Retired Path\n\n`docs/02.architecture/decisions/0001-choice.md`\n",
            ),
        )

    def test_repository_scan_covers_authored_docs_scripts_tests_and_config(self) -> None:
        mutations = {
            "docs/00.agent-governance/policies/source.md": (
                "branch-snapshot-prohibited",
                'branch_snapshot = "feature/archive"\n',
            ),
            "scripts/validation/check-provenance.py": (
                "fixed-head-fixture-prohibited",
                "EXPECTED_HEAD = \"" + "a" * 40 + "\"\n",
            ),
            "tests/fixtures/fixed-head.py": (
                "fixed-head-fixture-prohibited",
                "EXPECTED_HEAD = \"" + "9" * 40 + "\"\n",
            ),
            "tests/test_recovery.py": (
                "line-sha-prohibited",
                'LINE_SHA = "deadbeef:42"\n',
            ),
            ".codex/provenance.toml": (
                "duplicate-digest-prohibited",
                'content_sha256 = "' + "b" * 64 + '"\narchived_blob = "' + "c" * 40 + '"\n',
            ),
            ".github/workflow-contract.yml": (
                "fixed-head-fixture-prohibited",
                "EXPECTED_HEAD = \"" + "1" * 40 + "\"\n",
            ),
            "infra/provenance.toml": (
                "line-sha-prohibited",
                'recovery_commit = "deadbeef:42"\n',
            ),
            "docs/90.references/data/0001-evidence/unsafe.yaml": (
                "branch-snapshot-prohibited",
                "branch_snapshot: feature/archive\n",
            ),
            "docs/98.archive/migrations/0001-unsafe.md": (
                "snapshot-count-prohibited",
                "archive_snapshot_count: 184\n",
            ),
            "docs/99.templates/support/unsafe.yaml": (
                "branch-snapshot-prohibited",
                "branch_snapshot: feature/templates\n",
            ),
            "docs/99.templates/templates/common/unsafe.md": (
                "duplicate-digest-prohibited",
                "content_sha256: " + "2" * 64 + "\narchived_blob: " + "3" * 40 + "\n",
            ),
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            for relative, (_, text) in mutations.items():
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")

            findings = self.policy.validate_repository_provenance(root)
            actual = {(item.path, item.code) for item in findings}
            self.assertEqual(
                {(path, code) for path, (code, _) in mutations.items()},
                actual,
            )

    def test_repository_scan_rejects_a_minimal_superseded_adr_tombstone(self) -> None:
        from scripts.lib.document_governance import archive

        text = """---
profile_id: tombstone
status: completed
artifact_id: tombstone-0001
artifact_type: tombstone
parent_ids: [mig-0001]
created: 2026-08-27
updated: 2026-08-27
---

# Superseded ADR Tombstone

## Retired Path

`docs/02.architecture/decisions/0001-choice.md`

## Replacement

none

## Reason

The decision was superseded.

## Recovery Commit

`1111111111111111111111111111111111111111`

## Traceability

- [Archive index](../../README.md)
"""
        relative = pathlib.PurePosixPath(
            "docs/98.archive/tombstones/02.architecture/0001-choice.md"
        )
        record = archive._parse_tombstone_text(text, relative, relative.name)
        self.assertTrue(record.is_minimal)
        with tempfile.TemporaryDirectory() as temporary:
            target = pathlib.Path(temporary) / relative
            target.parent.mkdir(parents=True)
            target.write_text(text, encoding="utf-8")
            findings = self.policy.validate_repository_provenance(pathlib.Path(temporary))
        self.assertIn(
            (relative.as_posix(), "superseded-adr-archive-prohibited"),
            {(item.path, item.code) for item in findings},
        )

    def test_repository_scan_excludes_history_generated_and_binary_inputs(self) -> None:
        fixed_head = "EXPECTED_HEAD = \"" + "d" * 40 + "\"\n"
        excluded = (
            ".git/objects/fake.py",
            ".worktrees/branch/scripts/fake.py",
            "graphify-out/generated.py",
            "scripts/generated/fake.py",
            "infra/build/fake.py",
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            for relative in excluded:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(fixed_head, encoding="utf-8")
            binary = root / "scripts" / "fixture.bin"
            binary.parent.mkdir(parents=True, exist_ok=True)
            binary.write_bytes(b"EXPECTED_HEAD = \"" + b"e" * 40 + b"\"\x00")

            allowed = {
                "infra/security-pins.toml": 'image = "example.invalid/tool@sha256:' + "a" * 64 + '"\n',
                ".github/workflows/ci.yml": (
                    "base: ${{ github.event.pull_request.base.sha }}\nhead: ${{ github.sha }}\n"
                ),
                "docs/98.archive/tombstones/03.specs/0001-old.md": (
                    "## Recovery Commit\n\n`" + "b" * 40 + "`\n"
                ),
                "docs/90.references/data/0001-generated/README.md": (
                    "generated_by: scripts/generate.py\ncontent_sha256: " + "c" * 64 + "\n"
                ),
            }
            for relative, text in allowed.items():
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")

            self.assertEqual((), self.policy.validate_repository_provenance(root))

    def test_repository_scan_does_not_follow_leaf_or_ancestor_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            outside = root / "outside"
            outside.mkdir()
            bad = outside / "bad.py"
            bad.write_text("EXPECTED_HEAD = \"" + "f" * 40 + "\"\n", encoding="utf-8")

            scripts = root / "scripts"
            scripts.mkdir()
            os.symlink(bad, scripts / "leaf.py")
            leaf_findings = self.policy.validate_repository_provenance(root)
            self.assertIn(
                ("scripts/leaf.py", "provenance-input-invalid"),
                {(item.path, item.code) for item in leaf_findings},
            )

            (scripts / "leaf.py").unlink()
            scripts.rmdir()
            os.symlink(outside, scripts)
            ancestor_findings = self.policy.validate_repository_provenance(root)
            self.assertIn(
                ("scripts", "provenance-input-invalid"),
                {(item.path, item.code) for item in ancestor_findings},
            )

    def test_repository_scan_caps_directory_before_sorting(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            scripts = root / "scripts"
            scripts.mkdir()
            for name in ("z.py", "a.py"):
                (scripts / name).write_text("value = 1\n", encoding="utf-8")

            with mock.patch.object(self.policy, "_MAX_DIRECTORY_ENTRIES", 1):
                findings = self.policy.validate_repository_provenance(root)
            self.assertIn(
                ("scripts", "provenance-directory-entry-count-exceeded"),
                {(item.path, item.code) for item in findings},
            )

    def test_current_repository_has_no_provenance_policy_findings(self) -> None:
        findings = self.policy.validate_repository_provenance(ROOT)
        self.assertEqual((), findings)


if __name__ == "__main__":
    unittest.main()
