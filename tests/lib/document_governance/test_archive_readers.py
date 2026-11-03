"""Read-only Stage 98 loaders that current, non-archive checks still use."""

import pathlib
import tempfile
import unittest

from scripts.lib.document_governance import archive

ROOT = pathlib.Path(__file__).resolve().parents[3]

_TOMBSTONE = """---
title: "Example Tombstone"
status: "sealed"
---

# Example Tombstone

## Retired Path

`{retired}`

{recovery}## Reason

Retired for the test.
"""


class RecordedRetiredPathsTests(unittest.TestCase):
    def _root(self, tombstones: dict[str, str]) -> pathlib.Path:
        root = pathlib.Path(self.enterContext(tempfile.TemporaryDirectory()))
        partition = root / "docs/98.archive/tombstones/03.specs"
        partition.mkdir(parents=True)
        for name, text in tombstones.items():
            (partition / name).write_text(text, encoding="utf-8")
        return root

    def test_only_tombstones_with_a_recovery_commit_record_a_retirement(self) -> None:
        root = self._root(
            {
                "0001-recorded.md": _TOMBSTONE.format(
                    retired="docs/03.specs/0001-a/spec.md",
                    recovery="## Recovery Commit\n\n`0123456789abcdef`\n\n",
                ),
                "0002-route.md": _TOMBSTONE.format(
                    retired="docs/03.specs/0002-b/spec.md", recovery=""
                ),
                "0003-broken.md": "no frontmatter",
            }
        )
        self.assertEqual(
            frozenset({pathlib.PurePosixPath("docs/03.specs/0001-a/spec.md")}),
            archive.recorded_retired_paths(root),
        )

    def test_missing_archive_records_nothing(self) -> None:
        root = pathlib.Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.assertEqual(frozenset(), archive.recorded_retired_paths(root))

    def test_repository_ledger_yields_legacy_parent_identities(self) -> None:
        identities = archive.recover_legacy_parent_identities(ROOT)
        self.assertTrue(identities)
        self.assertTrue(all(isinstance(value, str) for value in identities))


if __name__ == "__main__":
    unittest.main()
