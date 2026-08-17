#!/usr/bin/env python3
"""Tests for the Spec 137 pre-deletion gate 4 contract."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "validation"))

import old_path_gate_contract as contract  # noqa: E402

SLUG = contract.SLUG
ALLOWLIST_HEADER = (
    "### Old-path allowlist\n\n"
    "| Path | Anchor | Class | Reason | Review |\n"
    "| --- | --- | --- | --- | --- |\n"
)


def codes(findings: list[contract.Finding]) -> set[str]:
    return {finding.code for finding in findings}


class OldPathGateFixtureTests(unittest.TestCase):
    """Behaviour against synthetic repositories under /tmp."""

    def _repo(self, directory: str) -> pathlib.Path:
        root = pathlib.Path(directory)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        (root / "docs/04.execution/tasks").mkdir(parents=True)
        (root / contract.TASK_PATH).write_text(ALLOWLIST_HEADER, encoding="utf-8")
        return root

    def _commit(self, root: pathlib.Path) -> None:
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)

    def _allow(self, root: pathlib.Path, *paths: str) -> None:
        rows = "".join(
            f"| `{path}` | `# anchor` | Factual history | reason | reviewed |\n"
            for path in paths
        )
        (root / contract.TASK_PATH).write_text(
            ALLOWLIST_HEADER + rows, encoding="utf-8"
        )

    def test_clean_repository_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/note.md").write_text("no old path here\n", encoding="utf-8")
            self._commit(root)
            findings, generated = contract.scan(root)
            self.assertEqual([], findings)
            self.assertEqual(0, generated)

    def test_clickable_link_is_a_finding(self) -> None:
        """The exact regression class that survived five days undetected."""
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/leaf.md").write_text(
                f"| [Predecessor]({SLUG}/workspace-baseline.md) | row |\n",
                encoding="utf-8",
            )
            self._commit(root)
            findings, _ = contract.scan(root)
            self.assertEqual({"OLD-PATH-CLICKABLE-LINK"}, codes(findings))
            self.assertEqual(1, findings[0].line)

    def test_clickable_link_is_a_finding_even_when_allowlisted(self) -> None:
        """Gate 4 admits no clickable-link exception, allowlist notwithstanding."""
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/leaf.md").write_text(
                f"[x](../{SLUG}/README.md)\n", encoding="utf-8"
            )
            self._allow(root, "docs/leaf.md")
            self._commit(root)
            findings, _ = contract.scan(root)
            self.assertEqual({"OLD-PATH-CLICKABLE-LINK"}, codes(findings))

    def test_unallowlisted_literal_is_a_finding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/note.md").write_text(f"`{SLUG}/`\n", encoding="utf-8")
            self._commit(root)
            findings, _ = contract.scan(root)
            self.assertEqual({"OLD-PATH-UNALLOWLISTED"}, codes(findings))

    def test_allowlisted_literal_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/note.md").write_text(f"`{SLUG}/`\n", encoding="utf-8")
            self._allow(root, "docs/note.md")
            self._commit(root)
            findings, _ = contract.scan(root)
            self.assertEqual([], findings)

    def test_retiring_directory_itself_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            inside = root / contract.RETIRING_DIR
            inside.mkdir(parents=True)
            (inside / "leaf.md").write_text(
                f"[self]({SLUG}/leaf.md) and `{SLUG}/`\n", encoding="utf-8"
            )
            self._commit(root)
            findings, _ = contract.scan(root)
            self.assertEqual([], findings)

    def test_generated_surface_is_counted_not_failed(self) -> None:
        """Never silently dropped: the occurrence count is always reported."""
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            generated = root / "graphify-out"
            generated.mkdir()
            (generated / "GRAPH_REPORT.md").write_text(
                f"[a]({SLUG}/x.md)\n`{SLUG}/`\n", encoding="utf-8"
            )
            self._commit(root)
            findings, count = contract.scan(root)
            self.assertEqual([], findings)
            self.assertEqual(2, count)

    def test_untracked_file_is_not_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            self._commit(root)
            (root / "docs/untracked.md").write_text(
                f"[x]({SLUG}/y.md)\n", encoding="utf-8"
            )
            findings, _ = contract.scan(root)
            self.assertEqual([], findings)

    def test_binary_file_does_not_crash_the_scan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "blob.bin").write_bytes(b"\x00\xff\xfe binary")
            self._commit(root)
            findings, _ = contract.scan(root)
            self.assertEqual([], findings)


class OldPathGateRepositoryTests(unittest.TestCase):
    """Behaviour against the live repository."""

    def test_allowlist_parses_from_the_task(self) -> None:
        allowed = contract.read_allowlist(ROOT)
        self.assertGreaterEqual(len(allowed), 30)
        self.assertTrue(all(not path.startswith("`") for path in allowed))

    def test_no_clickable_old_pack_link_survives(self) -> None:
        """Gate 4's absolute half: this must stay at zero."""
        findings, _ = contract.scan(ROOT)
        clickable = [
            finding for finding in findings if finding.code == "OLD-PATH-CLICKABLE-LINK"
        ]
        self.assertEqual([], clickable, f"clickable old-pack links: {clickable}")


if __name__ == "__main__":
    unittest.main()
