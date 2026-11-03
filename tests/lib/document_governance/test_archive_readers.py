"""Read-only Stage 98 loaders that current, non-archive checks still use."""

import pathlib
import subprocess
import tempfile
import unittest

from scripts.lib.document_governance import archive, requirements

ROOT = pathlib.Path(__file__).resolve().parents[3]

_TOMBSTONE = """---
title: "Example Tombstone"
type: "{kind}"
status: "{status}"
artifact_id: "{artifact_id}"
---

# Example Tombstone

## Retired Path

`{retired}`

## Recovery Commit

`{commit}`

## Reason

Retired for the test.
"""


def _git(root: pathlib.Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()


class SealedTombstoneReaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = pathlib.Path(self.enterContext(tempfile.TemporaryDirectory()))
        _git(self.root, "init", "-q")
        _git(self.root, "config", "user.name", "Reader Test")
        _git(self.root, "config", "user.email", "reader@example.invalid")
        retired = self.root / "docs/03.specs/0001-a/spec.md"
        retired.parent.mkdir(parents=True)
        retired.write_text("retired body\n", encoding="utf-8")
        _git(self.root, "add", ".")
        _git(self.root, "commit", "-qm", "add the retired body")
        self.commit = _git(self.root, "rev-parse", "HEAD")
        retired.unlink()
        self.partition = self.root / "docs/98.archive/tombstones/03.specs"
        self.partition.mkdir(parents=True)

    def _write(self, name: str, **values: str) -> None:
        fields = {
            "kind": "archive/tombstone",
            "status": "sealed",
            "artifact_id": "tomb-SPEC-0001",
            "retired": "docs/03.specs/0001-a/spec.md",
            "commit": self.commit,
            **values,
        }
        (self.partition / name).write_text(
            _TOMBSTONE.format(**fields), encoding="utf-8"
        )

    def test_a_sealed_tombstone_with_a_proven_blob_records_a_retirement(self) -> None:
        self._write("0001-recorded.md")
        self.assertEqual(
            frozenset({pathlib.PurePosixPath("docs/03.specs/0001-a/spec.md")}),
            archive.recorded_retired_paths(self.root),
        )

    def test_a_record_failing_the_minimal_contract_grants_no_exemption(self) -> None:
        cases = {
            "not-sealed": {"status": "draft"},
            "wrong-type": {"kind": "archive/migration"},
            "bad-commit": {"commit": "not-a-commit"},
            "unknown-commit": {"commit": "0" * 40},
            "path-not-at-commit": {"retired": "docs/03.specs/0002-b/spec.md"},
        }
        for label, values in cases.items():
            with self.subTest(case=label):
                for existing in self.partition.iterdir():
                    existing.unlink()
                self._write("0001-candidate.md", **values)
                self.assertEqual(frozenset(), archive.recorded_retired_paths(self.root))

    def test_missing_archive_records_nothing(self) -> None:
        root = pathlib.Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.assertEqual(frozenset(), archive.recorded_retired_paths(root))

    def test_requirement_gaps_need_a_sealed_tombstone(self) -> None:
        tombstones = self.root / "tombstones"
        tombstones.mkdir()
        for name, status in (("0001-sealed.md", "sealed"), ("0002-draft.md", "draft")):
            (tombstones / name).write_text(
                _TOMBSTONE.format(
                    kind="archive/tombstone",
                    status=status,
                    artifact_id=f"tomb-REQ-000{name[3]}",
                    retired=f"docs/01.requirements/000{name[3]}-x.md",
                    commit=self.commit,
                ),
                encoding="utf-8",
            )
        self.assertEqual(
            frozenset({"REQ-0001"}),
            requirements._tombstoned_requirement_ids(self.root, tombstones),
        )


class LegacyLineageReaderTests(unittest.TestCase):
    def test_repository_ledger_yields_legacy_parent_identities(self) -> None:
        identities = archive.recover_legacy_parent_identities(ROOT)
        self.assertTrue(identities)
        self.assertTrue(all(isinstance(value, str) for value in identities))


if __name__ == "__main__":
    unittest.main()
