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
    "| Path | Anchor | Literal class | Reason | Review |\n"
    "| --- | --- | --- | --- | --- |\n"
)

# Every clickable form the review measured as evading the first implementation.
# Each must be detected both on its own and inside a reviewed-allowlisted file,
# because gate 4 admits no clickable-link exception.
EVASIONS = {
    "inline": f"[a]({SLUG}/x.md)",
    "dot_slash": f"[a](./{SLUG}/x.md)",
    "angle_bracket": f"[a](<../{SLUG}/x.md>)",
    "directory_without_trailing_slash": f"[a](../research/{SLUG})",
    "reference_definition": f"[a][r]\n\n[r]: ../{SLUG}/x.md",
    "html_href": f'<a href="../{SLUG}/x.md">a</a>',
    "split_across_lines": f"[a](../{SLUG}/\nx.md)",
    "percent_encoded_slash": f"[a](..%2F{SLUG}%2Fx.md)",
    # Built from parts rather than written out, so this file does not itself
    # contain a percent-decodable copy of the slug. Writing the literal here
    # made the scanner report its own test file, correctly.
    "percent_encoded_slug_character": (f"[a](../{SLUG[:-2]}%73{SLUG[-1]}/x.md)"),
    "autolink": f"<../{SLUG}/x.md>",
    "uppercased_slug": f"[a](../{SLUG.upper()}/x.md)",
    # Forms the fix-round-1 re-review measured as still escaping.
    "query_string_terminator": f"[a](../{SLUG}?x=1)",
    "fragment_terminator": f"[a](../{SLUG}#frag)",
    "unquoted_html_attribute": f"<a href=../{SLUG}/x.md>a</a>",
    # Also assembled at runtime: written out, the entity decodes to the slug and
    # the scanner reports this file, which is correct behaviour.
    "html_numeric_entity": (f'<a href="../&#{ord(SLUG[0])};{SLUG[1:]}/x.md">a</a>'),
    "image": f"![a](../{SLUG}/x.png)",
    "destination_with_title": f'[a](../{SLUG}/x.md "t")',
    "img_src": f'<img src="../{SLUG}/x.png">',
    "true_multiline_destination": f"[a](../\n{SLUG}/x.md)",
}


def codes(findings: list[contract.Finding]) -> set[str]:
    return {finding.code for finding in findings}


class OldPathGateFixtureTests(unittest.TestCase):
    """Behaviour against synthetic repositories under the system temp root."""

    def _repo(self, directory: str) -> pathlib.Path:
        root = pathlib.Path(directory)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        (root / "docs/04.execution/tasks").mkdir(parents=True)
        (root / contract.TASK_PATH).write_text(ALLOWLIST_HEADER, encoding="utf-8")
        return root

    def _commit(self, root: pathlib.Path) -> None:
        subprocess.run(
            ["git", "-C", str(root), "add", "-A"], check=True, capture_output=True
        )

    def _allow(
        self,
        root: pathlib.Path,
        *paths: str,
        verdict: str = "reviewed",
        literal_class: str = "Factual history",
        anchor: str = "# anchor",
    ) -> None:
        rows = "".join(
            f"| `{path}` | `{anchor}` | {literal_class} | reason | {verdict} |\n"
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
            result = contract.scan(root)
            self.assertEqual([], result.findings)
            self.assertEqual(0, result.generated_occurrences)

    def test_every_clickable_form_is_detected(self) -> None:
        """Each form the review measured as an escape must now be caught."""
        for name, body in EVASIONS.items():
            with self.subTest(form=name):
                with tempfile.TemporaryDirectory() as directory:
                    root = self._repo(directory)
                    (root / "docs/leaf.md").write_text(body + "\n", encoding="utf-8")
                    self._commit(root)
                    result = contract.scan(root)
                    self.assertIn("OLD-PATH-CLICKABLE-LINK", codes(result.findings))

    def test_no_clickable_form_is_suppressed_by_the_allowlist(self) -> None:
        """The amplification the review found: a reviewed row swallowed five forms."""
        for name, body in EVASIONS.items():
            with self.subTest(form=name):
                with tempfile.TemporaryDirectory() as directory:
                    root = self._repo(directory)
                    (root / "docs/leaf.md").write_text(body + "\n", encoding="utf-8")
                    self._allow(root, "docs/leaf.md")
                    self._commit(root)
                    result = contract.scan(root)
                    self.assertIn("OLD-PATH-CLICKABLE-LINK", codes(result.findings))

    def test_unallowlisted_literal_is_a_finding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/note.md").write_text(f"`{SLUG}/`\n", encoding="utf-8")
            self._commit(root)
            result = contract.scan(root)
            self.assertEqual({"OLD-PATH-UNALLOWLISTED"}, codes(result.findings))

    def test_allowlisted_literal_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/note.md").write_text(f"`{SLUG}/`\n", encoding="utf-8")
            self._allow(root, "docs/note.md")
            self._commit(root)
            result = contract.scan(root)
            self.assertEqual([], result.findings)

    def test_forbidden_literal_class_grants_nothing(self) -> None:
        """Spec 137 denies an allowlist to routers and canonical-owner statements."""
        for literal_class in (
            "Current router",
            "Generated navigation",
            "Canonical-owner statement",
            "Mutable configuration route",
        ):
            with self.subTest(literal_class=literal_class):
                with tempfile.TemporaryDirectory() as directory:
                    root = self._repo(directory)
                    (root / "docs/note.md").write_text(f"`{SLUG}/`\n", encoding="utf-8")
                    self._allow(root, "docs/note.md", literal_class=literal_class)
                    self._commit(root)
                    result = contract.scan(root)
                    self.assertEqual(
                        {"OLD-PATH-FORBIDDEN-CLASS"}, codes(result.findings)
                    )

    def test_retiring_directory_itself_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            inside = root / contract.RETIRING_DIR
            inside.mkdir(parents=True)
            (inside / "leaf.md").write_text(
                f"[self]({SLUG}/leaf.md) and `{SLUG}/`\n", encoding="utf-8"
            )
            self._commit(root)
            result = contract.scan(root)
            self.assertEqual([], result.findings)

    def test_prefix_sibling_directory_is_still_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            sibling = root / f"docs/90.references/research/{SLUG}-notes"
            sibling.mkdir(parents=True)
            (sibling / "n.md").write_text(f"`{SLUG}/`\n", encoding="utf-8")
            self._commit(root)
            result = contract.scan(root)
            self.assertEqual({"OLD-PATH-UNALLOWLISTED"}, codes(result.findings))

    def test_generated_surface_counts_occurrences_not_lines(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            generated = root / "graphify-out"
            generated.mkdir()
            (generated / "GRAPH_REPORT.md").write_text(
                f"`{SLUG}/` and `{SLUG}/` again\n", encoding="utf-8"
            )
            self._commit(root)
            result = contract.scan(root)
            self.assertEqual([], result.findings)
            self.assertEqual(2, result.generated_occurrences)

    def test_clickable_link_inside_the_generated_surface_still_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            generated = root / "graphify-out"
            generated.mkdir()
            (generated / "GRAPH_REPORT.md").write_text(
                f"[a](../{SLUG}/x.md)\n", encoding="utf-8"
            )
            self._commit(root)
            result = contract.scan(root)
            self.assertIn("OLD-PATH-CLICKABLE-LINK", codes(result.findings))

    def test_untracked_file_is_not_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            self._commit(root)
            (root / "docs/untracked.md").write_text(
                f"[x]({SLUG}/y.md)\n", encoding="utf-8"
            )
            result = contract.scan(root)
            self.assertEqual([], result.findings)

    def test_binary_file_does_not_crash_the_scan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "blob.bin").write_bytes(b"\x00\xff\xfe binary")
            self._commit(root)
            result = contract.scan(root)
            self.assertEqual([], result.findings)

    def test_escaped_pipe_in_a_cell_does_not_shift_the_verdict_column(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/note.md").write_text(f"`{SLUG}/`\n", encoding="utf-8")
            (root / contract.TASK_PATH).write_text(
                ALLOWLIST_HEADER
                + "| `docs/note.md` | `# a` | Factual history | a \\| b | reviewed |\n",
                encoding="utf-8",
            )
            self._commit(root)
            result = contract.scan(root)
            self.assertEqual([], result.findings)

    def test_a_deeper_heading_ends_the_allowlist_table(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/note.md").write_text(f"`{SLUG}/`\n", encoding="utf-8")
            (root / contract.TASK_PATH).write_text(
                ALLOWLIST_HEADER
                + "#### Unrelated\n\n"
                + "| Path | Anchor | Literal class | Reason | Review |\n"
                + "| --- | --- | --- | --- | --- |\n"
                + "| `docs/note.md` | `# a` | Factual history | r | reviewed |\n",
                encoding="utf-8",
            )
            self._commit(root)
            result = contract.scan(root)
            self.assertEqual({"OLD-PATH-UNALLOWLISTED"}, codes(result.findings))


class SettledVerdictTests(unittest.TestCase):
    """The verdict predicate, including every case the review measured."""

    SETTLED = (
        "Approved C0/I0/M0",
        "Task 10b boundary reviewed; lifecycle reconciliation pending after deletion",
        "Focused GREEN and freshness PASS; scoped re-reviews Approved C0/I0/M0",
        # A closed round narrated in the past must not demote the row.
        "quality Needs fixes on the omission; Step 8 then received both external "
        "C0/I0/M0 approvals",
        # Ordinary approved wording that a blanket negation list demoted.
        "Approved; no new findings",
        "Approved; no Critical or Important findings",
        "Reviewed; no blocking findings",
        "Approved; non-blocking Minors only",
        "Approved, none outstanding",
    )
    UNSETTLED = (
        "",
        "Not Run",
        "independent pack review pending",
        "Not Run; independent review requested 2026-08-18",
        "review not approved",
        "NOT approved",
        "review pending; gates do not pass yet",
        "no review; will PASS later",
        "REVIEWED-BY-NOBODY",
        "independent review returned an Important finding; not approved",
        # Dropped from this fixture last round instead of being fixed.
        "pre-reviewed draft",
        "un-reviewed",
        "to be reviewed",
        "will be reviewed after deletion",
        "scheduled to be reviewed",
        "self-reviewed only",
        # The severity token must not outrank an explicit negation.
        "Not Run; C0/I0 placeholder",
        "review not approved, C0/I0",
        "no review happened; C0/I0",
        "Not Run; awaiting C0/I0 confirmation",
        "specification Approved C0/I0/M5; quality Needs fixes C0/I2/M10",
    )

    def test_settled_forms(self) -> None:
        for verdict in self.SETTLED:
            with self.subTest(verdict=verdict):
                self.assertTrue(contract._is_settled(verdict))

    def test_unsettled_forms(self) -> None:
        for verdict in self.UNSETTLED:
            with self.subTest(verdict=verdict):
                self.assertFalse(contract._is_settled(verdict))

    def test_bare_pass_alone_does_not_settle(self) -> None:
        """The review measured that the bare word carried no live row."""
        self.assertFalse(contract._is_settled("gates pass in the next unit"))


class OldPathGateRepositoryTests(unittest.TestCase):
    """Behaviour against the live repository."""

    EXPECTED_UNREVIEWED = {
        "docs/04.execution/tasks/2026-08-11-agentic-research-pack-source-refresh.md",
        "docs/04.execution/tasks/2026-08-14-agentic-research-pack-deepening.md",
        "scripts/validation/agentic-research-gate9-evidence.py",
        "scripts/validation/old_path_gate_contract.py",
        "tests/validation/test_agentic_research_gate9_evidence.py",
    }

    def test_allowlist_split_is_exact(self) -> None:
        """Pins the split, so a forced-settled regression cannot survive."""
        rows = contract.read_allowlist(ROOT)
        unreviewed = {path for path, row in rows.items() if not row.settled}
        self.assertEqual(self.EXPECTED_UNREVIEWED, unreviewed)
        self.assertEqual(34, sum(1 for row in rows.values() if row.settled))

    def test_no_live_row_declares_a_forbidden_class(self) -> None:
        rows = contract.read_allowlist(ROOT)
        offenders = [path for path, row in rows.items() if row.forbidden_class]
        self.assertEqual([], offenders)

    def test_no_clickable_old_pack_link_survives(self) -> None:
        """Gate 4's absolute half: this must stay at zero."""
        result = contract.scan(ROOT)
        clickable = [
            finding
            for finding in result.findings
            if finding.code == "OLD-PATH-CLICKABLE-LINK"
        ]
        self.assertEqual([], clickable, f"clickable old-pack links: {clickable}")


if __name__ == "__main__":
    unittest.main()
