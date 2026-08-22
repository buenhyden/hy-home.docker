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

# Clickable forms this fixture pins. Some evaded an earlier implementation and
# some are baseline forms that must not regress; per-entry comments mark which.
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
        (root / contract.TASK_PATH).parent.mkdir(parents=True)
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

    def _rows_for(self, tail: str) -> list[str]:
        live = "| `real/live.md` | `# h` | Factual history | r | Approved C0/I0/M0 |\n"
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "docs/04.execution/tasks").mkdir(parents=True)
            (root / contract.TASK_PATH).write_text(
                ALLOWLIST_HEADER + live + tail, encoding="utf-8"
            )
            return sorted(contract.read_allowlist(root))

    def test_only_live_rows_grant_exemptions(self) -> None:
        """Rows that are illustrative, commented, or past the table grant nothing.

        Each case below was a real leak. The ATX-heading and single-fence cases
        were fixed a round earlier but shipped unpinned, so a reviewer's mutants
        of both survived the suite; they are held here alongside the new ones.
        """
        dead = "| `dead/row.md` | `# h` | Factual history | r | reviewed |\n"
        later = (
            "\n| Path | Anchor | Literal class | Reason | Review |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| `leak/after.md` | `# h` | Factual history | r | reviewed |\n"
        )
        cases = {
            "atx_heading_ends_table": "# Later\n" + later,
            "setext_heading_ends_table": "\nLater\n=====\n" + later,
            "backtick_fence": "```\n" + dead + "```\n",
            "tilde_fence": "~~~\n" + dead + "~~~\n",
            "mismatched_fence_does_not_reopen": "```\n" + dead + "~~~\n" + dead,
            "unclosed_fence_admits_nothing_after": "```\n" + dead,
            # Four or more spaces is code content, not a fence, so treating it
            # as one closed a fence CommonMark keeps open and let the rows
            # after it become live grants.
            "four_space_indent_does_not_close": (
                "```\n" + dead + "    ```\n" + dead + "```\n"
            ),
            "single_line_comment": "<!-- " + dead.strip() + " -->\n",
            "block_comment": "<!--\n" + dead + "-->\n",
            # A ``` does not close a ```` block, and a closing fence carries no
            # info string; both let illustrative rows back in as live grants.
            "shorter_fence_does_not_close": "````\n" + dead + "```\n" + dead + "````\n",
            "info_string_does_not_close": "```\n" + dead + "```text\n" + dead + "```\n",
        }
        for name, tail in cases.items():
            with self.subTest(case=name):
                self.assertEqual(["real/live.md"], self._rows_for(tail))

    def test_state_resumes_after_an_illustrative_block(self) -> None:
        """A row AFTER a skipped block must still be a live grant.

        Asserting only that nothing leaks is a half test: it passes whether the
        block ends correctly or swallows the rest of the table. A fence opened
        inside an HTML comment ate the closing `-->` and dropped every later
        row, and a fixture with no trailing row could not see it.
        """
        dead = "| `dead/row.md` | `# h` | Factual history | r | reviewed |\n"
        after = "| `after/row.md` | `# h` | Factual history | r | Approved C0/I0/M0 |\n"
        cases = {
            "fence_inside_comment": "<!--\n```\n-->\n" + after,
            "block_comment": "<!--\n" + dead + "-->\n" + after,
            "closed_backtick_fence": "```\n" + dead + "```\n" + after,
            # A four-space run outside a fence must not OPEN one, or every
            # row after it is silently dropped.
            "four_space_indent_does_not_open": "    ```\n" + after,
            "shorter_fence_does_not_close": (
                "````\n" + dead + "```\n" + dead + "````\n" + after
            ),
            "info_string_does_not_close": (
                "```\n" + dead + "```text\n" + dead + "```\n" + after
            ),
        }
        for name, tail in cases.items():
            with self.subTest(case=name):
                self.assertEqual(["after/row.md", "real/live.md"], self._rows_for(tail))

    def test_unrunnable_conditions_are_distinguishable_from_failure(self) -> None:
        """Exit 2 must cover every "cannot run", not only a missing Task.

        The exception's own docstring said "missing or unreadable" while only
        missing was covered, so an unreadable Task, an undecodable one, and a
        root that is not a repository each produced a bare traceback at exit 1
        -- indistinguishable from a legitimate gate failure.
        """
        header = "### Old-path allowlist\n"
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            task = root / contract.TASK_PATH
            task.parent.mkdir(parents=True)

            task.write_text(header, encoding="utf-8")
            self.assertEqual(2, contract.main(["--root", str(root)]), "not a repo")

            subprocess.run(["git", "init", "-q", str(root)], check=True)
            task.write_bytes(b"\xff\xfe not utf-8")
            self.assertEqual(2, contract.main(["--root", str(root)]), "undecodable")

            # The OSError half shipped unpinned and a reviewer's mutant
            # survived. A chmod-based fixture is NOT usable here: this
            # platform's temp filesystem does not enforce permissions, so the
            # guard skipped and the test passed vacuously. Patching the read
            # is deterministic everywhere.
            task.write_text("### Old-path allowlist\n", encoding="utf-8")
            real_read = pathlib.Path.read_text

            def refuse(self, *args, **kwargs):
                if self.name == pathlib.Path(contract.TASK_PATH).name:
                    raise OSError(13, "Permission denied")
                return real_read(self, *args, **kwargs)

            pathlib.Path.read_text = refuse
            try:
                self.assertEqual(
                    2, contract.main(["--root", str(root)]), "unreadable"
                )
            finally:
                pathlib.Path.read_text = real_read

    def test_a_tracked_path_that_is_not_a_file_is_counted(self) -> None:
        # `is_file()` sat outside the read guard and its skip was uncounted.
        # A tracked file removed from the working tree exercises that branch
        # deterministically: git still lists it, the path does not exist.
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/gone.md").write_text("x\n", encoding="utf-8")
            (root / contract.TASK_PATH).write_text(ALLOWLIST_HEADER, encoding="utf-8")
            self._commit(root)
            (root / "docs/gone.md").unlink()
            self.assertEqual(1, contract.scan(root).unreadable_files)

    def test_a_scan_read_failure_is_counted_not_raised(self) -> None:
        """The scan loop's OSError half is a separate site from the Task's.

        A mutant reverting this one survived while the Task-side guard was
        pinned, because no fixture made an ordinary tracked file fail to read.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/leaf.md").write_text("x\n", encoding="utf-8")
            (root / contract.TASK_PATH).write_text(ALLOWLIST_HEADER, encoding="utf-8")
            self._commit(root)
            real_read = pathlib.Path.read_text

            def refuse(self, *args, **kwargs):
                if self.name == "leaf.md":
                    raise OSError(13, "Permission denied")
                return real_read(self, *args, **kwargs)

            pathlib.Path.read_text = refuse
            try:
                self.assertEqual(1, contract.scan(root).unreadable_files)
            finally:
                pathlib.Path.read_text = real_read

    def test_counter_output_surface_is_printed(self) -> None:
        """The printed counters ARE gate 4's evidence, so they must be pinned.

        A reviewer's mutant deleting the `unreadable_files_skipped` print line
        survived the whole suite: the dataclass field was pinned while the line
        that exposes it was not, so a refactor could silently remove the very
        evidence surface it was added to create.
        """
        import contextlib
        import io

        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / contract.TASK_PATH).write_text(ALLOWLIST_HEADER, encoding="utf-8")
            self._commit(root)
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                contract.main(["--root", str(root)])
        printed = stream.getvalue()
        for counter in (
            "allowlist_rows_reviewed=",
            "allowlist_rows_unreviewed=",
            "clickable_links=",
            "unallowlisted_literals=",
            "forbidden_class_literals=",
            "unreadable_files_skipped=",
        ):
            with self.subTest(counter=counter):
                self.assertIn(counter, printed)

    def test_unreadable_files_are_counted_not_silently_skipped(self) -> None:
        # The scan's own output is gate 4's evidence, so a skipped file that
        # leaves no trace is a hole the evidence cannot show.
        with tempfile.TemporaryDirectory() as directory:
            root = self._repo(directory)
            (root / "docs/binary.md").write_bytes(b"\xff\xfe\x00bad")
            (root / contract.TASK_PATH).write_text(ALLOWLIST_HEADER, encoding="utf-8")
            self._commit(root)
            self.assertEqual(1, contract.scan(root).unreadable_files)

    def test_a_missing_task_document_reports_rather_than_crashes(self) -> None:
        # Raising a named exception nothing catches only renamed the traceback:
        # the operator still got no verdict, no counters, and no finding list.
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            with self.assertRaises(contract.AllowlistUnavailable):
                contract.read_allowlist(root)
            # Exit 2 must be distinguishable from a legitimate gate failure (1).
            self.assertEqual(2, contract.main(["--root", str(root)]))


class LineAttributionTests(unittest.TestCase):
    """Findings must name the line the link is actually on."""

    def test_no_finding_is_fabricated_on_the_preceding_line(self) -> None:
        text = f"This line is totally clean.\n[a](../{SLUG}/x.md)"
        self.assertEqual({2: "inline-link"}, contract._clickable_lines(text))

    def test_several_links_report_their_own_lines(self) -> None:
        text = "\n".join(["x", f"[a](../{SLUG}/a.md)", "y", f"[a](../{SLUG}/b.md)"])
        self.assertEqual([2, 4], sorted(contract._clickable_lines(text)))


class CrossLineDestinationTests(unittest.TestCase):
    """A URL parser strips CR and LF, so a broken destination still links."""

    CASES = {
        "attribute_split_inside_url": (
            '<a href="../2026-07-05\n-agentic-research-pack-refresh/x.md">'
        ),
        "reference_definition_on_next_line": f"[r]:\n../{SLUG}/x.md",
        "newline_before_equals": f'<a href\n="../{SLUG}/x.md">',
        "backslash_separator": f'<a href="..\\{SLUG}\\x.md">',
    }

    def test_cross_line_destinations_are_detected(self) -> None:
        for name, text in self.CASES.items():
            with self.subTest(form=name):
                self.assertTrue(contract._clickable_lines(text), name)

    def test_destination_split_over_more_than_two_lines(self) -> None:
        # The window was fixed at two lines, so a destination broken over three
        # or more scored zero findings in both halves of the gate.
        head, tail = SLUG[:12], SLUG[12:]
        for parts in (
            f'<a href="../{head}\n{tail[:10]}\n{tail[10:]}/x.md">',
            f'<a href="../{head}\n{tail[:8]}\n{tail[8:18]}\n{tail[18:]}/x.md">',
        ):
            with self.subTest(lines=parts.count("\n") + 1):
                self.assertEqual(
                    {1: "split-html-attribute"}, contract._clickable_lines(parts)
                )

    def test_tab_is_stripped_like_a_newline(self) -> None:
        # The URL parser removes tab, LF and CR alike. Only two were handled,
        # so a tab-bearing destination resolved while scoring zero findings.
        head, tail = SLUG[:12], SLUG[12:]
        for form in ("\t", "&#9;", "&Tab;"):
            with self.subTest(form=form):
                text = f'<a href="../{head}{form}{tail}/x.md">'
                self.assertEqual({1: "html-attribute"}, contract._clickable_lines(text))

    def test_url_bearing_attributes_beyond_href_and_src(self) -> None:
        # These were detected only as literals, which a reviewed allowlist row
        # then suppressed -- the amplification the clickable check prevents.
        for attribute in ("srcset", "data", "poster", "action", "formaction"):
            with self.subTest(attribute=attribute):
                text = f'<x {attribute}="../{SLUG}/x.md">'
                self.assertEqual({1: "html-attribute"}, contract._clickable_lines(text))

    def test_unambiguous_attributes_need_no_enclosing_tag(self) -> None:
        """`href` and `src` are not ordinary prose, so they match anywhere.

        Requiring an enclosing tag for these lost real clickable HTML and the
        gate printed PASS with a working link present: an attribute at column
        zero on a continuation line concatenates to `<ahref=`, a `>` inside an
        earlier quoted value blocks a `[^<>]` prefix, and a tag opened further
        above than WINDOW_LINES is outside the window altogether.
        """
        for name, text in {
            "unindented_continuation": f'<a\nhref="../{SLUG}/x.md">l</a>',
            "self_closing_img": f'<img\nsrc="../{SLUG}/x.png"\n/>',
            "gt_inside_earlier_value": (
                f'<a title="Docs > Research" href="../{SLUG}/x.md">l</a>'
            ),
        }.items():
            with self.subTest(form=name):
                # Assert the LINE, not just truthiness: a bare assertTrue
                # cannot catch a re-introduced misattribution, which is the
                # defect two earlier rounds shipped.
                found = contract._clickable_lines(text)
                self.assertEqual([1], list(found), name)
                self.assertIn("html-attribute", found[1], name)

    def test_tag_opened_beyond_the_window_is_a_declared_limit(self) -> None:
        """A tag opened further above than WINDOW_LINES is NOT detected.

        This is asserted as a limit, not fixed. It was detected for one round,
        when the attribute matched with no tag context at all -- the same
        exemption that made `src = "..."` in Python an unsuppressable false
        positive. No windowed matcher can see a tag outside its window, so the
        choice is between this miss and that false-positive class. The miss is
        recorded in the module docstring as declared non-coverage.
        """
        text = "<a\n" + "x\n" * 8 + f'href="../{SLUG}/x.md">l'
        self.assertEqual({}, contract._clickable_lines(text))

    def test_multi_line_ambiguous_attribute_tag(self) -> None:
        # `<object` + `data=` concatenate to `<objectdata=`, which no word
        # boundary matches, so every multi-line tag was missed until the window
        # gained a space-joined pass.
        for tag in ("object data", "video poster", "form action"):
            element, attribute = tag.split()
            text = f'<{element}\n{attribute}="../{SLUG}/x">'
            with self.subTest(element=element):
                self.assertTrue(contract._clickable_lines(text))

    def test_attribute_names_outside_a_tag_are_not_clickable(self) -> None:
        """`data`, `action` and friends are ordinary identifiers too.

        A clickable finding bypasses the allowlist by design, so a false
        positive here is unsuppressable by any reviewed row and makes the gate
        unpassable. Widening the attribute list without requiring tag context
        turned prose and a Python assignment into permanent gate failures.
        """
        for text in (
            f'data = "docs/90.references/research/{SLUG}/README.md"',
            f"The action = docs/90.references/research/{SLUG}/README.md is noted.",
            f"curl --data=docs/90.references/research/{SLUG}/README.md http://x",
            f"cite: docs/90.references/research/{SLUG}/README.md",
            # The unambiguous half was exempted from tag context for one round
            # and re-acquired exactly this class. A clickable finding bypasses
            # the allowlist, so no reviewed row can clear these and the gate
            # becomes unpassable. Both halves are pinned here.
            f'src = "docs/90.references/research/{SLUG}/README.md"',
            f'href = "docs/90.references/research/{SLUG}/x.md"',
            f'poster = "docs/90.references/research/{SLUG}/a.png"',
            f"rsync --src=docs/90.references/research/{SLUG}/ dest/",
            f"the src = docs/90.references/research/{SLUG}/x.md value",
        ):
            with self.subTest(text=text[:40]):
                self.assertEqual({}, contract._clickable_lines(text))

    def test_window_bound_matches_its_documented_meaning(self) -> None:
        # WINDOW_LINES documents how many lines a destination MAY span. The
        # slice took one more than that, so the shipped width exceeded the
        # constant and the ledger understated it.
        def split_over(count: int) -> str:
            size = len(SLUG) // count + 1
            parts = [SLUG[i : i + size] for i in range(0, len(SLUG), size)]
            return '<a href="../' + "\n".join(parts) + '/x.md">'

        self.assertTrue(contract._clickable_lines(split_over(contract.WINDOW_LINES)))
        self.assertFalse(
            contract._clickable_lines(split_over(contract.WINDOW_LINES + 1))
        )

    def test_multiline_form_detects_its_own_case(self) -> None:
        # Emptying NEWLINE_WINDOW_FORMS survived the suite: the form had no
        # detection test, only the fabrication half of its behaviour pinned.
        self.assertTrue(
            any(
                name == "multiline-link"
                for _, name in contract._clickable_lines(
                    f"[a](../\n{SLUG}/x.md)"
                ).items()
            )
        )

    def test_inline_destination_may_contain_a_space(self) -> None:
        # Tightening _INLINE's class to exclude whitespace survived the suite
        # while silently losing angle-bracket destinations containing a space.
        self.assertTrue(contract._clickable_lines(f"[a](<../my dir/{SLUG}/x.md>)"))


class NormalizationTests(unittest.TestCase):
    """Pins the normalization behaviours whose mutants previously survived."""

    def test_newlines_are_deleted_not_replaced(self) -> None:
        self.assertEqual("ab", contract._normalize("a\nb"))
        self.assertEqual("ab", contract._normalize("a%0Ab"))

    def test_headings_only_parsed_in_markdown(self) -> None:
        # The fixture must be text the heading pattern WOULD match, or the
        # assertion holds whether or not the flag is honoured. The previous
        # fixture was "#!/usr/bin/env python3", which the pattern rejects on
        # its own, so mutating `if markdown:` to `if True:` survived the suite.
        text = "# Title\nbody"
        self.assertEqual(("Title",), contract._headings_by_line(text, True)[2])
        self.assertEqual((), contract._headings_by_line(text, False)[2])
        self.assertEqual(
            ("!/usr/bin/env python3",),
            contract._headings_by_line("# !/usr/bin/env python3\nx", True)[2],
        )

    def test_heading_chain_keeps_ancestors(self) -> None:
        chain = contract._headings_by_line("# Top\n\n## Inner\n\nbody", True)[5]
        self.assertEqual(("Top", "Inner"), chain)

    def test_anchor_text_strips_the_declared_hash_prefix(self) -> None:
        self.assertEqual("top", contract._anchor_text("# Top"))
        self.assertEqual("inner", contract._anchor_text("### Inner"))


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
        # "requested" is ordinary approved prose and must not demote.
        "Approved; requested changes were applied",
        "Reviewed and approved after the requested fixes landed",
    )
    UNSETTLED = (
        "",
        "Not Run",
        "independent pack review pending",
        "Not Run; independent review requested 2026-08-18",
        # A requested review is an open state even when the leading clause
        # settles. Round 3 dropped the "requested" token to stop it demoting
        # "requested changes", and tested only that benign direction, so these
        # two settled while every open row in the ledger uses this exact phrase.
        "Task 10b implementer reviewed; independent review requested 2026-08-18",
        "Task 10b implementer reviewed; independent re-review requested",
        "Approved by the implementer; a second review is requested",
        "Reviewed; re-reviews have been requested from both seats",
        # Excluding on the noun alone was an unconditional escape hatch, so
        # these settled and the outcome depended on voice rather than state.
        # The fix shipped unpinned and a reviewer's mutant reverting it
        # survived the whole suite; these hold it.
        "Approved C0/I0/M0; the seat requested changes",
        "Approved C0/I0/M0; requested changes remain open",
        "Approved C0/I0/M0; requested changes not yet supplied",
        "reviewed; requested revisions still needed",
        # Residual forms the first subject binding missed: an adverb between
        # the subject and the verb, verb-first phrasing, and the forge's own
        # change-request verdict token.
        "Task 10b implementer reviewed; independent review still requested",
        "Task 10b implementer reviewed; requested an independent review",
        "Task 10b implementer reviewed; changes requested",
        "Reviewed; changes were requested by the second seat",
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
        # Same two clauses, reversed. The verdict must not depend on order.
        "quality Needs fixes C0/I2/M10; specification Approved C0/I0/M0",
        "Needs fixes; re-reviewed round 2",
        "Needs fixes; awaiting C0/I0",
        "Needs fixes; target is C0/I0",
        "Needs fixes; do not mark approved",
        "Needs fixes / reviewed",
        "Rejected. The neighbouring literal was approved.",
        "outstanding Important finding; reviewed 2026-08-01",
        "review in progress; last approved 2026-07-01",
        "review abandoned; previously approved",
        # Self-approval wording, which the ledger's seat constraint forbids.
        "auto-approved",
        "approved by the author",
        "Approved (self)",
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

    # Refreshed 2026-08-19. The pinned set was stale: the taxonomy merge admitted
    # further rows and the Route-1 admission and split-row evaluation amendment
    # made every declared row a subject, so two rows previously hidden by a
    # path collision are now counted.
    # Refreshed 2026-08-19. The set has moved three times in one day: a stale
    # pin, then two settled verdicts withdrawn after a seat found the amended
    # route 1 does not admit them, then seven rows settled on that same seat's
    # verdict. The count therefore falls and then rises, and both directions are
    # recorded rather than smoothed.
    EXPECTED_UNREVIEWED = {
        "docs/03.specs/0105-agentic-engineering-implementation-audit-pack/spec.md",
        "docs/03.specs/0123-agentic-engineering-audit-remediation/spec.md",
        "docs/03.specs/0123-agentic-engineering-audit-remediation/tasks/tsk-0001-research-pack-extension.md",
        "docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md",
        "scripts/validation/check-document-corpus-lifecycle.py",
        "tests/validation/test_document_corpus_lifecycle.py",
        "tests/validation/test_document_taxonomy.py",
    }

    def test_allowlist_split_is_exact(self) -> None:
        """Pins the split, so a forced-settled regression cannot survive."""
        rows = contract.read_allowlist(ROOT)
        unreviewed = {
            path
            for path, group in rows.items()
            if any(not row.settled for row in group)
        }
        self.assertEqual(self.EXPECTED_UNREVIEWED, unreviewed)
        settled = sum(1 for group in rows.values() for row in group if row.settled)
        self.assertEqual(35, settled)

    def test_no_live_row_declares_a_forbidden_class(self) -> None:
        rows = contract.read_allowlist(ROOT)
        offenders = [
            path
            for path, group in rows.items()
            for row in group
            if row.forbidden_class
        ]
        self.assertEqual([], offenders)

    def test_malformed_row_fails_loudly(self) -> None:
        """An unescaped pipe must not shift the verdict into another field.

        `pick` indexes cells by header position, so a row with more cells than
        the header is misread rather than skipped. On 2026-08-19 a pasted table
        fragment put the text `Criteria source` where the review verdict
        belongs; it failed closed only because that string does not settle.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            task = root / contract.TASK_PATH
            task.parent.mkdir(parents=True)
            task.write_text(
                "### Old-path allowlist\n\n"
                "| Path | Line or stable anchor | Literal class | Reason | Review verdict |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| `a.md` | `x` | Factual history | reason with | an unescaped pipe | Approved |\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError) as caught:
                contract.read_allowlist(root)
            self.assertIn("header cell count", str(caught.exception))

    def test_rows_sharing_a_path_all_survive(self) -> None:
        """A split row must not be overwritten by its sibling.

        Spec 137's Route-1 admission and split-row evaluation amendment makes
        each declared row a separate subject. Before the fix the allowlist was a
        dict of one row per path, so the three-way migration-ledger split
        collapsed to whichever row parsed last and a settled verdict on it would
        have marked its siblings' literals reviewed.
        """
        rows = contract.read_allowlist(ROOT)
        ledger = rows["docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md"]
        self.assertEqual(3, len(ledger))
        self.assertEqual(
            {
                "Factual history",
                "Commit-pinned baseline",
                "Non-resolving same-slug",
            },
            {row.literal_class for row in ledger},
        )
        total = sum(len(group) for group in rows.values())
        self.assertEqual(43, total)
        self.assertGreater(total, len(rows))

    def test_one_unsettled_sibling_leaves_the_whole_path_unreviewed(self) -> None:
        """The collapse fails closed rather than trusting a settled sibling."""
        settled = contract.AllowRow(
            path="p",
            anchors=("a",),
            literal_class="Factual history",
            verdict="Approved",
            settled=True,
            forbidden_class=False,
        )
        unsettled = contract.AllowRow(
            path="p",
            anchors=("b",),
            literal_class="Commit-pinned baseline",
            verdict="Not Run",
            settled=False,
            forbidden_class=False,
        )
        forbidden = contract.AllowRow(
            path="p",
            anchors=("c",),
            literal_class="Current router",
            verdict="Approved",
            settled=True,
            forbidden_class=True,
        )
        self.assertIsNone(contract._collapse_rows([]))
        self.assertFalse(contract._collapse_rows([settled, unsettled]).settled)
        self.assertTrue(contract._collapse_rows([settled, forbidden]).forbidden_class)
        self.assertTrue(contract._collapse_rows([settled, settled]).settled)

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
